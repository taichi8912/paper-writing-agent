"""Anti-AI-slop linter.

Detects AI-writing fingerprints (forbidden vocabulary tiers, banned phrases,
em dashes, and structural patterns) and proposes precise academic replacements.
"""

from __future__ import annotations

from .linter import Finding, default_extensions, lint_file, lint_paths, lint_text
from .report import format_json, format_text, has_errors, summarize
from .rules import Rule, build_rules

__all__ = [
    "Finding",
    "Rule",
    "build_rules",
    "lint_text",
    "lint_file",
    "lint_paths",
    "default_extensions",
    "format_text",
    "format_json",
    "summarize",
    "has_errors",
]
