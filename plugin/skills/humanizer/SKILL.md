---
name: humanizer
description: >
  Remove signs of AI-generated writing from a scientific manuscript and make it
  read as precise, human academic prose. Detects and fixes inflated significance,
  copula avoidance, participle padding, synonym cycling, the rule of three,
  negative parallelism, em dashes, filler phrases, and AI vocabulary; restores
  plain, factual constructions. Use during revision, or whenever asked to
  "humanize", "remove AI tells", or "polish" a draft. Computer-science and
  software-engineering oriented.
version: 1.0.0
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
---

# Humanizer

Make a manuscript read like precise human academic writing. The authoritative,
enforced pattern list lives in the linter; this skill is how to apply and fix it.

## Procedure

1. Run the linter to locate machine-detectable patterns:
   `pwa lint <paths> --format json` (and `pwa check <paths>` for the full set).
2. For each finding, rewrite the sentence to remove the pattern while keeping the
   data and meaning intact. Prefer the suggestion the linter gives.
3. Re-run `pwa lint`/`pwa check` until clean (or until remaining findings are
   deliberate and allow-listed).

## Patterns to fix (intent; the linter owns the values)

- **Inflated significance / self-praise.** Drop `novel`, `remarkable`, `pivotal`,
  `groundbreaking`. Report the result; let the reader judge.
- **Copula avoidance.** `X serves as a bottleneck` becomes `X is the bottleneck`.
- **Participle padding.** `..., highlighting the benefit` becomes a new sentence
  with an explicit connective, or is deleted.
- **Synonym cycling.** Do not rotate `method` / `approach` / `technique` for the
  same thing; name it once and keep it.
- **Rule of three.** Do not pad to three items for rhythm.
- **Negative parallelism.** `not only X but also Y` becomes `X and Y`.
- **Em dashes.** Replace with commas, parentheses, or a period (zero tolerance by
  default).
- **Filler phrases.** `due to the fact that` becomes `because`; delete
  `it is important to note that`.
- **AI vocabulary.** `leverage` becomes `use`; `via` becomes `through`; `enhance`
  becomes `improve`; `robust` becomes `reliable`.

## Rules

- Preserve every number, statistic, and citation exactly.
- Keep appropriate hedging; simplify stacked hedges rather than removing caution.
- Legitimate single academic transitions (`Notably,`) are fine; flag only when
  stacked. See `STYLE_GUIDE.md` sections 7 and 8.
- This skill edits prose only on request, following plan-then-confirm.
