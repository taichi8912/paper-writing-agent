"""Validate a context index against the schema and anti-hallucination gates.

Beyond JSON Schema conformance, the validator enforces the rules that keep
citations honest:

- every BibTeX key has an entry (coverage), if the source keys are supplied;
- no placeholder text leaked into curated fields;
- no Tier-1 forbidden vocabulary in authored prose;
- ``cite_as`` matches the entry id;
- in strict mode, no entry is left ``needs_review``.
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from importlib import resources
from typing import Any

import jsonschema

from ..config import Config
from ..config.model import SlopConfig
from ..slop import lint_text

__all__ = ["ValidationReport", "validate_index", "load_schema"]

_PLACEHOLDER = re.compile(
    r"\b(tbd|tba|todo|fixme|xxx|lorem ipsum|not inferred|needs[ _-]?review)\b|<[^>]+>",
    re.IGNORECASE,
)


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def render(self) -> str:
        lines = [f"[error] {message}" for message in self.errors]
        lines += [f"[warning] {message}" for message in self.warnings]
        if not lines:
            return "Index is valid."
        lines.append("")
        lines.append(f"{len(self.errors)} error(s), {len(self.warnings)} warning(s).")
        return "\n".join(lines)


def load_schema() -> dict[str, Any]:
    text = resources.files("paper_writing_agent.bibindex").joinpath("schema.json").read_text(
        encoding="utf-8"
    )
    return json.loads(text)


def validate_index(
    index: dict[str, Any],
    *,
    bib_keys: Sequence[str] | None = None,
    strict: bool = False,
) -> ValidationReport:
    report = ValidationReport()

    # 1. Schema conformance.
    schema = load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(index), key=lambda e: list(e.path)):
        location = "/".join(str(p) for p in error.path) or "<root>"
        report.errors.append(f"schema: {location}: {error.message}")
    if report.errors:
        # Structural problems make the remaining checks unreliable.
        return report

    entries = index.get("entries", [])
    ids = [entry["id"] for entry in entries]

    # 2. Duplicate ids inside the index.
    duplicates = {entry_id for entry_id in ids if ids.count(entry_id) > 1}
    for entry_id in sorted(duplicates):
        report.errors.append(f"duplicate entry id: {entry_id}")

    # 3. Coverage against the source bibliography.
    if bib_keys is not None:
        missing = [key for key in bib_keys if key not in set(ids)]
        for key in missing:
            report.errors.append(f"coverage: bib key has no index entry: {key}")

    # 4. Per-entry content gates.
    vocab_config = Config(slop=SlopConfig(enabled_tiers=[1], em_dash="allow", detect_structural=False))
    for entry in entries:
        _check_cite_as(entry, report)
        _check_placeholders(entry, report)
        _check_forbidden_vocab(entry, vocab_config, report)
        _check_curation(entry, strict, report)

    return report


def _curated_fields(entry: dict[str, Any]) -> list[tuple[str, str]]:
    """Return (field_label, text) pairs for authored prose, honoring derived seeds.

    ``key_findings`` is checked only once an entry is curated; on a freshly built
    ``derived`` entry it equals the paper title verbatim, which is a quoted fact
    and must not be flagged as authored slop.
    """
    fields: list[tuple[str, str]] = []
    if entry.get("curation_status") != "derived":
        fields.append(("key_findings", entry.get("key_findings", "")))
    for phrase in entry.get("suitable_contexts", []):
        fields.append(("suitable_contexts", phrase))
    for phrase in entry.get("sample_phrases", []):
        fields.append(("sample_phrases", phrase))
    return fields


def _check_cite_as(entry: dict[str, Any], report: ValidationReport) -> None:
    expected = f"\\cite{{{entry['id']}}}"
    if entry.get("cite_as") != expected:
        report.errors.append(f"{entry['id']}: cite_as should be {expected!r}")


def _check_placeholders(entry: dict[str, Any], report: ValidationReport) -> None:
    for label, text in _curated_fields(entry):
        if _PLACEHOLDER.search(text):
            report.errors.append(f"{entry['id']}: placeholder text in {label}: {text!r}")


def _check_forbidden_vocab(
    entry: dict[str, Any], vocab_config: Config, report: ValidationReport
) -> None:
    for label, text in _curated_fields(entry):
        for finding in lint_text(text, path=entry["id"], config=vocab_config):
            report.errors.append(
                f"{entry['id']}: forbidden word in {label}: {finding.matched!r}"
            )


def _check_curation(entry: dict[str, Any], strict: bool, report: ValidationReport) -> None:
    if entry.get("curation_status") == "needs_review":
        message = f"{entry['id']}: curation_status is needs_review"
        if strict:
            report.errors.append(message)
        else:
            report.warnings.append(message)
