# Manuscript workspace

This workspace was scaffolded by `pwa init`. It holds the project-specific
context the writing agent uses, alongside your manuscript sources.

## Layout

- `PROJECT_PROFILE.md` -- this paper's venue, field, conventions, and vocabulary.
- `paper_outline.md` -- per-section argument and evidence map.
- `DEFINITIONS.md` -- registry of abbreviations and symbols (define once).
- `citation_policy.md` -- how to cite accurately and never fabricate a key.
- `provenance_map.md` -- traceability from figures and numbers to source code.
- `section_status.yaml` -- completion tracker (managed by `pwa sections`).
- `bib/` -- your `refs.bib` and the generated `bib_index.yaml`.
- `stats/` -- full-precision statistics extracted from your analysis.
- `paper-writing-agent.toml` -- the resolved configuration (edit freely).

## Resolved configuration

- Field: {{FIELD}}
- Venue tier: {{VENUE_TIER}}
- Strictness preset: {{PRESET}}
- Citation style: {{CITATION_STYLE}}
- Spelling: {{SPELLING}}
- P-value notation: {{PVALUE_NOTATION}}
- Section structure: {{SECTION_STRUCTURE}}
- Figure references: {{FIGURE_REF}}
- Operating language: {{LANGUAGE}}

## Everyday commands

```bash
pwa check .                       # run all linters (slop + stats + defs)
pwa bib build bib/refs.bib --output bib/bib_index.yaml
pwa bib validate bib/bib_index.yaml --bib bib/refs.bib --strict
pwa sections sync main.tex        # update the completion tracker
pwa sections exemplars <unit>     # what to imitate before drafting <unit>
pwa defs check <files in reading order>
```

The writing rules and operating principles live in the documentation and the
Claude Code plugin; `pwa check` enforces the machine-checkable subset here.
