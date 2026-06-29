"""Section-status tracker.

Tracks the completion level of every prose unit in a manuscript: ``low`` (first
draft), ``middle`` (revised and approved), or ``high`` (near-final). It records a
change history and, when drafting a weak unit, points to the strongest in-project
units as exemplars.

Promotion is never automatic. ``set_level`` is an explicit call; the design rule
(pillar 5) is that a unit advances only when the author says so.
"""

from __future__ import annotations

import re
from typing import Any

import yaml

from .. import __version__

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

LEVELS = ("low", "middle", "high")
_LEVEL_RANK = {level: rank for rank, level in enumerate(LEVELS)}

_INCLUDE = re.compile(r"\\(?:input|subfile|include)\{([^}]*)\}")
_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$", re.MULTILINE)


class TrackerError(ValueError):
    """Raised on an invalid tracker operation."""


def new_tracker() -> dict[str, Any]:
    return {"generator": f"paper-writing-agent sections {__version__}", "units": [], "history": []}


def load_tracker(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    data.setdefault("units", [])
    data.setdefault("history", [])
    return data


def save_tracker(path: str, tracker: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(tracker, handle, sort_keys=False, allow_unicode=True, width=100)


def discover_units(path: str) -> list[dict[str, str]]:
    """Enumerate prose units from a LaTeX root (\\input/\\subfile) or a Markdown file."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    if path.lower().endswith((".tex", ".latex", ".ltx")):
        units = []
        for match in _INCLUDE.finditer(text):
            target = match.group(1).strip()
            name = re.sub(r"\.tex$", "", target.rsplit("/", 1)[-1])
            units.append({"name": name, "path": target})
        return units

    units = []
    for match in _HEADING.finditer(text):
        title = match.group(2).strip()
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        units.append({"name": slug or "section", "path": path})
    return units


def sync_tracker(tracker: dict[str, Any], discovered: list[dict[str, str]]) -> dict[str, Any]:
    """Add new units as ``low`` and flag missing ones; keep existing levels."""
    by_name = {unit["name"]: unit for unit in tracker["units"]}
    discovered_names = {unit["name"] for unit in discovered}

    for unit in discovered:
        existing = by_name.get(unit["name"])
        if existing is None:
            tracker["units"].append(
                {"name": unit["name"], "path": unit["path"], "level": "low", "present": True}
            )
        else:
            existing["path"] = unit["path"]
            existing["present"] = True

    for unit in tracker["units"]:
        if unit["name"] not in discovered_names:
            unit["present"] = False

    tracker["units"].sort(key=lambda u: u["name"])
    return tracker


def set_level(
    tracker: dict[str, Any],
    name: str,
    level: str,
    *,
    reason: str = "",
    date: str = "",
) -> dict[str, Any]:
    if level not in LEVELS:
        raise TrackerError(f"level must be one of {LEVELS}, got {level!r}")
    unit = next((u for u in tracker["units"] if u["name"] == name), None)
    if unit is None:
        raise TrackerError(f"unknown unit: {name!r}")
    old = unit.get("level", "low")
    unit["level"] = level
    tracker["history"].append(
        {"date": date, "unit": name, "from": old, "to": level, "reason": reason}
    )
    return tracker


def exemplars(tracker: dict[str, Any], target: str | None = None) -> list[dict[str, str]]:
    """Return units to imitate: all ``high`` then all ``middle``, strongest first."""
    ranked = [
        u
        for u in tracker["units"]
        if u.get("level") in ("high", "middle") and u["name"] != target and u.get("present", True)
    ]
    ranked.sort(key=lambda u: (-_LEVEL_RANK[u["level"]], u["name"]))
    return [{"name": u["name"], "level": u["level"], "path": u.get("path", "")} for u in ranked]


def summarize(tracker: dict[str, Any]) -> dict[str, int]:
    counts = {level: 0 for level in LEVELS}
    for unit in tracker["units"]:
        level = unit.get("level", "low")
        if level in counts:
            counts[level] += 1
    counts["total"] = len(tracker["units"])
    return counts
