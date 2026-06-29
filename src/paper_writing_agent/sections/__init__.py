"""Section-status tracker.

Tracks the completion level (low / middle / high) of every prose unit in a
manuscript tree, records a change history, and selects the strongest in-project
units as exemplars when drafting a weaker unit.
"""

from __future__ import annotations

from .tracker import (
    LEVELS,
    discover_units,
    exemplars,
    load_tracker,
    new_tracker,
    save_tracker,
    set_level,
    summarize,
    sync_tracker,
)

__all__ = [
    "LEVELS",
    "new_tracker",
    "load_tracker",
    "save_tracker",
    "discover_units",
    "sync_tracker",
    "set_level",
    "exemplars",
    "summarize",
]
