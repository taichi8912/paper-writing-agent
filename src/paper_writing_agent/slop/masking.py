"""Mask non-prose regions so a linter never fires inside code or math.

We blank out fenced/inline code, math, LaTeX verbatim environments, comments,
and reference-command arguments by replacing those spans with spaces. Lengths
and newlines are preserved, so a match offset in the masked text maps back to the
same offset in the original text; the linter reports the original snippet.

``mask_math`` is configurable: the anti-slop linter masks math, but the
statistical-honesty linter keeps it, because in LaTeX a P-value usually lives
inside ``$...$``.
"""

from __future__ import annotations

import re

__all__ = ["FileType", "detect_file_type", "mask_regions"]

FileType = str  # "markdown" | "latex"

_LATEX_EXTENSIONS = (".tex", ".latex", ".ltx", ".sty", ".cls")

# Dollar math appears in both Markdown and LaTeX.
_MATH = [
    re.compile(r"\$\$.*?\$\$", re.DOTALL),
    re.compile(r"(?<!\\)\$[^$\n]*\$"),
]

_MARKDOWN_CODE = [
    re.compile(r"```.*?```", re.DOTALL),
    re.compile(r"~~~.*?~~~", re.DOTALL),
    re.compile(r"`[^`\n]*`"),
]

_LATEX_MATH_ENVS = "|".join(("equation", "align", "gather", "multline", "eqnarray"))
_LATEX_VERBATIM_ENVS = "|".join(("verbatim", "lstlisting", "minted"))

_LATEX_CODE = [
    re.compile(r"(?<!\\)%[^\n]*"),  # comment to end of line
    re.compile(
        rf"\\begin\{{(?:{_LATEX_VERBATIM_ENVS})\*?\}}.*?\\end\{{(?:{_LATEX_VERBATIM_ENVS})\*?\}}",
        re.DOTALL,
    ),
    re.compile(r"\\verb\*?(\W).*?\1"),
    re.compile(
        r"\\(?:cite[a-zA-Z]*|ref|eqref|label|includegraphics|url|href|input|include"
        r"|bibliography|usepackage|documentclass)\s*(?:\[[^\]]*\])?\{[^}]*\}"
    ),
]

_LATEX_MATH = [
    re.compile(r"\\\[.*?\\\]", re.DOTALL),
    re.compile(r"\\\(.*?\\\)", re.DOTALL),
    re.compile(
        rf"\\begin\{{(?:{_LATEX_MATH_ENVS})\*?\}}.*?\\end\{{(?:{_LATEX_MATH_ENVS})\*?\}}",
        re.DOTALL,
    ),
    *_MATH,
]


def detect_file_type(path: str) -> FileType:
    lower = path.lower()
    return "latex" if lower.endswith(_LATEX_EXTENSIONS) else "markdown"


def mask_regions(text: str, file_type: FileType, *, mask_math: bool = True) -> str:
    if file_type == "latex":
        patterns = list(_LATEX_CODE)
        if mask_math:
            patterns += _LATEX_MATH
    else:
        patterns = list(_MARKDOWN_CODE)
        if mask_math:
            patterns += _MATH
    chars = list(text)
    for pattern in patterns:
        for match in pattern.finditer(text):
            for index in range(*match.span()):
                if chars[index] != "\n":
                    chars[index] = " "
    return "".join(chars)
