# paper-writing-agent

> An evidence-grounded, anti-AI-slop manuscript-writing agent for
> computer-science and software-engineering papers, engineered to maximize
> acceptance at high-impact venues.

**Languages:** English · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

## What it is

paper-writing-agent helps you draft and revise scientific papers so that the
prose is precise, the statistics are honest, the citations are real, and the text
carries no AI fingerprints. It is a **hybrid**:

- a deterministic **Python core** (`pip install paper-writing-agent`, command
  `pwa`) that lints prose, indexes a bibliography, tracks completion, and checks
  definitions; and
- a **Claude Code plugin** that drives the core agentically and ships a knowledge
  base of journal-agnostic writing templates.

Sensible defaults out of the box; everything is overridable through `pwa init`.

## Why it works this way (design philosophy)

The full statement is in [docs/DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md).
In short, eight pillars:

1. **Evidence grounding.** Every claim resolves to a source: a number, a figure's
   provenance, a citation, or a definition.
2. **Anti-AI-slop.** AI prose has fingerprints; the linter finds them and
   proposes precise academic replacements.
3. **Statistical honesty.** "Significant" needs a test, a P-value, and an
   explicit verdict.
4. **Single source of truth.** Each rule and each piece of state has one owner.
5. **Plan, confirm, execute, verify.** The user holds decision authority.
6. **Reproducibility.** Statistics are re-runnable; changes are auditable.
7. **Configurable, not rigid.** Venue, citation style, spelling, and strictness
   are settings, not assumptions.
8. **Dogfooding.** The project lints its own prose with its own linter.

Objective: maximize acceptance at a high-impact venue. Quality hierarchy:
**Accuracy > Clarity > Conciseness > Professionalism.**

## Slides

A nine-slide deck on the motivation and technical core lives in
[docs/slides/](docs/slides/):
[PDF](docs/slides/design-philosophy.pdf) ·
[PPTX](docs/slides/design-philosophy.pptx) (native, editable).

## Install

```bash
pip install paper-writing-agent        # provides the `pwa` command
# or, from a clone:
pip install -e ".[dev]"
```

For the Claude Code plugin, see [plugin/README.md](plugin/README.md).

## Quickstart

```bash
# 1. Set up a manuscript workspace (interactive; or add --yes for defaults).
pwa init my-paper/

# 2. Write, then check your prose against every rule.
pwa check my-paper/

# 3. Build a citation context index from your bibliography.
pwa bib build my-paper/bib/refs.bib --output my-paper/bib/bib_index.yaml
pwa bib validate my-paper/bib/bib_index.yaml --bib my-paper/bib/refs.bib --strict

# 4. Track section completion and find exemplars to imitate.
pwa sections sync my-paper/main.tex
pwa sections exemplars introduction

# 5. Check define-once discipline in reading order.
pwa defs check my-paper/abstract.tex my-paper/introduction.tex
```

## Commands

| Command | What it does |
| --- | --- |
| `pwa init <dir>` | Create a config and scaffold a manuscript workspace. |
| `pwa lint <paths>` | Find AI-writing fingerprints; suggest replacements. |
| `pwa stats <paths>` | Check P-value verdicts, test naming, and number/unit style. |
| `pwa defs check <files>` | Flag forward references and redefinitions in reading order. |
| `pwa bib build/validate/ground` | Build, validate, and ground a citation context index. |
| `pwa sections status/sync/set/exemplars` | Track completion; pick exemplars. |
| `pwa check <paths>` | Run all linters at once. |

Each linter exits non-zero on errors, accepts `--exit-zero` for warn-only use,
and supports `--format json`.

## Configuration

`pwa init` writes `paper-writing-agent.toml` from a preset
(`strict-high-IF` / `balanced` / `lenient`) and a short wizard. Every value is
editable by hand. Configurable knobs include target field and venue tier,
citation style, spelling (US/UK), P-value notation, significant figures, section
structure, figure-reference style, hedging strictness, operating language, and
project-local forbidden-word extensions. Invariant by design: significance needs
a test and a verdict, citations are never fabricated, and the user decides.

## Two layers, one core

The Python core is pure, deterministic, and unit-tested; it owns the rules and
the checks and has no editor dependency. The Claude Code plugin supplies the
workflow, prompts, and templates, and calls the core for every check. See
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Privacy

This is a generic, domain-agnostic tool. It contains no project-specific,
unpublished, or author-private material. All worked examples are synthetic and
drawn from the computer-science and software domains. See [NOTICE](NOTICE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The project holds its own development to
the same discipline it enforces on manuscripts.

## License

MIT (see [LICENSE](LICENSE)). Attribution for adapted content is in
[NOTICE](NOTICE).
