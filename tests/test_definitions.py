"""Tests for the definitions / no-forward-reference linter."""

from __future__ import annotations

from paper_writing_agent.definitions import build_registry, lint_definitions


def _ids(findings):
    return {f.rule_id for f in findings}


def _write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_forward_reference_flagged(tmp_path):
    text = (
        "We evaluate the CNN on three tasks. "
        "A Convolutional Neural Network (CNN) is a standard model."
    )
    path = _write(tmp_path, "a.md", text)
    findings = lint_definitions([path])
    assert "defs.forward-reference" in _ids(findings)


def test_define_then_use_is_clean(tmp_path):
    text = (
        "A Convolutional Neural Network (CNN) is a standard model. "
        "We evaluate the CNN on three tasks."
    )
    path = _write(tmp_path, "a.md", text)
    findings = lint_definitions([path])
    assert findings == []


def test_redefinition_flagged(tmp_path):
    text = (
        "A Convolutional Neural Network (CNN) is a model. "
        "Later we restate the Convolutional Neural Network (CNN) again."
    )
    path = _write(tmp_path, "a.md", text)
    findings = lint_definitions([path])
    assert "defs.redefinition" in _ids(findings)


def test_reading_order_across_files(tmp_path):
    first = _write(tmp_path, "01_intro.md", "We rely on the GPU throughout.")
    second = _write(tmp_path, "02_methods.md", "We used a Graphics Processing Unit (GPU).")
    findings = lint_definitions([first, second])
    assert "defs.forward-reference" in _ids(findings)


def test_code_and_math_are_ignored(tmp_path):
    text = (
        "```\nThe CNN appears in code.\n```\n"
        "A Convolutional Neural Network (CNN) is defined here. We use the CNN next."
    )
    path = _write(tmp_path, "a.md", text)
    findings = lint_definitions([path])
    assert findings == []


def test_build_registry(tmp_path):
    text = "A Convolutional Neural Network (CNN) and a Recurrent Neural Network (RNN)."
    path = _write(tmp_path, "a.md", text)
    registry = build_registry([path])
    abbrevs = {entry["abbreviation"] for entry in registry["abbreviations"]}
    assert {"CNN", "RNN"} <= abbrevs
