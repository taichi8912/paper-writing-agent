---
description: Draft or revise a section, grounded in exemplars, the style guide, and the evidence map.
argument-hint: "<section/unit name>"
allowed-tools:
  - Bash
  - Read
  - Edit
---

Draft or revise the unit: `$ARGUMENTS`.

1. Read the style guide and the project profile. Run
   `pwa sections exemplars $ARGUMENTS` and read the strongest units to match
   their register and structure.
2. Pull the section's argument and evidence from the paper outline; pull any
   numbers from the statistics store (full precision, then round).
3. Plan the draft (claim-first paragraphs, calibrated hedging, statistics with
   verdicts, citations from the index). Confirm the plan before writing.
4. Write the draft. Place citations from the index; mark gaps with
   `% TODO: cite`.
5. Run `pwa check` on the unit; if LaTeX, compile. Fix findings and report what
   you verified. Do not change the unit's completion level yourself.
