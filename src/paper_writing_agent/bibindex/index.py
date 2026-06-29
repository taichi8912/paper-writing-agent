"""Build and merge the bibliography context index.

``build_index`` turns parsed BibTeX entries into a context index whose
bibliographic facts are filled in and whose semantic fields (key findings,
suitable contexts, sample phrases) start in a safe, honest state for an author or
agent to curate. ``merge_index`` adds new keys on regeneration without touching
existing curation.

Nothing here fabricates claims: ``key_findings`` is seeded from the paper's own
title, and entries are marked ``derived`` until grounded or curated.
"""

from __future__ import annotations

from typing import Any

import yaml

from .. import __version__
from .parser import BibEntry, find_duplicate_keys
from .topics import tag_entry

__all__ = ["build_index", "merge_index", "to_yaml", "save_index", "load_index"]

_GENERATOR = f"paper-writing-agent bibindex {__version__}"


def build_index(entries: list[BibEntry], *, source_bib: str) -> dict[str, Any]:
    """Build a fresh context index from parsed BibTeX entries."""
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    for entry in entries:
        if entry.key in seen:
            continue  # keep the first occurrence; duplicates are reported separately
        seen.add(entry.key)
        records.append(_seed_record(entry))

    index = {
        "metadata": {
            "source_bib": source_bib,
            "total_entries": len(entries),
            "unique_keys": len(records),
            "duplicate_keys": find_duplicate_keys(entries),
            "generator": _GENERATOR,
        },
        "topics": _invert_topics(records),
        "entries": records,
    }
    return index


def merge_index(existing: dict[str, Any], fresh: dict[str, Any]) -> dict[str, Any]:
    """Add new entries from ``fresh`` into ``existing`` without altering curation."""
    existing_entries: list[dict[str, Any]] = list(existing.get("entries", []))
    existing_ids = {record["id"] for record in existing_entries}

    added = [record for record in fresh.get("entries", []) if record["id"] not in existing_ids]
    merged_entries = existing_entries + added

    metadata = dict(existing.get("metadata", {}))
    metadata.update(
        {
            "source_bib": fresh.get("metadata", {}).get("source_bib", metadata.get("source_bib")),
            "total_entries": fresh.get("metadata", {}).get("total_entries", len(merged_entries)),
            "unique_keys": len(merged_entries),
            "duplicate_keys": fresh.get("metadata", {}).get("duplicate_keys", []),
            "generator": _GENERATOR,
        }
    )
    return {
        "metadata": metadata,
        "topics": _invert_topics(merged_entries),
        "entries": merged_entries,
    }


def _seed_record(entry: BibEntry) -> dict[str, Any]:
    title = entry.title() or entry.key
    return {
        "id": entry.key,
        "entry_type": entry.entry_type,
        "title": title,
        "authors_short": entry.authors(),
        "year": entry.year(),
        "venue": entry.venue(),
        "doi": entry.doi() or None,
        "url": entry.url() or None,
        "topics": tag_entry(title, entry.venue()),
        "citation_role": "background",
        "available_from_section": "any",
        # Seeded from the paper's own title (a fact, not a fabricated claim).
        "key_findings": title,
        "suitable_contexts": [],
        "sample_phrases": [],
        "author_usage": [],
        "curation_status": "derived",
        "cite_as": f"\\cite{{{entry.key}}}",
    }


def _invert_topics(records: list[dict[str, Any]]) -> dict[str, list[str]]:
    inverted: dict[str, list[str]] = {}
    for record in records:
        for tag in record.get("topics", []):
            inverted.setdefault(tag, []).append(record["id"])
    return {tag: inverted[tag] for tag in sorted(inverted)}


def to_yaml(index: dict[str, Any]) -> str:
    return yaml.safe_dump(index, sort_keys=False, allow_unicode=True, width=100)


def save_index(path: str, index: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(to_yaml(index))


def load_index(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)
