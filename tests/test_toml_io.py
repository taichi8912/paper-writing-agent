"""Tests for the dependency-free TOML serializer/parser."""

from __future__ import annotations

import pytest

from paper_writing_agent.config import toml_io


def test_dumps_scalars_and_tables():
    data = {"top": "value", "table": {"n": 2, "flag": True, "items": ["a", "b"]}}
    text = toml_io.dumps(data)
    assert 'top = "value"' in text
    assert "[table]" in text
    assert "n = 2" in text
    assert "flag = true" in text
    assert 'items = ["a", "b"]' in text


def test_roundtrip_via_fallback():
    data = {
        "project": {"field": "computer-science", "preset": "balanced"},
        "slop": {"enabled_tiers": [1, 2, 3], "em_dash": "zero", "detect_structural": True},
    }
    text = toml_io.dumps(data)
    parsed = toml_io._fallback_loads(text)
    assert parsed == data


def test_loads_prefers_real_parser_when_available():
    # loads() should agree with the fallback on the subset we emit.
    data = {"a": {"b": "c", "d": [1, 2]}}
    assert toml_io.loads(toml_io.dumps(data)) == data


def test_comments_and_blank_lines_ignored():
    text = '# header\n\n[t]\nk = "v"  # trailing\n'
    assert toml_io._fallback_loads(text) == {"t": {"k": "v"}}


def test_header_is_emitted_as_comments():
    text = toml_io.dumps({"a": 1}, header="line one\nline two")
    assert text.startswith("# line one\n# line two\n")


def test_string_escaping_roundtrip():
    data = {"t": {"path": 'a "quoted" word'}}
    assert toml_io._fallback_loads(toml_io.dumps(data)) == data


def test_unsupported_type_raises():
    with pytest.raises(TypeError):
        toml_io.dumps({"bad": {1, 2, 3}})
