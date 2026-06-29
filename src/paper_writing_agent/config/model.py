"""The configuration model.

Every author-idiosyncratic choice that the original agent hard-coded is exposed
here as a field with a friendly default. Values are validated on construction so
an invalid config fails fast with a clear message rather than misbehaving later.

The config is grouped into four tables: ``[project]``, ``[style]``, ``[slop]``,
and ``[stats]``. It round-trips to and from TOML via :mod:`.toml_io`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import toml_io

CONFIG_FILENAME = "paper-writing-agent.toml"

# Allowed values. Kept as plain tuples (not enums) so the TOML mapping is a
# trivial string round-trip and validation messages can list the options.
FIELDS = ("computer-science", "software-engineering", "machine-learning", "general")
VENUE_TIERS = ("high-IF", "mid-tier", "workshop", "preprint")
LANGUAGES = ("en", "ja", "zh")
PRINCIPLE_VERBOSITY = ("full", "brief", "off")
PRESETS = ("strict-high-IF", "balanced", "lenient")
SPELLINGS = ("US", "UK")
CITATION_STYLES = ("numeric", "author-year")
SECTION_STRUCTURES = ("methods-supplementary", "methods-extended", "imrad")
FIGURE_REFS = ("full", "abbreviated")
PVALUE_NOTATIONS = ("P-italic-sci", "p-lower-sci", "p-lower-e")
EM_DASH_POLICIES = ("zero", "allow")
HEDGING_STRICTNESS = ("strict", "balanced", "lenient")


class ConfigError(ValueError):
    """Raised when a configuration value is invalid."""


def _check(name: str, value: object, allowed: tuple[str, ...]) -> None:
    if value not in allowed:
        options = ", ".join(allowed)
        raise ConfigError(f"{name}: {value!r} is not valid. Choose one of: {options}.")


@dataclass
class ProjectConfig:
    research_field: str = "computer-science"
    venue_tier: str = "high-IF"
    operating_language: str = "en"
    principle_verbosity: str = "full"
    preset: str = "balanced"

    def __post_init__(self) -> None:
        _check("project.field", self.research_field, FIELDS)
        _check("project.venue_tier", self.venue_tier, VENUE_TIERS)
        _check("project.operating_language", self.operating_language, LANGUAGES)
        _check("project.principle_verbosity", self.principle_verbosity, PRINCIPLE_VERBOSITY)
        _check("project.preset", self.preset, PRESETS)


@dataclass
class StyleConfig:
    spelling: str = "US"
    citation_style: str = "numeric"
    section_structure: str = "methods-supplementary"
    figure_ref: str = "full"

    def __post_init__(self) -> None:
        _check("style.spelling", self.spelling, SPELLINGS)
        _check("style.citation_style", self.citation_style, CITATION_STYLES)
        _check("style.section_structure", self.section_structure, SECTION_STRUCTURES)
        _check("style.figure_ref", self.figure_ref, FIGURE_REFS)


@dataclass
class SlopConfig:
    enabled_tiers: list[int] = field(default_factory=lambda: [1, 2, 3])
    em_dash: str = "zero"
    detect_structural: bool = True
    extra_forbidden: list[str] = field(default_factory=list)
    allow: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        _check("slop.em_dash", self.em_dash, EM_DASH_POLICIES)
        for tier in self.enabled_tiers:
            if tier not in (1, 2, 3):
                raise ConfigError(f"slop.enabled_tiers: {tier!r} is not in {{1, 2, 3}}.")


@dataclass
class StatsConfig:
    pvalue_notation: str = "P-italic-sci"
    significant_figures: int = 2
    require_verdict: bool = True
    test_name_once: bool = True
    thousands_separator: bool = True
    leading_zero: bool = True
    hedging_strictness: str = "balanced"

    def __post_init__(self) -> None:
        _check("stats.pvalue_notation", self.pvalue_notation, PVALUE_NOTATIONS)
        _check("stats.hedging_strictness", self.hedging_strictness, HEDGING_STRICTNESS)
        if not 1 <= self.significant_figures <= 6:
            raise ConfigError("stats.significant_figures: must be between 1 and 6.")


@dataclass
class Config:
    project: ProjectConfig = field(default_factory=ProjectConfig)
    style: StyleConfig = field(default_factory=StyleConfig)
    slop: SlopConfig = field(default_factory=SlopConfig)
    stats: StatsConfig = field(default_factory=StatsConfig)

    # --- serialization ---------------------------------------------------- #
    def to_dict(self) -> dict[str, object]:
        return {
            "project": {
                "field": self.project.research_field,
                "venue_tier": self.project.venue_tier,
                "operating_language": self.project.operating_language,
                "principle_verbosity": self.project.principle_verbosity,
                "preset": self.project.preset,
            },
            "style": {
                "spelling": self.style.spelling,
                "citation_style": self.style.citation_style,
                "section_structure": self.style.section_structure,
                "figure_ref": self.style.figure_ref,
            },
            "slop": {
                "enabled_tiers": list(self.slop.enabled_tiers),
                "em_dash": self.slop.em_dash,
                "detect_structural": self.slop.detect_structural,
                "extra_forbidden": list(self.slop.extra_forbidden),
                "allow": list(self.slop.allow),
            },
            "stats": {
                "pvalue_notation": self.stats.pvalue_notation,
                "significant_figures": self.stats.significant_figures,
                "require_verdict": self.stats.require_verdict,
                "test_name_once": self.stats.test_name_once,
                "thousands_separator": self.stats.thousands_separator,
                "leading_zero": self.stats.leading_zero,
                "hedging_strictness": self.stats.hedging_strictness,
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Config:
        project = dict(data.get("project", {}))  # type: ignore[arg-type]
        style = dict(data.get("style", {}))  # type: ignore[arg-type]
        slop = dict(data.get("slop", {}))  # type: ignore[arg-type]
        stats = dict(data.get("stats", {}))  # type: ignore[arg-type]
        return cls(
            project=ProjectConfig(
                research_field=project.get("field", "computer-science"),
                venue_tier=project.get("venue_tier", "high-IF"),
                operating_language=project.get("operating_language", "en"),
                principle_verbosity=project.get("principle_verbosity", "full"),
                preset=project.get("preset", "balanced"),
            ),
            style=StyleConfig(
                spelling=style.get("spelling", "US"),
                citation_style=style.get("citation_style", "numeric"),
                section_structure=style.get("section_structure", "methods-supplementary"),
                figure_ref=style.get("figure_ref", "full"),
            ),
            slop=SlopConfig(
                enabled_tiers=list(slop.get("enabled_tiers", [1, 2, 3])),
                em_dash=slop.get("em_dash", "zero"),
                detect_structural=slop.get("detect_structural", True),
                extra_forbidden=list(slop.get("extra_forbidden", [])),
                allow=list(slop.get("allow", [])),
            ),
            stats=StatsConfig(
                pvalue_notation=stats.get("pvalue_notation", "P-italic-sci"),
                significant_figures=stats.get("significant_figures", 2),
                require_verdict=stats.get("require_verdict", True),
                test_name_once=stats.get("test_name_once", True),
                thousands_separator=stats.get("thousands_separator", True),
                leading_zero=stats.get("leading_zero", True),
                hedging_strictness=stats.get("hedging_strictness", "balanced"),
            ),
        )

    def to_toml(self) -> str:
        header = (
            "paper-writing-agent configuration.\n"
            "Generated by `pwa init`. Every value has a friendly default and is\n"
            "safe to edit by hand. See docs/ for the meaning of each option."
        )
        return toml_io.dumps(self.to_dict(), header=header)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(self.to_toml())

    @classmethod
    def load(cls, path: str) -> Config:
        return cls.from_dict(toml_io.load(path))
