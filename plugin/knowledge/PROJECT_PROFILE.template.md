# Project profile (template)

This file records what is specific to *your* paper: the venue, the field, the
conventions, and any project-local vocabulary. It is the generic counterpart of
an author-preferences file. Copy it into your manuscript workspace and fill it in.
Keep it free of unpublished or private material if the repository is public.

## Paper

- Working title: <title>
- Field: <e.g., systems / ML / PL / security>
- Target venue: <venue> (tier: <high-IF / mid / workshop>)
- Submission format: <LaTeX / Markdown / DOCX through Pandoc>

## Contribution (one paragraph)

State the conceptual or technical advance in plain language: what is new, what
problem it solves, and why it matters.

## Conventions (mirror `paper-writing-agent.toml`)

- Spelling: <US / UK>
- Citation style: <numeric / author-year>
- P-value notation: <P-italic-sci / p-lower-sci / p-lower-e>
- Section structure: <methods-supplementary / methods-extended / imrad>
- Figure references: <full / abbreviated>

## Project vocabulary

- Preferred terms and their definitions (define once, use bare).
- Terms to avoid in prose (for example, implementation class or function names).
- Project-local additions to the forbidden-word list (`slop.extra_forbidden`).

## Prior work to ground citations

If you have a prior paper, list its source path so `pwa bib ground` can extract
how you cited each reference; grounded keys become verified.

- Prior manuscript source: <path or "none">
