---
name: section-status
description: >
  Track and use the completion level (low/middle/high) of each prose unit, and
  pick the strongest in-project units as exemplars before drafting a weak one.
  Use when planning what to write next or recording revision progress. Wraps
  `pwa sections`. Never promotes a unit automatically.
version: 1.0.0
allowed-tools:
  - Read
  - Bash
---

# Section status

Know where the manuscript stands and what to imitate.

## Commands

- Sync units from the document tree: `pwa sections sync main.tex`
- Show the table: `pwa sections status`
- Record a level change (explicit, with history):
  `pwa sections set introduction middle --reason "revised after review"`
- List exemplars before drafting a unit:
  `pwa sections exemplars introduction`

## Workflow

1. Before drafting a `low` unit, run `exemplars` and read the `high` then
   `middle` units. Follow their structure, register, statistical notation, and
   citation discipline.
2. After the user approves a revision, record the new level with `set`.
3. Never self-promote a unit; the level changes only when the user says so.

See `SECTION_STATUS.template.md` for the level definitions.
