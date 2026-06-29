"""Symbol and abbreviation registry with a no-forward-reference linter.

Maintains a single registry of every symbol and abbreviation, the reading-order
point where it is first defined, and checks that nothing is used before it is
defined and that nothing is defined twice.
"""

from __future__ import annotations

from .linter import build_registry, find_definitions, lint_definitions

__all__ = ["lint_definitions", "build_registry", "find_definitions"]
