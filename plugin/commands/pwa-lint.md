---
description: Run the anti-AI-slop linter on the given files or directories and summarize findings.
argument-hint: "[paths...]"
allowed-tools:
  - Bash
  - Read
---

Run the anti-AI-slop linter on `$ARGUMENTS` (default: the current directory).

1. Run `pwa lint $ARGUMENTS --format text`.
2. Group the findings by rule and severity. Errors are forbidden vocabulary,
   filler phrases, and em dashes; warnings are replace-with-alternative words and
   structural patterns.
3. For each finding, propose the specific rewrite (use the linter's suggestion).
   Do not edit files unless asked; if asked, follow plan-then-confirm.
