"""Built-in strictness presets.

A preset is a ready-made :class:`~paper_writing_agent.config.model.Config`. The
``init`` wizard starts from a preset and lets the user override individual
fields, so a newcomer gets sensible behavior without learning every knob.

- ``strict-high-IF``: maximal vigilance. All forbidden-word tiers, zero em
  dashes, structural pattern detection, strict hedging. Use when chasing a
  top-tier venue and you want every AI fingerprint and loose claim flagged.
- ``balanced`` (default): the same rules a careful author would apply, without
  flagging borderline cases. A good day-to-day setting.
- ``lenient``: a light touch. Only the strongest Tier-1 markers and bare
  P-values are flagged; structural heuristics are off. Use for early drafts.
"""

from __future__ import annotations

from .model import Config, ProjectConfig, SlopConfig, StatsConfig, StyleConfig

__all__ = ["PRESET_NAMES", "get_preset"]

PRESET_NAMES = ("strict-high-IF", "balanced", "lenient")


def get_preset(name: str) -> Config:
    """Return a fresh :class:`Config` for the named preset."""
    if name == "strict-high-IF":
        return _strict()
    if name == "balanced":
        return _balanced()
    if name == "lenient":
        return _lenient()
    options = ", ".join(PRESET_NAMES)
    raise ValueError(f"Unknown preset {name!r}. Choose one of: {options}.")


def _strict() -> Config:
    return Config(
        project=ProjectConfig(preset="strict-high-IF"),
        style=StyleConfig(),
        slop=SlopConfig(enabled_tiers=[1, 2, 3], em_dash="zero", detect_structural=True),
        stats=StatsConfig(
            require_verdict=True,
            test_name_once=True,
            significant_figures=2,
            hedging_strictness="strict",
        ),
    )


def _balanced() -> Config:
    return Config(
        project=ProjectConfig(preset="balanced"),
        style=StyleConfig(),
        slop=SlopConfig(enabled_tiers=[1, 2, 3], em_dash="zero", detect_structural=True),
        stats=StatsConfig(
            require_verdict=True,
            test_name_once=True,
            significant_figures=2,
            hedging_strictness="balanced",
        ),
    )


def _lenient() -> Config:
    return Config(
        project=ProjectConfig(preset="lenient"),
        style=StyleConfig(),
        slop=SlopConfig(enabled_tiers=[1], em_dash="allow", detect_structural=False),
        stats=StatsConfig(
            require_verdict=True,
            test_name_once=False,
            significant_figures=3,
            hedging_strictness="lenient",
        ),
    )
