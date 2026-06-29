# Provenance map

End-to-end traceability for every figure, table, and headline number, so any
claim can be traced back to the code and data that produced it.

## Naming

Name analysis notebooks by what they show and claim, not by figure number, so
renumbering the paper does not break the map.

## Per-figure entries

| Figure/Table | Notebook | Experiment dir | Run script | Dataset | Preprocessing | Raw source |
| --- | --- | --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## Statistics

Each reported number resolves to a full-precision record in `stats/`, produced by
a re-runnable extraction script, never transcribed from a figure image. Round to
the configured significant figures only in the prose.

## Rule

A training experiment is traced to the full pipeline (raw data -> preprocessing
-> dataset -> run -> notebook -> figure), not just the final run.
