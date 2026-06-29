# Architecture

> The authoritative specification is
> [`requirements/0001-public-release-requirements.md`](requirements/0001-public-release-requirements.md).

paper-writing-agent is a **hybrid**: a deterministic Python core that any editor
can call, plus a Claude Code plugin that drives the core agentically.

```
paper-writing-agent/
├── src/paper_writing_agent/   # deterministic core (editor-agnostic)
│   ├── cli.py                 #   entry point: pwa init|lint|bib|stats|sections|defs|check
│   ├── config/               #   config model + presets + init wizard + TOML I/O
│   ├── slop/                 #   anti-AI-slop linter (rules, masking, engine, report)
│   ├── bibindex/             #   BibTeX parser, context index, schema validator, grounding
│   ├── stats/                #   statistical-honesty linter
│   ├── sections/             #   completion tracker (low/middle/high) + exemplars
│   ├── definitions/          #   abbreviation registry + no-forward-reference linter
│   ├── scaffold.py           #   workspace scaffolder used by `pwa init`
│   └── templates/workspace/  #   manuscript-workspace templates (shipped as package data)
├── plugin/                    # Claude Code plugin (agentic layer)
│   ├── .claude-plugin/plugin.json
│   ├── skills/  commands/  agents/  knowledge/
│   └── README.md
├── examples/                  # synthetic CS/software worked examples
├── tests/                     # pytest tests for every module
└── docs/                      # README (EN/ZH/JA), design philosophy, this file, requirements
```

The report format is shared: the `slop`, `stats`, and `definitions` linters all
emit the same `Finding` type, so `pwa check` and the JSON output are uniform.

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
