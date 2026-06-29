# Statistics store

Keep full-precision statistics here, extracted by a re-runnable script (never
transcribed from a figure image). Round only in the prose, to the configured
significant figures.

Suggested per-figure layout:

```
stats/
  Figure1/
    main.json     # per-group mean/std/n and per-comparison test, P-value, effect size
    main.csv      # one row per pairwise comparison
```

When the manuscript states a statistic, pull the full-precision value from here,
then round. `pwa stats` checks that every reported P-value carries an explicit
significance verdict and that notation follows the house style.
