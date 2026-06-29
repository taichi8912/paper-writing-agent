"""Formatters for linter findings (text and JSON) plus a summary count.

Output is deterministic so it can be asserted in tests and diffed in CI. Rich is
used for color when writing to a terminal and available, but the plain text form
is the canonical, color-free representation.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Sequence

from .linter import Finding

__all__ = ["format_text", "format_json", "summarize", "has_errors"]


def summarize(findings: Sequence[Finding]) -> dict[str, int]:
    counts: Counter[str] = Counter(f.severity for f in findings)
    return {
        "total": len(findings),
        "error": counts.get("error", 0),
        "warning": counts.get("warning", 0),
    }


def has_errors(findings: Sequence[Finding]) -> bool:
    return any(f.severity == "error" for f in findings)


def format_text(findings: Sequence[Finding]) -> str:
    if not findings:
        return "No findings."
    lines: list[str] = []
    for finding in findings:
        location = f"{finding.path}:{finding.line}:{finding.col}"
        head = f"{location} [{finding.severity}] {finding.rule_id}: {finding.message}"
        if finding.matched.strip():
            head += f" (found: {finding.matched!r})"
        lines.append(head)
        if finding.suggestion:
            lines.append(f"    -> {finding.suggestion}")
    summary = summarize(findings)
    lines.append("")
    lines.append(
        f"{summary['total']} finding(s): "
        f"{summary['error']} error, {summary['warning']} warning."
    )
    return "\n".join(lines)


def format_json(findings: Sequence[Finding]) -> str:
    payload = {
        "findings": [f.to_dict() for f in findings],
        "summary": summarize(findings),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)
