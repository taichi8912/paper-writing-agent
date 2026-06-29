---
description: Place an accurate citation for a claim using the bibliography context index, never inventing a key.
argument-hint: "<claim or file:line>"
allowed-tools:
  - Bash
  - Read
  - Edit
---

Find and place the right citation for: `$ARGUMENTS`.

1. Ensure an index exists (`pwa bib build refs.bib` if needed) and read
   `bib_index.yaml`.
2. Identify candidate keys by topic, citation role, and reading-order
   availability. Prefer `verified` keys over `derived` ones.
3. Propose the `\cite{...}` placement (end of the supported clause). If no key
   fits, propose a `% TODO: cite -- <claim>` marker instead. Never invent a key.
4. On approval, make the edit, then run `pwa bib validate bib_index.yaml`.

Follow the citation policy in the plugin knowledge base.
