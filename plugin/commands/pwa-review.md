---
description: Run a READ-ONLY pre-submission self-review and write a reviewer report plus a revision roadmap.
argument-hint: "[manuscript path]"
allowed-tools:
  - Bash
  - Read
  - Write
---

Run a pre-submission self-review of `$ARGUMENTS` (default: the manuscript in the
current workspace). Use the `peer-review` skill.

1. Read the draft (compiled PDF or section sources), the style guide, the
   statistics store, and the project profile. Run `pwa check` and fold its
   findings in.
2. Produce independent perspectives (methods/statistics, domain/novelty,
   clarity/presentation, devil's advocate), an editor summary, and a prioritized
   revision roadmap.
3. Write all output to separate files under `review/<date>/` and report the
   paths. Do NOT edit the manuscript; the roadmap informs the author, who
   decides what to change.
