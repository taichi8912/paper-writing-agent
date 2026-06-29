"""Tests for the section-status tracker."""

from __future__ import annotations

import pytest

from paper_writing_agent.sections import (
    discover_units,
    exemplars,
    new_tracker,
    set_level,
    summarize,
    sync_tracker,
)
from paper_writing_agent.sections.tracker import TrackerError


def test_discover_latex_units(tmp_path):
    root = tmp_path / "main.tex"
    root.write_text(
        "\\input{introduction}\n\\subfile{results.tex}\n\\include{discussion}\n", encoding="utf-8"
    )
    units = discover_units(str(root))
    names = [u["name"] for u in units]
    assert names == ["introduction", "results", "discussion"]


def test_discover_markdown_units(tmp_path):
    doc = tmp_path / "paper.md"
    doc.write_text("# Intro\n\ntext\n\n## Related Work\n\nmore\n", encoding="utf-8")
    names = [u["name"] for u in discover_units(str(doc))]
    assert names == ["intro", "related-work"]


def test_sync_adds_new_units_as_low_and_flags_missing():
    tracker = new_tracker()
    sync_tracker(tracker, [{"name": "intro", "path": "intro.tex"}])
    assert tracker["units"][0]["level"] == "low"

    set_level(tracker, "intro", "high", reason="done", date="2026-06-29")
    # Re-sync with a different set: intro disappears, methods appears.
    sync_tracker(tracker, [{"name": "methods", "path": "methods.tex"}])
    by_name = {u["name"]: u for u in tracker["units"]}
    assert by_name["intro"]["level"] == "high"  # level preserved
    assert by_name["intro"]["present"] is False  # flagged missing
    assert by_name["methods"]["present"] is True


def test_set_level_records_history():
    tracker = new_tracker()
    sync_tracker(tracker, [{"name": "intro", "path": "intro.tex"}])
    set_level(tracker, "intro", "middle", reason="revised", date="2026-06-29")
    assert tracker["history"][-1] == {
        "date": "2026-06-29",
        "unit": "intro",
        "from": "low",
        "to": "middle",
        "reason": "revised",
    }


def test_set_level_rejects_bad_level_and_unknown_unit():
    tracker = new_tracker()
    sync_tracker(tracker, [{"name": "intro", "path": "intro.tex"}])
    with pytest.raises(TrackerError):
        set_level(tracker, "intro", "perfect")
    with pytest.raises(TrackerError):
        set_level(tracker, "ghost", "high")


def test_exemplars_orders_high_then_middle_and_excludes_target():
    tracker = new_tracker()
    sync_tracker(
        tracker,
        [
            {"name": "intro", "path": "intro.tex"},
            {"name": "results", "path": "results.tex"},
            {"name": "methods", "path": "methods.tex"},
        ],
    )
    set_level(tracker, "results", "high", date="2026-06-29")
    set_level(tracker, "methods", "middle", date="2026-06-29")
    picks = exemplars(tracker, target="intro")
    assert [p["name"] for p in picks] == ["results", "methods"]
    # The target itself is never an exemplar.
    assert all(p["name"] != "intro" for p in picks)


def test_summarize_counts_levels():
    tracker = new_tracker()
    sync_tracker(tracker, [{"name": "a", "path": "a"}, {"name": "b", "path": "b"}])
    set_level(tracker, "a", "high", date="2026-06-29")
    counts = summarize(tracker)
    assert counts["total"] == 2
    assert counts["high"] == 1
    assert counts["low"] == 1
