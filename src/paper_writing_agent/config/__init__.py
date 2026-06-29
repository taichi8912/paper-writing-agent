"""Configuration model, presets, and the interactive ``init`` wizard.

The configuration layer is the public-tool delta from the original agent: every
author-idiosyncratic choice that was hard-coded in the source agent is exposed
here as a friendly default that the user can override.
"""

from __future__ import annotations

import os

from .model import CONFIG_FILENAME, Config, ConfigError
from .presets import PRESET_NAMES, get_preset
from .wizard import run_wizard

__all__ = [
    "CONFIG_FILENAME",
    "Config",
    "ConfigError",
    "PRESET_NAMES",
    "get_preset",
    "run_wizard",
    "find_config_path",
    "load_config",
]


def find_config_path(start: str = ".") -> str | None:
    """Search ``start`` and its parents for a config file; return its path or None."""
    current = os.path.abspath(start)
    while True:
        candidate = os.path.join(current, CONFIG_FILENAME)
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def load_config(start: str = ".") -> Config:
    """Load the nearest config, or return the ``balanced`` preset if none exists.

    Running with no config is intentionally valid: the tool behaves like the
    ``balanced`` preset so it is useful before ``pwa init`` is ever run.
    """
    path = find_config_path(start)
    if path is None:
        return get_preset("balanced")
    return Config.load(path)
