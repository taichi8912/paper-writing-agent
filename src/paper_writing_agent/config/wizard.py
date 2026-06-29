"""The interactive ``init`` wizard.

The wizard asks a short series of questions, each with a friendly default, and
returns a :class:`Config`. It starts from a preset, then overrides the handful
of fields a newcomer cares about most. When input is not interactive (no TTY) or
``assume_yes`` is set, it returns the chosen preset unchanged so the same code
path works in scripts and CI.
"""

from __future__ import annotations

import sys

from .model import (
    CITATION_STYLES,
    FIELDS,
    LANGUAGES,
    VENUE_TIERS,
    Config,
)
from .presets import PRESET_NAMES, get_preset

__all__ = ["run_wizard"]


def run_wizard(*, assume_yes: bool = False, preset: str = "balanced") -> Config:
    """Run the wizard and return a configured :class:`Config`."""
    interactive = sys.stdin.isatty() and not assume_yes
    if not interactive:
        return get_preset(preset)

    print("paper-writing-agent setup")
    print("Answer a few questions, or press Enter to accept the default.\n")

    chosen_preset = _ask_choice("Strictness preset", PRESET_NAMES, preset)
    config = get_preset(chosen_preset)

    config.project.research_field = _ask_choice(
        "Target field", FIELDS, config.project.research_field
    )
    config.project.venue_tier = _ask_choice(
        "Target venue tier", VENUE_TIERS, config.project.venue_tier
    )
    config.style.citation_style = _ask_choice(
        "Citation style", CITATION_STYLES, config.style.citation_style
    )
    config.style.spelling = _ask_choice("Spelling", ("US", "UK"), config.style.spelling)
    config.project.operating_language = _ask_choice(
        "Operating language", LANGUAGES, config.project.operating_language
    )

    # Re-validate the assembled configuration.
    return Config.from_dict(config.to_dict())


def _ask_choice(label: str, options: tuple[str, ...], default: str) -> str:
    rendered = ", ".join(options)
    while True:
        answer = input(f"{label} [{rendered}] ({default}): ").strip()
        if not answer:
            return default
        if answer in options:
            return answer
        print(f"  '{answer}' is not one of: {rendered}. Try again.")
