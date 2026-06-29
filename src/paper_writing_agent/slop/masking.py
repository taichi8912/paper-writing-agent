"""Mask non-prose regions so the linter never fires inside code or math.

We blank out fenced/inline code, math, LaTeX verbatim environments, comments,
and reference-command arguments by replacing those spans with spaces. Lengths
and newlines are preserved, so a match offset in the masked text maps back to the
same offset in the original text; the linter reports the original snippet.
"""

from __future__ import annotations

import re

__all__ = ["FileType", "detect_file_type", "mask_regions"]

FileType = str  # "markdown" | "latex"

_LATEX_EXTENSIONS = (".tex", ".latex", ".ltx", ".sty", ".cls")

# Shared: dollar math appears in both Markdown and LaTeX.
_MATH = [
    re.compile(r"\$\$.*?\$\$", re.DOTALL),
    re.compile(r"(?<!\\)\$[^$\n]*\$"),
]

_MARKDOWN = [
    re.compile(r"```.*?```", re.DOTALL),
    re.compile(r"~~~.*?~~~", re.DOTALL),
    re.compile(r"`[^`\n]*`"),
    *_MATH,
]

_LATEX_ENVS = "|".join(
    ("verbatim", "lstlisting", "minted", "equation", "align", "gather", "multline", "eqnarray")
)
_LATEX = [
    re.compile(r"(?<!\\)%[^\n]*"),  # comment to end of line
    re.compile(rf"\\begin\{{(?:{_LATEX_ENVS})\*?\}}.*?\\end\{{(?:{_LATEX_ENVS})\*?\}}", re.DOTALL),
    re.compile(r"\\verb\*?(\W).*?\1"),
    re.compile(r"\\\[.*?\\\]", re.DOTALL),
    re.compile(r"\\\(.*?\\\)", re.DOTALL),
    re.compile(
        r"\\(?:cite[a-zA-Z]*|ref|eqref|label|includegraphics|url|href|input|include"
        r"|bibliography|usepackage|documentclass)\s*(?:\[[^\]]*\])?\{[^}]*\}"
    ),
    *_MATH,
]


def detect_file_type(path: str) -> FileType:
    lower = path.lower()
    return "latex" if lower.endswith(_LATEX_EXTENSIONS) else "markdown"


def _blank(span: str) -> str:
    # Preserve newlines so line numbers stay correct; blank everything else.
    return "".join("\n" if ch == "\n" else " " for ch in span)


def mask_regions(text: str, file_type: FileType) -> str:
    patterns = _LATEX if file_type == "latex" else _MARKDOWN
    chars = list(text)
    for pattern in patterns:
        for match in pattern.finditer(text):
            start, end = match.span()
            for index in range(start, end):
                if chars[index] != "\n":
                    chars[index] = " "
    return "".join(chars)
