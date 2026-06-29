---
name: definitions-check
description: >
  Enforce "define once, then use bare" for abbreviations and symbols. Flags an
  abbreviation used before it is defined (forward reference) and any term defined
  twice (redefinition), in reading order across files. Use before submission or
  after restructuring sections. Wraps `pwa defs`.
version: 1.0.0
allowed-tools:
  - Read
  - Bash
---

# Definitions check

Keep terminology consistent and free of forward references.

## Commands

- Check in reading order (pass files in the order a reader meets them):
  `pwa defs check abstract.tex introduction.tex results.tex discussion.tex methods.tex`
- Seed an abbreviation registry from the text:
  `pwa defs build <files...> --output definitions.yaml`

## What it catches

- **Forward reference**: an abbreviation used before "Long Form (ABBR)" appears.
  Fix by introducing the term at first use, or reordering.
- **Redefinition**: the same abbreviation expanded twice. Define once; afterwards
  use it bare.

Keep `DEFINITIONS.template.md` as the single source of truth for what each symbol
and abbreviation means.
