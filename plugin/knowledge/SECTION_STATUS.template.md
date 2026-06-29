# Section status (how to read the tracker)

The completion tracker (`section_status.yaml`, managed by `pwa sections`) records
the state of every prose unit. This note explains how to use it; the data lives
in the YAML file, not here.

## Levels

- **low**: first draft or skeleton; not yet aligned with the paper's intent.
- **middle**: revised at least once and approved; usable as a style reference.
- **high**: near-final and fully aligned; the strongest in-project exemplar.

## Rules

- Promotion is never automatic. The agent proposes a change; you run
  `pwa sections set <unit> <level>` to record it (history is kept).
- Before drafting a `low` unit, read the exemplars first:
  `pwa sections exemplars <unit>` lists `high` then `middle` units. Follow their
  structure, register, statistical notation, and citation discipline.
- Keep the tracker in sync with the document tree after adding or removing units:
  `pwa sections sync <root>`.

## Reading the distribution

The mix of levels is a running signal of where the manuscript stands. Aim to lift
the lowest units toward the exemplars, not to polish what is already `high`.
