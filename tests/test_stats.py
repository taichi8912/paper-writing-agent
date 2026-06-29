"""Tests for the statistical-honesty linter."""

from __future__ import annotations

from paper_writing_agent.config import get_preset
from paper_writing_agent.stats import lint_stats


def _ids(findings):
    return {f.rule_id for f in findings}


def test_pvalue_without_verdict_is_flagged():
    text = "Group A scored higher than B (P = 1.2e-5)."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "stats.pvalue-no-verdict" in _ids(findings)


def test_pvalue_with_verdict_is_accepted():
    text = "The difference was significant (P = 1.2e-5; Welch's t-test)."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "stats.pvalue-no-verdict" not in _ids(findings)


def test_verdict_in_adjacent_sentence_is_accepted():
    text = "We compared the two systems. The difference was not significant (P = 0.21)."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "stats.pvalue-no-verdict" not in _ids(findings)


def test_lowercase_p_flagged_when_house_style_is_capital():
    text = "The effect was significant (p = 0.001)."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "stats.pvalue-case" in _ids(findings)


def test_enotation_flagged_for_sci_style():
    text = "The effect was significant (P = 2.6e-5)."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "stats.pvalue-enotation" in _ids(findings)


def test_leading_zero():
    text = "The correlation was significant (r = .45, P = .01)."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "stats.leading-zero" in _ids(findings)


def test_number_unit_spacing():
    text = "The window was 4000bp wide and the model used 40GB of memory."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    ids = _ids(findings)
    assert "stats.number-unit-spacing" in ids


def test_thousands_separator():
    text = "We processed 300000000 records in total."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "stats.thousands-separator" in _ids(findings)


def test_repeated_test_name_flagged():
    text = (
        "The difference was significant (P = 0.01; Welch's t-test). "
        "A later comparison used a Welch's t-test as well."
    )
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert "stats.test-name-repeated" in _ids(findings)


def test_latex_pvalue_in_math_is_seen():
    text = "The gain was significant ($P = 2.6 \\times 10^{-5}$; Welch's t-test)."
    findings = lint_stats(text, path="a.tex", config=get_preset("strict-high-IF"))
    # math is kept, so a verdict is present and notation is correct -> no p-value defects
    assert "stats.pvalue-no-verdict" not in _ids(findings)
    assert "stats.pvalue-enotation" not in _ids(findings)


def test_clean_text_has_no_findings():
    text = "We report a 32% improvement over the baseline across all configurations."
    findings = lint_stats(text, path="a.md", config=get_preset("strict-high-IF"))
    assert findings == []
