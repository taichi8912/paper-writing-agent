---
title: "paper-writing-agent: Public Release Requirements"
doc_id: REQ-0001
status: approved
created: 2026-06-29
language: English
related_notes:
  - "[[論文執筆エージェントの外部リポジトリ公開]]"
source_prompt: "Obsidian Vault/NewPrompt/論文執筆エージェントの外部リポジトリ公開.md (Request.1)"
---

# paper-writing-agent: Public Release Requirements (REQ-0001)

This is the authoritative specification for the public, open-source release of a
scientific paper-writing agent, generalized from a private agent built while
writing high-impact manuscripts. It is the contract that the implementation and
all later changes are measured against.

> Origin: this specification derives from Request.1 of the source prompt
> [[論文執筆エージェントの外部リポジトリ公開]]. The requirement to link back to
> that note is satisfied by the `related_notes` field above and by a reciprocal
> Wikilink added to the source note.

## 1. Goal and scope

Re-implement the paper-writing agent as a public software project that any
researcher can use, with **no leakage** of project-specific or author-private
material, and with **friendly, configurable defaults** in place of the original
agent's hard-coded, author-tuned settings.

### 1.1 Objectives

- Maximize writing efficiency for computer-science and software-engineering
  papers.
- Maximize the probability of acceptance at high-impact venues.
- Carry the author's distinctive design philosophy through the README and the
  source: evidence grounding, anti-AI-slop, statistical honesty, traceability.

### 1.2 Non-goals

- Not a domain-specific tool. No quantum-machine-learning, genomics, or any
  single-discipline content in the shipped product.
- Not a replacement for journal peer review. The peer-review feature is a
  pre-submission self-review aid only.
- Not an autonomous writer. The user holds decision authority at every step.

## 2. Decisions (confirmed with the user)

| Decision | Value |
| --- | --- |
| Implementation form | Hybrid: Claude Code plugin + Python package |
| Project name | `paper-writing-agent` (CLI `paper-writing-agent`, alias `pwa`; import `paper_writing_agent`) |
| Location | `/<project-root>/paper-writing-agent` |
| Requirements location | `docs/requirements/` (version-controlled with the code) |
| Configuration UX | `init` wizard + selectable presets |
| Code / docs language | English; README additionally in 中文 and 日本語 |
| License | MIT (code); CC BY-SA attribution for adapted anti-AI-writing catalogue in `NOTICE` |

## 3. Design philosophy (the eight pillars)

The canonical statement lives in [`../DESIGN_PHILOSOPHY.md`](../DESIGN_PHILOSOPHY.md);
summarized here for completeness.

1. Evidence grounding and traceability.
2. Anti-AI-slop.
3. Statistical honesty (significance requires test + P-value + verdict).
4. Single source of truth.
5. Plan, confirm, execute, verify (user decision authority).
6. Reproducibility and audit trail.
7. Configurable, not rigid.
8. Dogfooding (the project lints its own prose).

Quality hierarchy: **Accuracy ≫ Clarity ≫ Conciseness ≫ Professionalism.**

## 4. Functional requirements

### 4.1 Configuration and onboarding (`config/`, `pwa init`)

- FR-CFG-1: A typed configuration model serialized as TOML (`paper-writing-agent.toml`).
- FR-CFG-2: An interactive `init` wizard that asks for target field, venue tier,
  citation style, spelling variant, strictness preset, and operating language,
  then writes a config with friendly defaults; every value is overridable.
- FR-CFG-3: Built-in presets: `strict-high-IF`, `balanced`, `lenient`.
- FR-CFG-4: All defaults are non-destructive and documented; running with no
  config uses `balanced`.

### 4.2 Anti-AI-slop linter (`slop/`, `pwa lint`)

- FR-SLOP-1: Detect forbidden vocabulary in three tiers (Tier 1 forbidden,
  Tier 2 replace-with-alternative, Tier 3 forbidden phrases).
- FR-SLOP-2: Detect structural AI patterns (em dashes with zero tolerance by
  default, copula avoidance, present-participle padding, synonym cycling, rule
  of three, negative parallelism, inflated significance, generic conclusions).
- FR-SLOP-3: Emit findings with file, line, matched text, rule id, severity, and
  a suggested replacement.
- FR-SLOP-4: Support `--exit-zero` (warn-only), machine-readable output (JSON),
  and project-local extension/allow lists.
- FR-SLOP-5: Operate on Markdown and LaTeX; never alter content inside code
  blocks, math, or verbatim environments.

### 4.3 Bibliography context indexer (`bibindex/`, `pwa bib`)

- FR-BIB-1: Parse a BibTeX file into a per-key context index (metadata + topic
  tags + factual summary + suitable contexts + sample phrases + `cite_as`).
- FR-BIB-2: Validate the index against a JSON Schema with anti-hallucination
  gates (no placeholder phrases, no forbidden vocabulary, full key coverage,
  `cite_as` pattern check).
- FR-BIB-3: Merge-preserving regeneration (`--update`): add new keys without
  destroying human curation of existing entries.
- FR-BIB-4: Optional author-grounding: extract verbatim citation usage from a
  prior manuscript's source to ground new citation decisions.
- FR-BIB-5: Detect duplicate keys and missing required fields.

### 4.4 Statistical-honesty linter (`stats/`, `pwa stats`)

- FR-STAT-1: Flag any reported P-value that lacks an explicit significance
  verdict in the same or an adjacent sentence.
- FR-STAT-2: Flag a statistical test name repeated after its first occurrence
  (style configurable).
- FR-STAT-3: Check P-value and numeric notation against the configured house
  style (capitalization, scientific notation, significant figures, thousands
  separators, leading zeros, number-unit spacing).
