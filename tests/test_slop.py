"""Tests for the anti-AI-slop linter."""

from __future__ import annotations

import json

from paper_writing_agent.config import Config, get_preset
from paper_writing_agent.config.model import SlopConfig
from paper_writing_agent.slop import (
    format_json,
    has_errors,
    lint_text,
    summarize,
)


def _ids(findings):
    return {f.rule_id for f in findings}


def test_detects_tier1_words():
    text = "We delve into the problem and underscore a pivotal, novel result."
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    ids = _ids(findings)
    assert "tier1.delv" in ids
    assert "tier1.underscor" in ids
    assert "tier1.pivotal" in ids
    assert "tier1.novel" in ids
    assert all(f.severity == "error" for f in findings if f.category == "tier1")


def test_detects_tier2_with_suggestion():
    text = "We leverage the GPU to enhance throughput."
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    by_id = {f.rule_id: f for f in findings}
    assert "tier2.leverag" in by_id
    assert by_id["tier2.leverag"].severity == "warning"
    assert "use" in (by_id["tier2.leverag"].suggestion or "")


def test_detects_tier3_phrase():
    text = "Due to the fact that the cache missed, latency rose."
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "tier3.due-to-the-fact-that" in _ids(findings)


def test_em_dash_flagged_by_default_and_suppressed_when_allowed():
    text = "The compiler — our baseline — was slow."
    strict = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "struct.em-dash" in _ids(strict)

    lenient = lint_text(text, path="a.md", config=get_preset("lenient"))
    assert "struct.em-dash" not in _ids(lenient)


def test_structural_participle_padding():
    text = "Throughput rose by 32%, demonstrating the value of the optimization."
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "struct.participle-padding" in _ids(findings)


def test_code_blocks_are_not_linted_markdown():
    text = "Normal prose.\n\n```\nwe leverage delve pivotal\n```\n\nInline `leverage` too."
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    # Nothing inside the fenced block or inline code should be flagged.
    assert findings == []


def test_latex_math_and_comments_are_not_linted():
    text = "Real prose is fine.\n% we leverage delve here in a comment\n$x = \\text{leverage}$\n"
    findings = lint_text(text, path="a.tex", config=get_preset("strict-high-IF"))
    assert findings == []


def test_latex_cite_argument_is_masked():
    text = "As reported \\cite{leverage2024delve}, throughput improved."
    findings = lint_text(text, path="a.tex", config=get_preset("strict-high-IF"))
    assert findings == []


def test_allow_list_suppresses_word():
    cfg = Config(slop=SlopConfig(enabled_tiers=[1, 2, 3], allow=["novel"]))
    text = "A novel idea that we leverage."
    ids = _ids(lint_text(text, path="a.md", config=cfg))
    assert "tier1.novel" not in ids
    assert "tier2.leverag" in ids  # still flagged


def test_extra_forbidden_words():
    cfg = Config(slop=SlopConfig(extra_forbidden=["quux"]))
    findings = lint_text("The quux module is ready.", path="a.md", config=cfg)
    assert any(f.rule_id == "tier1.custom.quux" for f in findings)


def test_lenient_does_not_flag_tier2():
    text = "We leverage the cache to enhance speed."
    findings = lint_text(text, path="a.md", config=get_preset("lenient"))
    # Lenient enables tier 1 only.
    assert all(f.category != "tier2" for f in findings)


def test_findings_are_sorted_by_position():
    text = "pivotal\nnovel delve"
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    positions = [(f.line, f.col) for f in findings]
    assert positions == sorted(positions)


def test_line_and_column_are_reported():
    text = "ok line\nthen pivotal here"
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    pivotal = next(f for f in findings if f.rule_id == "tier1.pivotal")
    assert pivotal.line == 2
    assert pivotal.col == 6


def test_json_output_is_valid_and_has_summary():
    text = "We delve and leverage."
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    payload = json.loads(format_json(findings))
    assert payload["summary"]["total"] == len(findings)
    assert payload["summary"]["error"] >= 1
    assert {"findings", "summary"} == set(payload)


def test_clean_text_has_no_findings_and_no_errors():
    text = "We measured throughput and report a 32% improvement over the baseline."
    findings = lint_text(text, path="a.md", config=get_preset("strict-high-IF"))
    assert findings == []
    assert summarize(findings)["total"] == 0
    assert has_errors(findings) is False
