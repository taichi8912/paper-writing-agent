---
description: Run every linter (anti-slop, statistical honesty, definitions) and report a consolidated result.
argument-hint: "[paths...]"
allowed-tools:
  - Bash
  - Read
---

Run the full check on `$ARGUMENTS` (default: the current directory).

1. Run `pwa check $ARGUMENTS`.
2. Summarize by category: slop (vocabulary/structure), stats (P-value verdicts,
   notation, test naming, numbers/units), and definitions (forward references,
   redefinitions).
3. List the errors first (these would block submission), then the warnings.
4. Propose fixes grouped by file. Edit only on request, following
   plan-then-confirm.
