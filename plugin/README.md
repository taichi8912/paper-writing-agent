# paper-writing-agent (Claude Code plugin)

The agentic layer of paper-writing-agent. It drives the deterministic Python core
(`pwa`) and ships a knowledge base of journal-agnostic writing templates.

## What it provides

- **Skills** (`skills/`): `humanizer` (anti-AI-slop), `bib-context` (citation
  index), `section-status` (completion tracker), `definitions-check` (define-once
  discipline), and two READ-ONLY, user-triggered adapters, `peer-review` and
  `lit-search`.
- **Commands** (`commands/`): `/pwa-lint`, `/pwa-check`, `/pwa-cite`,
  `/pwa-draft`, `/pwa-review`.
- **Agents** (`agents/`): `writer`, `citation`, `reviewer`, `provenance`.
- **Knowledge** (`knowledge/`): the operating principles, the style guide, an
  agent system prompt, and templates for the project profile, citation policy,
  section status, definitions, paper outline, and provenance map.

## Prerequisite

Install the core so the skills and commands can call it:

```bash
pip install paper-writing-agent   # provides the `pwa` command
```

## Install the plugin

Point Claude Code at this repository as a plugin marketplace (the manifest is in
`.claude-plugin/plugin.json`), or copy `plugin/` into your project's
`.claude/` plugin path. See the project root `README.md` for current install
instructions.

## How the layers fit

The plugin holds workflow, prompts, and templates. Every deterministic check is
delegated to the core (`pwa lint|stats|defs|bib|sections|check`), which is
unit-tested and editor-agnostic. The rules are verifiable; the agent orchestrates.
