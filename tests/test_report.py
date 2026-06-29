"""Tests for the shared finding report formatters."""

from __future__ import annotations

import json

from paper_writing_agent.slop import format_json, format_text, has_errors, summarize
from paper_writing_agent.slop.linter import Finding


def _finding(severity="error", rule_id="tier1.delv"):
    return Finding(
        path="a.md",
        line=1,
        col=4,
        rule_id=rule_id,
        category="tier1",
        severity=severity,
        matched="delve",
        message="Tier-1 forbidden word.",
        suggestion="examine, study",
    )


def test_summarize_counts():
    findings = [_finding("error"), _finding("warning", "tier2.leverag")]
    summary = summarize(findings)
    assert summary == {"total": 2, "error": 1, "warning": 1}


def test_has_errors():
    assert has_errors([_finding("error")]) is True
    assert has_errors([_finding("warning", "tier2.leverag")]) is False
    assert has_errors([]) is False


def test_format_text_includes_location_and_suggestion():
    text = format_text([_finding()])
    assert "a.md:1:4" in text
    assert "tier1.delv" in text
    assert "examine, study" in text
    assert "1 finding(s)" in text


def test_format_text_empty():
    assert format_text([]) == "No findings."


def test_format_json_roundtrip():
    payload = json.loads(format_json([_finding()]))
    assert payload["summary"]["total"] == 1
    assert payload["findings"][0]["rule_id"] == "tier1.delv"
    assert payload["findings"][0]["matched"] == "delve"
