"""The statistical-honesty linter.

Checks that statistics are reported the way a careful reviewer expects:

- every reported P-value carries an explicit significance verdict nearby;
- a statistical test is named once, at first occurrence;
- P-value and numeric notation follow the configured house style
  (capitalization, scientific vs e-notation, leading zeros, thousands
  separators, number-unit spacing).

Findings reuse the shared :class:`~paper_writing_agent.slop.linter.Finding` type
so all linters share one report format.
"""

from __future__ import annotations

import re

from ..config import Config, load_config
from ..slop.linter import Finding
from ..slop.masking import detect_file_type, mask_regions

__all__ = ["lint_stats"]

_PVALUE = re.compile(
    r"(?<![A-Za-z])(?P<sym>[Pp])(?:\s*-?\s*values?)?\s*(?P<op>[=<>≤≥])\s*"
    r"(?P<num>\.?\d[\d.]*(?:\s*(?:[eE][+-]?\d+|(?:×|x|\\times)\s*10\s*\^?\s*\{?[-–]?\d+\}?))?)"
)
_VERDICT = re.compile(
    r"\b(?:not\s+significant|non[-\s]?significant|no\s+significant|"
    r"significant(?:ly)?|significance|did\s+not\s+differ|no\s+(?:statistical\s+)?difference)\b"
    r"|\bn\.?s\.?\b",
    re.IGNORECASE,
)
_LEADING_ZERO = re.compile(r"(?<![\d.])\.\d+")
_NUMBER_UNIT = re.compile(r"\b(\d+(?:\.\d+)?)(bp|kb|kbp|Mbp|GB|MB|KB|TB|ms|ns|GHz|MHz|nm)\b")
_BIG_INT = re.compile(r"(?<![\d,.])\d{5,}(?![\d,.])")

# Longest first, so "Welch's t-test" is consumed before "t-test".
_TESTS: list[tuple[str, re.Pattern[str]]] = [
    ("Welch's t-test", re.compile(r"Welch(?:'s)?\s+t-test", re.IGNORECASE)),
    ("Student's t-test", re.compile(r"Student(?:'s)?\s+t-test", re.IGNORECASE)),
    ("Wilcoxon signed-rank test", re.compile(r"Wilcoxon\s+signed[-\s]rank(?:\s+test)?", re.I)),
    ("Wilcoxon rank-sum test", re.compile(r"Wilcoxon\s+rank[-\s]sum(?:\s+test)?", re.I)),
    ("Mann-Whitney U test", re.compile(r"Mann[-\s]Whitney(?:\s+U)?(?:\s+test)?", re.IGNORECASE)),
    ("Kruskal-Wallis test", re.compile(r"Kruskal[-\s]Wallis(?:\s+test)?", re.IGNORECASE)),
    ("Kolmogorov-Smirnov test", re.compile(r"Kolmogorov[-\s]Smirnov(?:\s+test)?", re.IGNORECASE)),
    ("Fisher's exact test", re.compile(r"Fisher(?:'s)?\s+exact\s+test", re.IGNORECASE)),
    ("chi-squared test", re.compile(r"chi[-\s]squared?(?:\s+test)?", re.IGNORECASE)),
    ("t-test", re.compile(r"\bt-test\b", re.IGNORECASE)),
    ("ANOVA", re.compile(r"\bANOVA\b")),
    ("TOST", re.compile(r"\bTOST\b")),
    ("Spearman correlation", re.compile(r"\bSpearman\b", re.IGNORECASE)),
    ("Pearson correlation", re.compile(r"\bPearson\b", re.IGNORECASE)),
]


def lint_stats(
    text: str, *, path: str = "<text>", config: Config | None = None
) -> list[Finding]:
    config = config or load_config()
    stats = config.stats
    file_type = detect_file_type(path)
    # Keep math: in LaTeX, P-values live inside $...$.
    masked = mask_regions(text, file_type, mask_math=False)
    line_starts = _line_starts(text)
    sentences = _sentence_spans(masked)

    findings: list[Finding] = []

    for match in _PVALUE.finditer(masked):
        findings.extend(_check_pvalue(match, masked, sentences, stats, text, line_starts, path))

    if stats.leading_zero:
        for match in _LEADING_ZERO.finditer(masked):
            findings.append(
                _make(text, line_starts, path, match.start(), match.group(0),
                      "stats.leading-zero", "warning",
                      "decimal without a leading zero", "write 0" + match.group(0))
            )

    for match in _NUMBER_UNIT.finditer(masked):
        findings.append(
            _make(text, line_starts, path, match.start(), match.group(0),
                  "stats.number-unit-spacing", "warning",
                  "insert a space between the number and its unit",
                  f"{match.group(1)} {match.group(2)}")
        )

    if stats.thousands_separator:
        for match in _BIG_INT.finditer(masked):
            findings.append(
                _make(text, line_starts, path, match.start(), match.group(0),
                      "stats.thousands-separator", "warning",
                      "large integer without thousands separators", _group_int(match.group(0)))
            )

    if stats.test_name_once:
        findings.extend(_check_test_names(masked, text, line_starts, path))

    findings.sort(key=lambda f: (f.line, f.col, f.rule_id))
    return findings


