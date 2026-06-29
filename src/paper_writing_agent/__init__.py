"""paper-writing-agent.

An evidence-grounded, anti-AI-slop manuscript-writing agent for
computer-science and software-engineering papers, engineered to maximize
acceptance at high-impact venues.

The package exposes a deterministic, editor-agnostic core (linters, validators,
indexers, and a configuration model). The agentic layer lives under ``plugin/``
as a Claude Code plugin that drives this core.
"""

__version__ = "0.1.0"
