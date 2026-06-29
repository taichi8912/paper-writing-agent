"""Scaffold a manuscript workspace from packaged templates.

``pwa init`` copies the template tree (shipped as package data under
``templates/workspace``) into the target directory, substituting ``{{KEY}}``
placeholders from the resolved configuration. Existing files are never
overwritten unless ``overwrite`` is set, so re-running ``init`` is safe.
"""

from __future__ import annotations

import os
from importlib import resources

from .config import Config

__all__ = ["scaffold_workspace", "placeholders"]


def placeholders(config: Config) -> dict[str, str]:
    return {
        "FIELD": config.project.research_field,
        "VENUE_TIER": config.project.venue_tier,
        "PRESET": config.project.preset,
        "LANGUAGE": config.project.operating_language,
        "SPELLING": config.style.spelling,
        "CITATION_STYLE": config.style.citation_style,
        "SECTION_STRUCTURE": config.style.section_structure,
        "FIGURE_REF": config.style.figure_ref,
        "PVALUE_NOTATION": config.stats.pvalue_notation,
    }


def _iter_templates(node, prefix: str = ""):
    for child in node.iterdir():
        relative = f"{prefix}{child.name}"
        if child.is_dir():
            yield from _iter_templates(child, relative + "/")
        else:
            yield relative, child.read_text(encoding="utf-8")


def _substitute(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def scaffold_workspace(
    target_dir: str, config: Config, *, overwrite: bool = False
) -> list[str]:
    """Write the workspace templates into ``target_dir``; return created paths."""
    mapping = placeholders(config)
    base = resources.files("paper_writing_agent").joinpath("templates", "workspace")
    created: list[str] = []
    for relative, text in _iter_templates(base):
        destination = os.path.join(target_dir, relative)
        if os.path.exists(destination) and not overwrite:
            continue
        os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)
        with open(destination, "w", encoding="utf-8") as handle:
            handle.write(_substitute(text, mapping))
        created.append(destination)
    return sorted(created)