# --------------------------------------------------------------------------- #
# checks
# --------------------------------------------------------------------------- #
def _check_pvalue(match, masked, sentences, stats, text, line_starts, path) -> list[Finding]:
    out: list[Finding] = []
    start = match.start()
    snippet = text[start : match.end()].strip()
    sym = match.group("sym")
    num = match.group("num")

    if stats.require_verdict and not _has_verdict(masked, sentences, start):
        out.append(
            _make(text, line_starts, path, start, snippet, "stats.pvalue-no-verdict", "error",
                  "P-value without an explicit significance verdict in the same or adjacent sentence",
                  "state whether the comparison is significant (and name the test once)")
        )

    wants_capital = stats.pvalue_notation.startswith("P-")
    if wants_capital and sym == "p":
        out.append(_make(text, line_starts, path, start, snippet, "stats.pvalue-case", "warning",
                         "house style uses a capital, italic P", "P"))
    if not wants_capital and sym == "P":
        out.append(_make(text, line_starts, path, start, snippet, "stats.pvalue-case", "warning",
                         "house style uses a lowercase p", "p"))

    # Match genuine e-notation (digit e digit), not the 'e' inside "\times".
    if stats.pvalue_notation.endswith("-sci") and re.search(r"\d[eE][+-]?\d", num):
        out.append(_make(text, line_starts, path, start, snippet, "stats.pvalue-enotation", "warning",
                         "use scientific notation (x 10^{-k}) rather than e-notation",
                         "e.g. 2.6 x 10^{-5}"))
    return out


def _check_test_names(masked: str, text: str, line_starts, path: str) -> list[Finding]:
    out: list[Finding] = []
    work = list(masked)
    for label, pattern in _TESTS:
        spans = [m.span() for m in pattern.finditer("".join(work))]
        for start, _end in spans[1:]:
            out.append(
                _make(text, line_starts, path, start, text[start:_end], "stats.test-name-repeated",
                      "warning", f"test name '{label}' already introduced; name a test once",
                      "drop the repeated test name")
            )
        for start, end in spans:  # consume so shorter names do not re-match
            for index in range(start, end):
                if work[index] != "\n":
                    work[index] = " "
    return out


def _has_verdict(masked: str, sentences: list[tuple[int, int]], pos: int) -> bool:
    for i, (start, end) in enumerate(sentences):
        if start <= pos < end:
            window = masked[start:end]
            if i > 0:
                prev_start, _prev_end = sentences[i - 1]
                window = masked[prev_start:end]
            return bool(_VERDICT.search(window))
    return bool(_VERDICT.search(masked[max(0, pos - 160) : pos + 160]))


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _line_starts(text: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            starts.append(index + 1)
    return starts


def _locate(line_starts: list[int], offset: int) -> tuple[int, int]:
    low, high = 0, len(line_starts) - 1
    while low < high:
        mid = (low + high + 1) // 2
        if line_starts[mid] <= offset:
            low = mid
        else:
            high = mid - 1
    return low + 1, offset - line_starts[low] + 1


def _sentence_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    for match in re.finditer(r"[.!?](?=\s|$)|\n\s*\n", text):
        spans.append((start, match.end()))
        start = match.end()
    if start < len(text):
        spans.append((start, len(text)))
    return spans


def _make(text, line_starts, path, offset, snippet, rule_id, severity, message, suggestion):
    line, col = _locate(line_starts, offset)
    snippet = snippet if len(snippet) <= 80 else snippet[:80].rstrip() + "..."
    return Finding(
        path=path, line=line, col=col, rule_id=rule_id, category="stats",
        severity=severity, matched=snippet, message=message, suggestion=suggestion,
    )


def _group_int(digits: str) -> str:
    return f"{int(digits):,}"
