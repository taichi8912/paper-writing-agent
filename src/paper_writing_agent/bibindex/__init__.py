"""Bibliography context indexer and validator.

Builds a searchable, schema-validated context index from a BibTeX file so the
agent can select citation keys accurately, and validates the index against an
anti-hallucination schema. Supports merge-preserving regeneration and
author-grounded citation extraction from a prior manuscript.
"""

from __future__ import annotations

from .grounding import apply_grounding, extract_usage
from .index import build_index, load_index, merge_index, save_index, to_yaml
from .parser import BibEntry, find_duplicate_keys, parse_bibtex
from .topics import TOPIC_TAGS, tag_entry
from .validate import ValidationReport, load_schema, validate_index

__all__ = [
    "BibEntry",
    "parse_bibtex",
    "find_duplicate_keys",
    "build_index",
    "merge_index",
    "to_yaml",
    "save_index",
    "load_index",
    "tag_entry",
    "TOPIC_TAGS",
    "validate_index",
    "ValidationReport",
    "load_schema",
    "extract_usage",
    "apply_grounding",
]
