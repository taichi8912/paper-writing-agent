# Provenance map (template)

End-to-end traceability for every figure, table, and headline number, so any
claim can be traced back to the code and data that produced it. This is what lets
the agent ground statements in evidence rather than memory.

## Naming

Name analysis notebooks by what they show and claim, not by figure number, so
renumbering the paper does not break the map (for example
`throughput_vs_baseline.ipynb`, not `fig2.ipynb`).

## Per-figure entries

| Figure/Table | Notebook | Experiment dir | Run script | Dataset | Preprocessing | Raw source |
| --- | --- | --- | --- | --- | --- | --- |
| <Figure 1> | <notebook> | <experiment dir> | <script> | <dataset> | <pipeline> | <raw> |

## Statistics

Each reported number resolves to a full-precision record in the statistics store
(`stats/`), produced by a re-runnable extraction script, never transcribed from a
figure image. Round to the configured significant figures only in the prose.

## Rule

A training experiment is traced to the full pipeline (raw data -> preprocessing
-> dataset -> run -> notebook -> figure), not just the final run.
