"""Tests that packaged data (schema, templates) is importable as a resource.

These guard the packaging: if package data is not shipped, the schema and the
workspace templates cannot be loaded from an installed wheel.
"""

from __future__ import annotations

from importlib import resources

from paper_writing_agent.bibindex.validate import load_schema


def test_schema_loads_and_is_well_formed():
    schema = load_schema()
    assert schema["type"] == "object"
    assert "entries" in schema["properties"]
    assert "$defs" in schema


def test_workspace_templates_are_packaged():
    base = resources.files("paper_writing_agent").joinpath("templates", "workspace")
    assert base.joinpath("README.md").is_file()
    assert base.joinpath("PROJECT_PROFILE.md").is_file()
    assert base.joinpath("section_status.yaml").is_file()
    assert base.joinpath("bib", "README.md").is_file()


def test_template_has_placeholders():
    base = resources.files("paper_writing_agent").joinpath("templates", "workspace")
    profile = base.joinpath("PROJECT_PROFILE.md").read_text(encoding="utf-8")
    assert "{{SPELLING}}" in profile  # substituted by the scaffolder at init time
