# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Public-release requirements specification and design philosophy
  (`docs/requirements/0001-public-release-requirements.md`,
  `docs/DESIGN_PHILOSOPHY.md`).
- Configuration model with `strict-high-IF` / `balanced` / `lenient` presets, an
  interactive `pwa init` wizard, and dependency-free TOML I/O.
- Anti-AI-slop linter (`pwa lint`): three vocabulary tiers, structural patterns,
  em-dash policy, code/math masking, text and JSON reports.
- Bibliography context indexer (`pwa bib`): BibTeX parser, topic tagging,
  JSON-Schema validation with anti-hallucination gates, merge-preserving
  regeneration, and author-grounding from a prior manuscript.
- Statistical-honesty linter (`pwa stats`): P-value verdict requirement,
  name-the-test-once, and notation checks.
- Section-status tracker (`pwa sections`) and definitions / no-forward-reference
  linter (`pwa defs`); aggregate `pwa check`.
- Manuscript-workspace scaffolding emitted by `pwa init`.
- Claude Code plugin: skills, commands, agents, and a knowledge base (operating
  principles, journal-agnostic style guide, templates).
- Design-philosophy slide deck (`docs/slides/`, native editable PPTX + PDF).
- Trilingual README (English, 中文, 日本語) at the repository root, tests for
  every module, and a
  development base structure that dogfoods the anti-slop linter in pre-commit and
  CI (single-source-of-truth layout, reproducible tooling, semantic versioning).

[Unreleased]: https://github.com/taichi8912/paper-writing-agent/commits/main
