"""Tests for region masking."""

from __future__ import annotations

from paper_writing_agent.slop.masking import detect_file_type, mask_regions


def test_detect_file_type():
    assert detect_file_type("a.tex") == "latex"
    assert detect_file_type("a.LaTeX") == "latex"
    assert detect_file_type("a.md") == "markdown"
    assert detect_file_type("a.markdown") == "markdown"


def test_mask_preserves_length_and_newlines():
    text = "line one\n```\ncode\n```\nline two\n"
    masked = mask_regions(text, "markdown")
    assert len(masked) == len(text)
    assert masked.count("\n") == text.count("\n")


def test_markdown_code_is_blanked():
    text = "use `leverage` here"
    masked = mask_regions(text, "markdown")
    assert "leverage" not in masked
    assert masked.startswith("use ")


def test_markdown_fenced_block_blanked():
    text = "before\n```\nleverage pivotal\n```\nafter"
    masked = mask_regions(text, "markdown")
    assert "leverage" not in masked
    assert "before" in masked and "after" in masked


def test_latex_comment_and_verbatim_blanked():
    text = "real % leverage in comment\n\\begin{verbatim}\nleverage\n\\end{verbatim}\n"
    masked = mask_regions(text, "latex")
    assert "leverage" not in masked
    assert "real" in masked


def test_cite_argument_blanked():
    text = "see \\cite{leverage2020} now"
    masked = mask_regions(text, "latex")
    assert "leverage2020" not in masked
    assert masked.startswith("see ")


def test_math_toggle():
    text = "value $P = 2.6 \\times 10^{-5}$ end"
    masked_on = mask_regions(text, "latex", mask_math=True)
    masked_off = mask_regions(text, "latex", mask_math=False)
    assert "10^{-5}" not in masked_on  # math masked
    assert "10^{-5}" in masked_off  # math kept (so the stats linter can see P)


def test_markdown_dollar_math_masked_by_default():
    text = "inline $x = leverage$ math"
    assert "leverage" not in mask_regions(text, "markdown")
    assert "leverage" in mask_regions(text, "markdown", mask_math=False)
