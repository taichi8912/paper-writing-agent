"""Tests for the bibliography context indexer, validator, and grounding."""

from __future__ import annotations

import copy

from paper_writing_agent.bibindex import (
    apply_grounding,
    build_index,
    extract_usage,
    find_duplicate_keys,
    merge_index,
    parse_bibtex,
    validate_index,
)

SAMPLE_BIB = r"""
@article{smith2021attention,
  title = {Attention Improves Neural Translation},
  author = {Smith, Jane and Doe, John},
  journal = {Journal of Machine Learning},
  year = {2021},
  doi = {10.1/abc},
}

@inproceedings{lee2020gpu,
  title = "A GPU Kernel for Fast Convolution",
  author = "Lee, Kim",
  booktitle = "Proceedings of Systems",
  year = "2020"
}

% a stray comment
@misc{nadel2019dataset,
  title = {{The Benchmark Dataset Collection}},
  author = {Nadel, A.},
  year = {2019},
  url = {https://example.org/data}
}
"""


def test_parse_extracts_entries_and_fields():
    entries = parse_bibtex(SAMPLE_BIB)
    assert [e.key for e in entries] == ["smith2021attention", "lee2020gpu", "nadel2019dataset"]
    smith = entries[0]
    assert smith.entry_type == "article"
    assert smith.title() == "Attention Improves Neural Translation"
    assert smith.authors() == ["Smith", "Doe"]
    assert smith.venue() == "Journal of Machine Learning"
    assert smith.year() == "2021"


def test_quoted_and_braced_values_both_parse():
    entries = {e.key: e for e in parse_bibtex(SAMPLE_BIB)}
    assert entries["lee2020gpu"].title() == "A GPU Kernel for Fast Convolution"
    assert entries["nadel2019dataset"].title() == "The Benchmark Dataset Collection"


def test_duplicate_keys_detected():
    dup = SAMPLE_BIB + "\n@misc{smith2021attention, title={dup}, year={2022}}"
    entries = parse_bibtex(dup)
    assert find_duplicate_keys(entries) == ["smith2021attention"]


def test_build_index_structure_and_cite_as():
    index = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    assert index["metadata"]["unique_keys"] == 3
    ids = [e["id"] for e in index["entries"]]
    assert ids == ["smith2021attention", "lee2020gpu", "nadel2019dataset"]
    smith = index["entries"][0]
    assert smith["cite_as"] == r"\cite{smith2021attention}"
    assert smith["curation_status"] == "derived"
    assert "deep_learning_architecture" in smith["topics"] or "nlp" in smith["topics"]


def test_freshly_built_index_validates():
    index = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    report = validate_index(index)
    assert report.ok, report.render()


def test_validate_detects_coverage_gap():
    index = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    # Remove one entry; coverage against the full bib must fail.
    index["entries"] = index["entries"][:-1]
    keys = [e.key for e in parse_bibtex(SAMPLE_BIB)]
    report = validate_index(index, bib_keys=keys)
    assert not report.ok
    assert any("coverage" in e for e in report.errors)


def test_validate_flags_forbidden_vocab_in_curated_field():
    index = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    entry = index["entries"][0]
    entry["curation_status"] = "verified"
    entry["sample_phrases"] = ["This delve into a pivotal idea."]
    report = validate_index(index)
    assert not report.ok
    assert any("forbidden word" in e for e in report.errors)


def test_validate_flags_placeholder_text():
    index = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    entry = index["entries"][0]
    entry["curation_status"] = "verified"
    entry["suitable_contexts"] = ["TODO: fill this in"]
    report = validate_index(index)
    assert not report.ok
    assert any("placeholder" in e for e in report.errors)


def test_validate_bad_cite_as():
    index = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    index["entries"][0]["cite_as"] = "\\cite{wrong}"
    report = validate_index(index)
    assert not report.ok
    assert any("cite_as" in e for e in report.errors)


def test_strict_mode_rejects_needs_review():
    index = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    index["entries"][0]["curation_status"] = "needs_review"
    assert validate_index(index, strict=False).ok
    assert not validate_index(index, strict=True).ok


def test_merge_preserves_existing_curation():
    base = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    curated = copy.deepcopy(base)
    curated["entries"][0]["key_findings"] = "A carefully curated finding."
    curated["entries"][0]["curation_status"] = "verified"

    extended_bib = SAMPLE_BIB + "\n@misc{new2023, title={A New Tool}, author={X, Y}, year={2023}}"
    fresh = build_index(parse_bibtex(extended_bib), source_bib="sample.bib")

    merged = merge_index(curated, fresh)
    by_id = {e["id"]: e for e in merged["entries"]}
    assert by_id["smith2021attention"]["key_findings"] == "A carefully curated finding."
    assert by_id["smith2021attention"]["curation_status"] == "verified"
    assert "new2023" in by_id  # new key added


def test_grounding_extracts_section_and_sentence():
    prior = r"""
\section{Introduction}
Transformers changed translation \citep{smith2021attention}. We build on this.

\section{Methods}
We used a custom kernel \cite{lee2020gpu} for speed.
"""
    usage = extract_usage(prior)
    assert "smith2021attention" in usage
    assert usage["smith2021attention"][0]["section"] == "Introduction"
    assert "Transformers" in usage["smith2021attention"][0]["sentence"]
    assert usage["lee2020gpu"][0]["section"] == "Methods"


def test_apply_grounding_marks_verified():
    index = build_index(parse_bibtex(SAMPLE_BIB), source_bib="sample.bib")
    prior = r"\section{Intro}\nText \cite{lee2020gpu} here."
    grounded = apply_grounding(index, extract_usage(prior))
    assert grounded == 1
    lee = next(e for e in index["entries"] if e["id"] == "lee2020gpu")
    assert lee["curation_status"] == "verified"
    assert lee["author_usage"]
