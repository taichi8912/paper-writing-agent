"""Tests for the configuration model, presets, and loader."""

from __future__ import annotations

import pytest

from paper_writing_agent.config import (
    CONFIG_FILENAME,
    Config,
    ConfigError,
    find_config_path,
    get_preset,
    load_config,
)
from paper_writing_agent.config.presets import PRESET_NAMES


def test_default_config_is_valid():
    config = Config()
    assert config.project.research_field == "computer-science"
    assert config.style.spelling == "US"
    assert config.slop.em_dash == "zero"
    assert config.stats.require_verdict is True


def test_toml_roundtrip_preserves_values():
    original = get_preset("strict-high-IF")
    restored = Config.from_dict(original.to_dict())
    assert restored.to_dict() == original.to_dict()


@pytest.mark.parametrize("name", PRESET_NAMES)
def test_presets_build_and_validate(name):
    config = get_preset(name)
    assert config.project.preset == name
    # Round-tripping a preset through TOML text must reproduce it.
    assert Config.from_dict(config.to_dict()).to_dict() == config.to_dict()


def test_lenient_relaxes_rules():
    lenient = get_preset("lenient")
    assert lenient.slop.enabled_tiers == [1]
    assert lenient.slop.em_dash == "allow"
    assert lenient.slop.detect_structural is False


def test_strict_enables_everything():
    strict = get_preset("strict-high-IF")
    assert strict.slop.enabled_tiers == [1, 2, 3]
    assert strict.slop.em_dash == "zero"
    assert strict.stats.hedging_strictness == "strict"


def test_invalid_value_raises_with_helpful_message():
    with pytest.raises(ConfigError) as excinfo:
        Config.from_dict({"style": {"spelling": "Australian"}})
    assert "spelling" in str(excinfo.value)
    assert "US" in str(excinfo.value)


def test_invalid_significant_figures_raises():
    with pytest.raises(ConfigError):
        Config.from_dict({"stats": {"significant_figures": 99}})


def test_save_and_load_file(tmp_path):
    path = tmp_path / CONFIG_FILENAME
    get_preset("balanced").save(str(path))
    loaded = Config.load(str(path))
    assert loaded.project.preset == "balanced"


def test_find_config_searches_parents(tmp_path):
    (tmp_path / CONFIG_FILENAME).write_text(get_preset("balanced").to_toml(), encoding="utf-8")
    nested = tmp_path / "a" / "b"
    nested.mkdir(parents=True)
    assert find_config_path(str(nested)) == str(tmp_path / CONFIG_FILENAME)


def test_load_config_falls_back_to_balanced(tmp_path):
    # No config anywhere under an isolated dir -> balanced preset.
    config = load_config(str(tmp_path))
    assert config.project.preset == "balanced"
