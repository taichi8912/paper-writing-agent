# Contributing to paper-writing-agent

Thank you for considering a contribution. This project enforces a particular
discipline on the manuscripts it helps write, and it holds its own development
to the same standard. The development base structure is part of the product:
how we build the tool demonstrates the philosophy the tool encodes.

## The operating principles (how we work)

These are the generic, English form of the workflow the agent itself follows.
They apply to maintainers, contributors, and the agent equally.

1. **Plan, then confirm.** Report the plan before generating or changing files.
   For non-trivial changes, open an issue or a draft PR describing the plan and
   wait for review before large edits.
2. **No silent detours.** If the agreed plan fails, surface it and agree on the
   next step. Do not swap in an alternative approach unannounced.
3. **The maintainer decides.** Automation is a tool; humans hold decision
   authority. The tool never auto-applies destructive or far-reaching changes.
4. **Rules are stable.** The design philosophy (see `docs/DESIGN_PHILOSOPHY.md`)
   is the top-level contract; do not reinterpret it to justify a change.
5. **Evidence over assertion.** Every claim in code, tests, or docs resolves to
   a source. No speculative edits to files you have not read.

## Ground rules for changes

- **Investigate before editing.** Read the file and its tests first.
- **Requested change only.** Do not refactor surrounding code opportunistically
  in the same change; keep diffs reviewable.
- **Single source of truth.** Each rule or piece of state lives in exactly one
  canonical place. If you add a rule, add it once and reference it elsewhere.
- **Dogfood.** Prose you add to `docs/` and `README*.md` must pass the project's
  own anti-slop linter (`pwa lint docs/`).
- **No private data.** This is a generic tool. Never add project-specific,
  unpublished, or author-private material, paths, names, or credentials.

## Development setup

```bash
git clone https://github.com/taichi8912/paper-writing-agent
cd paper-writing-agent
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Quality gate (run before opening a PR)

```bash
ruff check src tests
black --check src tests
mypy src
pytest --cov=paper_writing_agent
pwa lint docs/ README.md   # dogfood the anti-slop linter on our own prose
```

## Commit and PR conventions

- Conventional Commits: `feat(slop): ...`, `fix(bibindex): ...`, `docs: ...`,
  `test: ...`, `chore: ...`, `refactor: ...`.
- One logical change per commit; tests accompany behavior changes.
- PRs describe the plan, the change, and the verification performed.

## Code style

- Python 3.11+, type-hinted, formatted with `black`, linted with `ruff`.
- Name things for what they are: avoid `tmp`, `data`, `retval`; include units in
  names (`delay_ms`, `size_bytes`); boolean names read as predicates
  (`is_enabled`, `has_citation`).
- Comments explain *why*, not *what*. Flag traps and non-obvious constraints.
