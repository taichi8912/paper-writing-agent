"""The anti-AI-slop rule catalogue.

Three vocabulary tiers plus structural patterns. The catalogue is generic and
domain-agnostic; every illustrative message uses a computer-science or
software-engineering example rather than any specific paper.

Tiers
-----
- Tier 1 (error): strong AI-pattern markers and unscientific self-praise.
- Tier 2 (warning): words better replaced with a precise alternative.
- Tier 3 (error): filler phrases and AI opening/closing formulas.
- Structural (warning): em dashes, copula avoidance, participle padding, and
  negative parallelism.

A :class:`Rule` is a compiled pattern plus metadata. Vocabulary patterns use
``\\b`` word boundaries and are case-insensitive; the reported snippet comes from
the original (unmasked) text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = ["Rule", "build_rules"]


@dataclass(frozen=True)
class Rule:
    id: str
    category: str  # "tier1" | "tier2" | "tier3" | "structural"
    severity: str  # "error" | "warning"
    pattern: re.Pattern[str]
    message: str
    suggestion: str | None
    tier: int | None = None


def _word(stem: str) -> re.Pattern[str]:
    """Case-insensitive whole-word(s) pattern; ``stem`` may include a regex group."""
    return re.compile(rf"\b{stem}\b", re.IGNORECASE)


def _phrase(text: str) -> re.Pattern[str]:
    """Case-insensitive phrase pattern with flexible internal whitespace."""
    parts = [re.escape(token) for token in text.split()]
    return re.compile(r"\b" + r"\s+".join(parts) + r"\b", re.IGNORECASE)


# --------------------------------------------------------------------------- #
# Tier 1: forbidden (strong AI markers / unscientific self-praise)
# --------------------------------------------------------------------------- #
# stem regex -> (suggestion, short why)
_TIER1: dict[str, tuple[str, str]] = {
    r"delv(?:e|es|ed|ing)": ("examine, study", "strong AI marker"),
    r"underscor(?:e|es|ed|ing)": ("show, indicate", "non-academic emphasis"),
    r"showcas(?:e|es|ed|ing)": ("present, demonstrate", "non-academic emphasis"),
    r"unveil(?:s|ed|ing)?": ("present, introduce", "non-academic emphasis"),
    r"meticulous(?:ly)?": ("careful, systematic", "subjective self-praise"),
    r"intrica(?:te|cies)": ("complex, detailed", "subjective"),
    r"commendable": ("(remove)", "subjective self-praise"),
    r"pivotal": ("central, important", "subjective"),
    r"tapestry": ("(rephrase concretely)", "metaphor"),
    r"realm": ("field, area", "metaphor"),
    r"symphony": ("(rephrase concretely)", "metaphor"),
    r"prov(?:e|es|ed|en)": ("show, demonstrate", "science does not prove"),
    r"groundbreaking": ("(remove; let results speak)", "self-praise"),
    r"impressive": ("(remove; report the number)", "self-praise"),
    r"remarkable": ("notable, substantial", "self-praise without a test"),
    r"novel": ("new (or name the specific contribution)", "self-praise; reader judges"),
    r"a testament to": ("evidence for, demonstrates", "non-academic"),
}

# --------------------------------------------------------------------------- #
# Tier 2: replace with a precise alternative
# --------------------------------------------------------------------------- #
_TIER2: dict[str, str] = {
    r"leverag(?:e|es|ed|ing)": "use, employ",
    r"utiliz(?:e|es|ed|ing)": "use",
    r"robust": "reliable, stable, sound",
    r"comprehensive": "thorough, complete, detailed",
    r"nuanced": "subtle, refined",
    r"multifaceted": "complex, diverse",
    r"landscape": "field, domain, area",
    r"foster(?:s|ed|ing)?": "promote, encourage",
    r"streamlin(?:e|es|ed|ing)": "simplify, optimize",
    r"facilitat(?:e|es|ed|ing)": "enable, allow",
    r"enhanc(?:e|es|ed|ing)": "improve, increase",
    r"tailor(?:s|ed|ing)?": "adapt, customize",
    r"harness(?:es|ed|ing)?": "use, apply",
    r"seamless(?:ly)?": "smooth, integrated",
    r"empower(?:s|ed|ing)?": "enable",
    r"synerg(?:y|ies|istic)": "combined effect, integration",
    r"crucial(?:ly)?": "critical, vital",
    r"transformative": "major, substantial",
    r"navigat(?:e|es|ed|ing)": "address, handle",
    r"vibrant": "active (or rephrase)",
    r"via": "through, by means of",
    r"linked to": "associated with",
    r"yield(?:s|ed|ing)?": "produce, provide, generate",
}

# --------------------------------------------------------------------------- #
# Tier 3: forbidden filler phrases / AI formulas
# --------------------------------------------------------------------------- #
_TIER3: dict[str, str] = {
    "due to the fact that": "because, since",
    "in spite of the fact that": "although, despite",
    "it is important to note that": "(delete; state it directly)",
    "it is interesting to note that": "notably (or delete)",
    "it is worth noting that": "notably (or delete)",
    "in order to": "to",
    "in the ever-evolving landscape of": "(state the point directly)",
    "let's explore": "we examine",
    "we can see that": "the results show",
    "the future looks bright": "(state concrete next steps)",
    "paving the way for": "(state the concrete enabling result)",
    "a step in the right direction": "(state the measured improvement)",
    "plays a vital role": "(state what it does)",
    "plays a crucial role": "(state what it does)",
    "plays a key role": "(state what it does)",
    "plays a significant role": "(state what it does)",
}

# --------------------------------------------------------------------------- #
# Structural patterns
# --------------------------------------------------------------------------- #
_PARTICIPLE_WATCH = (
    "highlighting|underscoring|emphasizing|showcasing|reflecting|symbolizing|"
    "demonstrating|suggesting|ensuring|prompting|cultivating|fostering|paving"
)

_STRUCTURAL: list[tuple[str, str, re.Pattern[str], str, str | None]] = [
    (
        "struct.copula-avoidance",
        "warning",
        re.compile(r"\b(serves as|stands as|acts as)\b", re.IGNORECASE),
        "copula avoidance; prefer a plain 'is/are'",
        "is, are",
    ),
    (
        "struct.role-inflation",
        "warning",
        re.compile(r"\bplays?\s+an?\s+\w+\s+role\b", re.IGNORECASE),
        "inflated 'plays a ... role' construction; state what it does",
        None,
    ),
    (
        "struct.participle-padding",
        "warning",
        re.compile(rf",\s+(?:{_PARTICIPLE_WATCH})\b", re.IGNORECASE),
        "trailing participle padding; use an explicit connective or a new sentence",
        "therefore, thus, accordingly",
    ),
    (
        "struct.negative-parallelism",
        "warning",
        re.compile(r"\bnot only\b.*?\bbut also\b", re.IGNORECASE | re.DOTALL),
        "negative parallelism; state the points plainly",
        None,
    ),
    (
        "struct.beyond-transition",
        "warning",
        re.compile(r"(?m)^\s*Beyond\b"),
        "informal 'Beyond ...' opener; prefer 'In addition to ...'",
        "In addition to",
    ),
]

_EM_DASH = Rule(
    id="struct.em-dash",
    category="structural",
    severity="error",
    pattern=re.compile(r"—"),
    message="em dash is a strong AI marker; replace with commas, parentheses, or a period",
    suggestion=", or ( ) or .",
    tier=None,
)


def build_rules(
    *,
    enabled_tiers: tuple[int, ...] = (1, 2, 3),
    detect_structural: bool = True,
    em_dash: str = "zero",
    extra_forbidden: tuple[str, ...] = (),
) -> list[Rule]:
    """Assemble the active rule set for the given configuration."""
    rules: list[Rule] = []

    if 1 in enabled_tiers:
        for stem, (suggestion, why) in _TIER1.items():
            label = _label(stem)
            rules.append(
                Rule(
                    id=f"tier1.{label}",
                    category="tier1",
                    severity="error",
                    pattern=_word(stem),
                    message=f"Tier-1 forbidden word ({why}).",
                    suggestion=suggestion,
                    tier=1,
                )
            )
        for word in extra_forbidden:
            rules.append(
                Rule(
                    id=f"tier1.custom.{word.lower()}",
                    category="tier1",
                    severity="error",
                    pattern=_word(re.escape(word)),
                    message="Project-defined forbidden word.",
                    suggestion=None,
                    tier=1,
                )
            )

    if 2 in enabled_tiers:
        for stem, suggestion in _TIER2.items():
            rules.append(
                Rule(
                    id=f"tier2.{_label(stem)}",
                    category="tier2",
                    severity="warning",
                    pattern=_word(stem),
                    message="Tier-2 word; replace with a precise alternative.",
                    suggestion=suggestion,
                    tier=2,
                )
            )

    if 3 in enabled_tiers:
        for phrase, suggestion in _TIER3.items():
            rules.append(
                Rule(
                    id=f"tier3.{_slug(phrase)}",
                    category="tier3",
                    severity="error",
                    pattern=_phrase(phrase),
                    message="Tier-3 filler phrase.",
                    suggestion=suggestion,
                    tier=3,
                )
            )

    if em_dash == "zero":
        rules.append(_EM_DASH)

    if detect_structural:
        for rule_id, severity, pattern, message, suggestion in _STRUCTURAL:
            rules.append(
                Rule(
                    id=rule_id,
                    category="structural",
                    severity=severity,
                    pattern=pattern,
                    message=message,
                    suggestion=suggestion,
                    tier=None,
                )
            )

    return rules


def _label(stem: str) -> str:
    """Derive a short, stable id fragment from a regex stem."""
    base = re.split(r"[^a-zA-Z]", stem, maxsplit=1)[0]
    return base.lower() or "word"


def _slug(phrase: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", phrase.lower()).strip("-")
