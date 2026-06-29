# Citation policy (template)

How to place citations accurately and never hallucinate one. This policy works
with the bibliography context index built by `pwa bib build`.

## When to cite

- A specific factual claim attributable to prior work.
- A named model, algorithm, dataset, benchmark, or tool.
- A comparison or contrast with prior work.
- A background fact a reader would expect a reference for.

## How to choose a key

1. Open the context index and find candidates by topic, role, and reading-order
   availability (`available_from_section`).
2. Prefer keys with `curation_status: verified` (grounded in your real prior
   usage) over `derived` ones when both fit.
3. Place `\cite{key}` at the end of the clause or sentence it supports, before
   the punctuation. Combine co-supporting keys in one command.

## Hard rules (anti-hallucination)

- **Never invent a key.** Use only keys present in the bibliography and index.
- **If no key fits, leave** `% TODO: cite -- <one-line description>` and move on.
- **No citation stuffing.** At most two or three citations per paragraph, except
  in a dedicated related-work paragraph.
- **No fabricated numbers inside a citation context.** Pull any statistic from
  the statistics store.
- **Introduce a reference at its earliest allowed section,** then reuse it bare;
  re-cite only when a new specific claim needs it.

## Maintenance

- After editing the `.bib`, rebuild with `pwa bib build --update` (preserves
  curation) and re-run `pwa bib validate` (and `--strict` before submission).
