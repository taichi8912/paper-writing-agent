# Citation policy

How to place citations accurately and never hallucinate one. Works with the
context index built by `pwa bib build`.

## When to cite

- A specific factual claim attributable to prior work.
- A named model, algorithm, dataset, benchmark, or tool.
- A comparison or contrast with prior work.
- A background fact a reader would expect a reference for.

## How to choose a key

1. Open `bib/bib_index.yaml`; find candidates by topic, citation role, and
   reading-order availability.
2. Prefer keys with `curation_status: verified` over `derived` when both fit.
3. Place `\cite{key}` at the end of the supported clause, before punctuation;
   combine co-supporting keys in one command.

## Hard rules

- Never invent a key. If none fits, leave `% TODO: cite -- <claim>` and continue.
- No citation stuffing (two or three per paragraph outside related work).
- Pull any statistic from `stats/`, never from memory.

## Maintenance

- After editing the `.bib`, run `pwa bib build --update`, then
  `pwa bib validate` (use `--strict` before submission).
