"""Author-grounding: learn how citations were actually used in a prior paper.

Scanning a previous manuscript's LaTeX source, this extracts, for each cited key,
the section it appeared in and the sentence around the citation. Folding that into
the index gives the agent verified, real usage to imitate, which is the strongest
defense against citation hallucination: prefer keys the author has actually used,
in the way they used them.
"""

from __future__ import annotations

import re
from typing import Any

__all__ = ["extract_usage", "apply_grounding"]

_CITE = re.compile(
    r"\\(?:cite|citep|citet|citeauthor|citeyear|parencite|textcite|autocite|footcite)\*?"
    r"(?:\[[^\]]*\])*\{([^}]*)\}"
)
_SECTION = re.compile(r"\\(?:chapter|section|subsection|subsubsection)\*?\{([^}]*)\}")
_SENTENCE_BOUND = re.compile(r"[.!?]\s|\n\s*\n")


def extract_usage(text: str) -> dict[str, list[dict[str, str]]]:
    """Return {cite_key: [{'section': ..., 'sentence': ...}, ...]} from a manuscript."""
    sections = [(m.start(), _clean(m.group(1))) for m in _SECTION.finditer(text)]
    usage: dict[str, list[dict[str, str]]] = {}
    for match in _CITE.finditer(text):
        section = _section_at(sections, match.start())
        sentence = _sentence_around(text, match.start(), match.end())
        for key in (k.strip() for k in match.group(1).split(",")):
            if not key:
                continue
            usage.setdefault(key, []).append({"section": section, "sentence": sentence})
    return usage


def apply_grounding(
    index: dict[str, Any],
    usage: dict[str, list[dict[str, str]]],
    *,
    mark_verified: bool = True,
) -> int:
    """Attach usage to matching entries; return the number of entries grounded."""
    grounded = 0
    for entry in index.get("entries", []):
        records = usage.get(entry["id"])
        if not records:
            continue
        entry["author_usage"] = records
        if mark_verified:
            entry["curation_status"] = "verified"
        grounded += 1
    return grounded


def _section_at(sections: list[tuple[int, str]], position: int) -> str:
    current = "unknown"
    for start, title in sections:
        if start <= position:
            current = title
        else:
            break
    return current


def _sentence_around(text: str, start: int, end: int) -> str:
    left = 0
    for match in _SENTENCE_BOUND.finditer(text, 0, start):
        left = match.end()
    right_match = _SENTENCE_BOUND.search(text, end)
    right = right_match.start() + 1 if right_match else len(text)
    return _clean(text[left:right])


def _clean(value: str) -> str:
    value = re.sub(r"\s+", " ", value)
    return value.strip()
