# Project profile

What is specific to this paper. Keep it free of unpublished or private material
if the repository is public.

## Paper

- Working title: TODO
- Field: {{FIELD}}
- Target venue: TODO (tier: {{VENUE_TIER}})
- Submission format: TODO (LaTeX / Markdown / DOCX through Pandoc)

## Contribution (one paragraph)

State the conceptual or technical advance in plain language: what is new, what
problem it solves, and why it matters.

## Conventions (mirror paper-writing-agent.toml)

- Spelling: {{SPELLING}}
- Citation style: {{CITATION_STYLE}}
- P-value notation: {{PVALUE_NOTATION}}
- Section structure: {{SECTION_STRUCTURE}}
- Figure references: {{FIGURE_REF}}

## Experiment sources (point the agent here)

The agent writes from your artifacts, not from memory. Record where each kind of
evidence lives, so every method, number, and figure resolves to the code and logs
that produced it. Absolute paths or paths relative to this workspace both work;
write "none" for anything that does not apply.

- Results and outputs: TODO (run outputs, checkpoints, metrics)
- Experiment source code: TODO (the analysis or training code)
- Run scripts and job files: TODO (what launched each run)
- Experiment configuration: TODO (run configs, hyperparameters)
- Logs: TODO (stdout, stderr, training logs)
- Environment recipe: TODO (requirements.txt, environment.yml, Dockerfile, lockfile)
- Virtual environment: TODO (interpreter or env path, for exact versions)
- Statistics store: stats/ (full-precision numbers; see provenance_map.md)

The more of this the agent can read, the less the paper loses in translation.

## Project vocabulary

- Preferred terms and their definitions (define once, use bare).
- Terms to avoid in prose (for example, implementation class or function names).
- Project-local additions to the forbidden-word list (slop.extra_forbidden).

## Prior work to ground citations

If you have a prior paper, give its source path so `pwa bib ground` can extract
how you cited each reference; grounded keys become verified.

- Prior manuscript source: TODO (or "none")
