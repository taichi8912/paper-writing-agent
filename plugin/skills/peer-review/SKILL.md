---
name: peer-review
description: >
  Pre-submission self-review of a finished draft. Produces independent reviewer
  perspectives, an editorial summary, and a prioritized revision roadmap as
  SEPARATE documents. READ-ONLY with respect to the manuscript: it never edits
  the paper. User-triggered only. Use when asked to "review", "self-review", or
  "simulate peer review" before submitting.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Peer review (self-review aid)

A pre-submission check, not a substitute for the venue's real peer review.

## Invariants

- **READ-ONLY manuscript.** Do not edit the paper. Write reviews to separate
  files (for example `review/<date>/`).
- **User-triggered only.** Run only when the user asks (operating principle 1).
- **No fabricated critique.** Ground every comment in the actual text, a missing
  control, an unstated assumption, or a real statistical concern.

## Procedure

1. Read the compiled PDF or the section sources, the style guide, the statistics
   store, and the project profile.
2. Produce independent perspectives: a methods/statistics reviewer, a
   domain/novelty reviewer, a clarity/presentation reviewer, and a devil's
   advocate who argues for rejection.
3. Add an editor summary (accept / minor / major / reject, with reasons) and a
   prioritized revision roadmap.
4. Save all output as separate documents and report their paths. Do not apply any
   changes; the roadmap informs the author, who decides.

If an external reviewer tool is installed, this skill can call it in the same
READ-ONLY, user-triggered way; otherwise it performs the review inline.
