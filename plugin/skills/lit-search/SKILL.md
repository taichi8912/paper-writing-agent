---
name: lit-search
description: >
  Find prior work for the Introduction or Discussion and feed only verified
  references into the bibliography pipeline. READ-ONLY with respect to the
  manuscript; results go to a staging area, not directly into the paper.
  User-triggered only. Use when asked to "find related work", "search the
  literature", or "check what exists" before writing.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - WebSearch
  - WebFetch
  - Bash
---

# Literature search (staging adapter)

Bring in prior work safely, without polluting the manuscript or the bibliography.

## Invariants

- **Manuscript READ-ONLY.** Do not edit the paper.
- **Staging only.** Write findings to a staging file (for example
  `lit_search/<topic>.md`); do not write to the `.bib` directly.
- **User-triggered only.** Run only when asked (operating principle 1).
- **Verify before use.** Treat a source as usable only after confirming it
  exists and says what you claim. Mark unverifiable sources as failed.

## Procedure

1. Search for candidate works on the requested topic; capture title, authors,
   year, venue, and a one-line factual finding for each.
2. Verify each candidate against its real source page; drop the unverifiable.
3. Write the verified candidates to the staging file with a short synthesis.
4. The author adds chosen entries to the `.bib`, then you run
   `pwa bib build --update` and `pwa bib validate` to fold them into the index.

If an external deep-research tool is installed, this skill can call it in the
same READ-ONLY, user-triggered, staging-first way; otherwise it searches inline.
