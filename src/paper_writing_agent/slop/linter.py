"""The anti-AI-slop linter engine.

Given text and a configuration, it masks non-prose regions, runs the active rule
set, and returns deterministic :class:`Finding` records (sorted by position).
The matched snippet is always read from the original text so reports show what
the author actually wrote.
"""

from __future__ import annotations

import os
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from ..config import Config, load_config
from .masking import detect_file_type, mask_regions
from .rules import Rule, build_rules

__all__ = ["Finding", "lint_text", "lint_file", "lint_paths", "default_extensions"]

_DEFAULT_EXTENSIONS = (".md", ".markdown", ".tex", ".latex", ".ltx")
_SNIPPET_MAX = 80


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    col: int
    rule_id: str
    category: str
    severity: str
    matched: str
    message: str
    suggestion: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "line": self.line,
            "col": self.col,
            "rule_id": self.rule_id,
            "category": self.category,
            "severity": self.severity,
            "matched": self.matched,
            "message": self.message,
            "suggestion": self.suggestion,
        }


def default_extensions() -> tuple[str, ...]:
    return _DEFAULT_EXTENSIONS


def _rules_for(config: Config) -> list[Rule]:
    return build_rules(
        enabled_tiers=tuple(config.slop.enabled_tiers),
        detect_structural=config.slop.detect_structural,
        em_dash=config.slop.em_dash,
        extra_forbidden=tuple(config.slop.extra_forbidden),
    )


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            starts.append(index + 1)
    return starts


def _locate(line_starts: list[int], offset: int) -> tuple[int, int]:
    # Binary search for the last line start <= offset.
    low, high = 0, len(line_starts) - 1
    while low < high:
        mid = (low + high + 1) // 2
        if line_starts[mid] <= offset:
            low = mid
        else:
            high = mid - 1
    return low + 1, offset - line_starts[low] + 1


def lint_text(
    text: str,
    *,
    path: str = "<text>",
    config: Config | None = None,
    rules: Sequence[Rule] | None = None,
) -> list[Finding]:
    config = config or load_config()
    rules = rules if rules is not None else _rules_for(config)
    allow = {word.lower() for word in config.slop.allow}

    file_type = detect_file_type(path)
    masked = mask_regions(text, file_type)
    line_starts = _line_starts(text)

    findings: list[Finding] = []
    for rule in rules:
        for match in rule.pattern.finditer(masked):
            start, end = match.span()
            snippet = text[start:end]
            if snippet.strip().lower() in allow:
                continue
            if len(snippet) > _SNIPPET_MAX:
                snippet = snippet[:_SNIPPET_MAX].rstrip() + "..."
            line, col = _locate(line_starts, start)
            findings.append(
                Finding(
                    path=path,
                    line=line,
                    col=col,
                    rule_id=rule.id,
                    category=rule.category,
                    severity=rule.severity,
                    matched=snippet,
                    message=rule.message,
                    suggestion=rule.suggestion,
                )
            )

    findings.sort(key=lambda f: (f.line, f.col, f.rule_id))
    return findings


def lint_file(path: str, *, config: Config | None = None) -> list[Finding]:
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    return lint_text(text, path=path, config=config)


def _iter_files(paths: Iterable[str], extensions: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    for entry in paths:
        if os.path.isdir(entry):
            for root, _dirs, files in os.walk(entry):
                for name in sorted(files):
                    if name.lower().endswith(extensions):
                        found.append(os.path.join(root, name))
        elif os.path.isfile(entry):
            found.append(entry)
    return found


def lint_paths(
    paths: Sequence[str],
    *,
    config: Config | None = None,
    extensions: tuple[str, ...] = _DEFAULT_EXTENSIONS,
) -> list[Finding]:
    config = config or load_config()
    rules = _rules_for(config)
    findings: list[Finding] = []
    for file_path in _iter_files(paths, extensions):
        with open(file_path, encoding="utf-8") as handle:
            text = handle.read()
        findings.extend(lint_text(text, path=file_path, config=config, rules=rules))
    return findings