- FR-STAT-4: Define a re-runnable statistics-store format (full precision in,
  rounded display out) and refuse values transcribed from images.

### 4.5 Section-status tracker (`sections/`, `pwa sections`)

- FR-SEC-1: Track each prose unit's completion level: `low`, `middle`, `high`.
- FR-SEC-2: Keep a change history (date, unit, old/new level, reason).
- FR-SEC-3: Stay in sync with the document tree (`\input`/`\subfile` or Markdown
  headings).
- FR-SEC-4: Given a target unit, list the strongest `high` then `middle` units
  as exemplars.
- FR-SEC-5: Never auto-promote a unit; promotion requires explicit user action.

### 4.6 Definitions registry and no-forward-reference linter (`definitions/`, `pwa defs`)

- FR-DEF-1: Maintain a registry of symbols and abbreviations with the
  reading-order point of first definition.
- FR-DEF-2: Flag a symbol or abbreviation used before it is defined.
- FR-DEF-3: Flag a symbol or abbreviation defined more than once.

### 4.7 Aggregate check (`pwa check`)

- FR-CHK-1: Run the configured linters over a manuscript and produce a single
  consolidated report and exit status.

### 4.8 Claude Code plugin (`plugin/`)

- FR-PLG-1: Ship skills wrapping the core checks (humanizer/slop, bib-indexer,
  section-status, definitions-check).
- FR-PLG-2: Ship adapter skills for external deep-research and peer-review tools
  that are READ-ONLY with respect to the manuscript and user-triggered only.
- FR-PLG-3: Ship slash commands and agent definitions encoding the
  plan-confirm-execute-verify workflow.
- FR-PLG-4: Ship a knowledge base of journal-agnostic templates (style guide,
  definitions, section status, citation policy, paper outline, provenance map,
  project profile) plus a system-prompt template stating the operating
  principles in English.

### 4.9 Manuscript-workspace templates (`templates/`, emitted by `pwa init`)

- FR-TPL-1: `pwa init` scaffolds a per-manuscript workspace from the templates,
  parameterized by the chosen configuration.

## 5. Configurable knobs vs. always-on invariants

### 5.1 Configurable (with friendly defaults)

Target field (default: CS/software), venue tier, citation style
(numeric/author-year), spelling (US/UK), P-value notation, significant figures,
section structure (Methods naming; Supplementary vs Extended Data),
figure-reference abbreviation, hedging strictness, operating language
(en/ja/zh), principle verbosity, forbidden-word extensions.

### 5.2 Always-on invariants

Quality hierarchy as default; significance requires test + P-value + verdict;
evidence grounding; no speculative edits to unread files; user decision
authority; no fabricated citations.

## 6. Privacy and information-leakage requirements

- PRIV-1: No project-specific model names, domain terms, datasets, cell lines,
  hardware, experiment ids, dates, or request history.
- PRIV-2: No author name, email, or server/file paths.
- PRIV-3: No venue-specific private rules; venue behavior is configuration.
- PRIV-4: All worked examples are synthetic and drawn from CS/software domains.
- PRIV-5: A privacy statement in `NOTICE` asserts the above.

## 7. Non-functional requirements

- NFR-1: Python 3.10+; typed; `ruff` + `black` clean; `mypy` advisory.
- NFR-2: Unit and golden-file tests for every linter; CI on 3.10, 3.11, and 3.12.
- NFR-3: Deterministic linter output (stable ordering) for reproducible CI.
- NFR-4: The project dogfoods its own anti-slop linter in pre-commit and CI.
- NFR-5: No network calls in the core; external tools are opt-in through the plugin.

## 8. Development base structure (process as product)

The repository layout and process embody the philosophy:

- Single-source-of-truth layout; one canonical file per rule/state.
- Spec-driven: this document is the contract; design philosophy is the appeal
  court.
- Reproducible tooling: pinned dev tooling, deterministic outputs, semver,
  Keep a Changelog, Conventional Commits.
- Dogfooding gate in CI and pre-commit.
- `CONTRIBUTING.md` restates the operating principles for human contributors.

## 9. Acceptance criteria

- AC-1: `pip install -e .` succeeds; `pwa --help` lists all subcommands.
- AC-2: `pwa init` produces a valid config and a manuscript workspace.
- AC-3: Each linter has passing unit/golden tests and flags its target patterns
  on a fixture.
- AC-4: `pwa check` consolidates linter output with a correct exit status.
- AC-5: The Claude Code plugin loads (valid `plugin.json`, skills, commands,
  agents) and its adapters are READ-ONLY and user-triggered.
- AC-6: A single root `README.md` carries English, 简体中文, and 日本語 sections,
  cross-linked by an anchor-based language navigation bar at the top, and each
  section includes an author-responsibility disclaimer.
- AC-7: A privacy scan finds none of the forbidden private tokens (PRIV-1/2/3).
- AC-8: The project's own docs pass `pwa lint` (dogfooding).

## 10. Implementation phases

| Phase | Deliverable |
| --- | --- |
| P0 | Scaffold + this requirements doc + reciprocal Wikilink + `git init` |
| P1 | Config model + presets + `init` wizard + CLI skeleton |
| P2 | Anti-slop linter + tests |
| P3 | Bibliography indexer + schema + validate + merge + author-grounding + tests |
| P4 | Statistical-honesty linter + section tracker + definitions linter + tests |
| P5 | Claude Code plugin (skills, commands, agents, knowledge, system prompt) |
| P6 | Manuscript-workspace templates emitted by `init` |
| P7 | README (EN/ZH/JA), design philosophy, architecture, contributing; dogfood lint; final verification |
