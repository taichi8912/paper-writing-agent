"""Symbol/abbreviation registry and a no-forward-reference linter.

Reading the document in order, this finds where each abbreviation is defined
(the "Long Form (ABBR)" pattern) and flags two defects:

- an abbreviation used before it is defined (forward reference);
- an abbreviation defined more than once (redefinition).

Reading order is the order in which files are passed. This is the generic,
checkable form of the "define once, then use bare" discipline.
"""

from __future__ import annotations

import re

from ..slop.linter import Finding
from ..slop.masking import detect_file_type, mask_regions

__all__ = ["lint_definitions", "build_registry"]

# "Convolutional Neural Network (CNN)" -> long form + acronym.
_DEFINITION = re.compile(r"([A-Z][A-Za-z0-9.\-]*(?:\s+[A-Za-z0-9.\-]+){0,5})\s*\(([A-Z][A-Za-z0-9]{1,7})s?\)")
# Common all-caps tokens that are not abbreviations to define.
_STOPWORDS = {"A", "I", "THE", "AND", "OR", "OF", "IN", "ON", "FOR", "TO", "AI", "OK"}


def _concat(files: list[str]) -> tuple[str, list[tuple[int, str]]]:
    """Concatenate files in reading order; return (text, [(offset, path), ...])."""
    chunks: list[str] = []
    offsets: list[tuple[int, str]] = []
    position = 0
    for path in files:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        offsets.append((position, path))
        chunks.append(text)
        position += len(text) + 1  # +1 for the joining newline
    return "\n".join(chunks), offsets


def _mask_all(text: str) -> str:
    # Mask code and math for both flavors so we never read a definition out of code.
    masked = mask_regions(text, "markdown")
    return mask_regions(masked, "latex")


def _path_for(offsets: list[tuple[int, str]], offset: int) -> str:
    path = offsets[0][1] if offsets else "<text>"
    for start, candidate in offsets:
        if start <= offset:
            path = candidate
        else:
            break
    return path


def _line_col(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    col = offset - (text.rfind("\n", 0, offset) + 1) + 1
    return line, col


def find_definitions(masked: str) -> dict[str, list[int]]:
    definitions: dict[str, list[int]] = {}
    for match in _DEFINITION.finditer(masked):
        acronym = match.group(2)
        if acronym in _STOPWORDS:
            continue
        definitions.setdefault(acronym, []).append(match.start(2))
    return definitions


def lint_definitions(files: list[str]) -> list[Finding]:
    """Lint a sequence of files (in reading order) for definition discipline."""
    text, offsets = _concat(files)
    masked = _mask_all(text)
    definitions = find_definitions(masked)

    findings: list[Finding] = []
    for acronym, def_positions in definitions.items():
        first_def = min(def_positions)

        for extra in sorted(def_positions)[1:]:
            path = _path_for(offsets, extra)
            line, col = _line_col(text, extra)
            findings.append(
                Finding(
                    path=path, line=line, col=col, rule_id="defs.redefinition",
                    category="definitions", severity="warning", matched=acronym,
                    message=f"abbreviation '{acronym}' is defined more than once",
                    suggestion="define once at first use, then use it bare",
                )
            )

        for use in re.finditer(rf"\b{re.escape(acronym)}\b", masked):
            pos = use.start()
            if pos < first_def and pos not in def_positions:
                path = _path_for(offsets, pos)
                line, col = _line_col(text, pos)
                findings.append(
                    Finding(
                        path=path, line=line, col=col, rule_id="defs.forward-reference",
                        category="definitions", severity="error", matched=acronym,
                        message=f"abbreviation '{acronym}' is used before it is defined",
                        suggestion="introduce 'Long Form (ABBR)' at first use",
                    )
                )

    findings.sort(key=lambda f: (f.path, f.line, f.col, f.rule_id))
    return findings


def build_registry(files: list[str]) -> dict[str, object]:
    """Build a registry of abbreviations and where each is first defined."""
    text, offsets = _concat(files)
    masked = _mask_all(text)
    definitions = find_definitions(masked)
    entries = []
    for acronym in sorted(definitions):
        first = min(definitions[acronym])
        line, _col = _line_col(text, first)
        entries.append(
            {
                "abbreviation": acronym,
                "first_defined_in": _path_for(offsets, first),
                "line": line,
                "definitions": len(definitions[acronym]),
            }
        )
    return {"abbreviations": entries}
