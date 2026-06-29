# Examples

Synthetic, computer-science examples that show the tool in action. They contain
no project-specific or private material.

- `before_slop.md`: a paragraph written with typical AI fingerprints and a bare
  P-value. Run the linters on it to see the findings:

  ```bash
  pwa check examples/before_slop.md
  ```

- `after_clean.md`: the same content rewritten to pass `pwa check`. Compare the
  two to see the intended register.

  ```bash
  pwa check examples/after_clean.md   # exits 0
  ```

## More examples

- `latex/`: a two-file LaTeX snippet (`abstract.tex`, `introduction.tex`). It
  shows the statistical-honesty linter reading a P-value inside `$...$`, and the
  define-once check across files in reading order. It is a clean positive
  example:

  ```bash
  pwa check examples/latex/abstract.tex examples/latex/introduction.tex   # exits 0
  pwa defs check examples/latex/abstract.tex examples/latex/introduction.tex
  ```

- `bibliography/`: a small `refs.bib` plus a walkthrough of
  `pwa bib build / validate / ground`. See `bibliography/README.md`.

