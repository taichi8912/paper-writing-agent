"""Tests for the manuscript-workspace scaffolder."""

from __future__ import annotations

import os

from paper_writing_agent.config import get_preset
from paper_writing_agent.scaffold import placeholders, scaffold_workspace


def test_scaffold_creates_expected_files(tmp_path):
    config = get_preset("balanced")
    created = scaffold_workspace(str(tmp_path), config)
    names = {os.path.relpath(p, str(tmp_path)) for p in created}
    assert "README.md" in names
    assert "PROJECT_PROFILE.md" in names
    assert "section_status.yaml" in names
    assert os.path.join("bib", "README.md") in names
    assert os.path.join("stats", "README.md") in names


def test_placeholders_are_substituted(tmp_path):
    config = get_preset("strict-high-IF")
    config.style.spelling = "UK"
    scaffold_workspace(str(tmp_path), config)
    profile = (tmp_path / "PROJECT_PROFILE.md").read_text(encoding="utf-8")
    assert "Spelling: UK" in profile
    assert "{{" not in profile  # all placeholders resolved


def test_scaffold_does_not_overwrite_existing(tmp_path):
    config = get_preset("balanced")
    readme = tmp_path / "README.md"
    readme.write_text("KEEP ME", encoding="utf-8")
    created = scaffold_workspace(str(tmp_path), config)
    assert readme.read_text(encoding="utf-8") == "KEEP ME"
    assert str(readme) not in created  # skipped, not reported as created


def test_overwrite_flag_replaces(tmp_path):
    config = get_preset("balanced")
    readme = tmp_path / "README.md"
    readme.write_text("OLD", encoding="utf-8")
    scaffold_workspace(str(tmp_path), config, overwrite=True)
    assert readme.read_text(encoding="utf-8") != "OLD"


def test_placeholders_mapping_covers_config():
    mapping = placeholders(get_preset("balanced"))
    assert mapping["FIELD"] == "computer-science"
    assert mapping["PRESET"] == "balanced"
    assert "PVALUE_NOTATION" in mapping
