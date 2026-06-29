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
