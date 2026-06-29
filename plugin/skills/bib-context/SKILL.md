---
name: bib-context
description: >
  Build, validate, and ground a bibliography context index so citations are
  accurate and never hallucinated. Use when adding citations, after editing the
  .bib file, or when asked to find the right reference for a claim. Wraps
  `pwa bib` and the citation policy.
version: 1.0.0
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
---

# Bibliography context

Give the agent the context it needs to cite the right key for each claim, and
keep it honest.

## Build and maintain

- Build the index from a BibTeX file:
  `pwa bib build refs.bib --output bib_index.yaml`
- After editing the `.bib`, regenerate without losing curation:
  `pwa bib build refs.bib --output bib_index.yaml --update`
- Validate (run `--strict` before submission):
  `pwa bib validate bib_index.yaml --bib refs.bib [--strict]`
- Ground citations in your real prior usage (sets entries to `verified`):
  `pwa bib ground bib_index.yaml --from prior_paper/*.tex`

## Placing a citation

1. Read `bib_index.yaml`; find candidates by topic, citation role, and reading-
   order availability.
2. Prefer `verified` keys over `derived` ones when both fit.
3. Insert `\cite{key}` at the end of the supported clause; combine co-supporting
   keys in one command.
4. If no key fits, leave `% TODO: cite -- <claim>` and continue. Never invent a
   key.

See `citation_policy.template.md` for the full policy.
