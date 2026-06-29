# Architecture

> Status: scaffold. This document is expanded as modules land (P1-P7). The
> authoritative specification is
> [`requirements/0001-public-release-requirements.md`](requirements/0001-public-release-requirements.md).

paper-writing-agent is a **hybrid**: a deterministic Python core that any editor
can call, plus a Claude Code plugin that drives the core agentically.

```
paper-writing-agent/
├── src/paper_writing_agent/   # deterministic core (editor-agnostic)
│   ├── cli.py                 #   entry point: pwa init|lint|bib|stats|sections|defs|check
│   ├── config/               #   config model + presets + init wizard
│   ├── slop/                 #   anti-AI-slop linter
│   ├── bibindex/             #   bibliography context indexer + schema validator
│   ├── stats/                #   statistics store + statistical-honesty linter
│   ├── sections/             #   completion tracker (low/middle/high) + exemplars
│   └── definitions/          #   symbol/abbreviation registry + no-forward-reference linter
├── plugin/                    # Claude Code plugin (agentic layer)
│   ├── skills/  commands/  agents/  knowledge/
│   └── plugin.json
├── templates/                 # manuscript-workspace scaffolding emitted by `pwa init`
├── examples/                  # synthetic CS/software worked examples
├── tests/                     # pytest + golden-file tests
└── docs/                      # README (EN/ZH/JA), design philosophy, this file, requirements
```

## Two layers, one core

- The **core** is pure, testable, and deterministic. It holds the rules and the
  checks. It has no dependency on any editor or LLM.
- The **plugin** is the agentic layer. It supplies workflow, prompts, and
  knowledge-base templates, and it calls the core for every deterministic check.

This separation keeps the rules verifiable (the core is unit-tested) while the
agent layer stays free to orchestrate.

## Data flow (writing a manuscript)

```
config (venue, style, strictness)
        │
        ▼
knowledge templates ──► draft prose ──► core linters ──► verdicts
   (style guide,                         (slop, stats,      │
    definitions,                          sections,         ▼
    citation policy)                      definitions)   revise → re-verify
        ▲                                                    │
        └──────────── bibindex (citation context) ◄──────────┘
```
