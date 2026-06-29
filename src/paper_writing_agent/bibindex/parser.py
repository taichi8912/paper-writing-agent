"""A small, dependency-free BibTeX parser.

Handles the constructs that appear in real bibliographies: ``@type{key, ...}``
entries with brace- or quote-delimited values, nested braces, and authors joined
by `` and ``. ``@string``/``@comment``/``@preamble`` are skipped. The parser is
forgiving: a malformed entry is skipped rather than aborting the whole file.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

__all__ = ["BibEntry", "parse_bibtex", "find_duplicate_keys"]

_IGNORED_TYPES = {"string", "comment", "preamble"}
_VENUE_FIELDS = ("journal", "booktitle", "publisher", "school", "institution", "howpublished")


@dataclass
class BibEntry:
    key: str
    entry_type: str
    fields: dict[str, str] = field(default_factory=dict)

    def title(self) -> str:
        return _clean(self.fields.get("title", ""))

    def year(self) -> str:
        return _clean(self.fields.get("year", ""))

    def doi(self) -> str:
        return _clean(self.fields.get("doi", ""))

    def url(self) -> str:
        return _clean(self.fields.get("url", ""))

    def venue(self) -> str:
        for name in _VENUE_FIELDS:
            if name in self.fields:
                return _clean(self.fields[name])
        return ""

    def authors(self) -> list[str]:
        raw = self.fields.get("author", "")
        if not raw:
            return []
        parts = re.split(r"\s+and\s+", _clean(raw))
        return [_short_author(p) for p in parts if p.strip()]


def parse_bibtex(text: str) -> list[BibEntry]:
    entries: list[BibEntry] = []
    index = 0
    length = len(text)
    while True:
        at = text.find("@", index)
        if at == -1:
            break
        cursor = at + 1
        while cursor < length and text[cursor].isalpha():
            cursor += 1
        entry_type = text[at + 1 : cursor].lower()
        while cursor < length and text[cursor] in " \t\r\n":
            cursor += 1
        if cursor >= length or text[cursor] != "{":
            index = at + 1
            continue
        body, after = _read_braced(text, cursor)
        index = after
        if entry_type in _IGNORED_TYPES:
            continue
        entry = _parse_entry_body(entry_type, body)
        if entry is not None:
            entries.append(entry)
    return entries


def find_duplicate_keys(entries: list[BibEntry]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for entry in entries:
        if entry.key in seen and entry.key not in duplicates:
            duplicates.append(entry.key)
        seen.add(entry.key)
    return duplicates


# --------------------------------------------------------------------------- #
# internals
# --------------------------------------------------------------------------- #
def _read_braced(text: str, open_index: int) -> tuple[str, int]:
    """Read a brace-balanced block starting at ``open_index`` ('{'); return (inner, after)."""
    depth = 0
    cursor = open_index
    length = len(text)
    while cursor < length:
        char = text[cursor]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : cursor], cursor + 1
        cursor += 1
    return text[open_index + 1 :], length


def _parse_entry_body(entry_type: str, body: str) -> BibEntry | None:
    parts = _split_top_level(body, ",")
    if not parts:
        return None
    key = parts[0].strip()
    if not key:
        return None
    fields: dict[str, str] = {}
    for chunk in parts[1:]:
        if "=" not in chunk:
            continue
        name, _, value = chunk.partition("=")
        name = name.strip().lower()
        if name:
            fields[name] = _unwrap_value(value.strip())
    return BibEntry(key=key, entry_type=entry_type, fields=fields)


def _split_top_level(text: str, separator: str) -> list[str]:
    parts: list[str] = []
    buffer: list[str] = []
    depth = 0
    in_quote = False
    for char in text:
        if char == '"' and depth == 0:
            in_quote = not in_quote
            buffer.append(char)
        elif char == "{":
            depth += 1
            buffer.append(char)
        elif char == "}":
            depth = max(0, depth - 1)
            buffer.append(char)
        elif char == separator and depth == 0 and not in_quote:
            parts.append("".join(buffer))
            buffer = []
        else:
            buffer.append(char)
    if buffer:
        parts.append("".join(buffer))
    return parts


def _unwrap_value(value: str) -> str:
    value = value.strip()
    if value.startswith("{") and value.endswith("}"):
        return value[1:-1].strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].strip()
    return value


def _clean(value: str) -> str:
    """Collapse whitespace and strip the most common LaTeX brace/escape noise."""
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value)
    value = value.replace("{", "").replace("}", "")
    return value.strip()


def _short_author(name: str) -> str:
    """Normalize an author to a short 'Last' (or 'Last, First') form."""
    name = _clean(name)
    if "," in name:
        last = name.split(",", 1)[0].strip()
        return last
    tokens = name.split()
    return tokens[-1] if tokens else name
