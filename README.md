# paper-writing-agent

> An evidence-grounded, anti-AI-slop manuscript-writing agent for
> computer-science and software-engineering papers, engineered to maximize
> acceptance at high-impact venues.

**Languages:** English (this file) · [中文](docs/README.zh.md) · [日本語](docs/README.ja.md)

> Status: alpha scaffold. The full README, install instructions, and worked
> examples are completed in the final documentation pass. For now, see:
>
> - [Design philosophy](docs/DESIGN_PHILOSOPHY.md): the contract behind every feature.
> - [Architecture](docs/ARCHITECTURE.md): how the hybrid core and plugin fit together.
> - [Requirements](docs/requirements/0001-public-release-requirements.md): the authoritative specification.
> - [Contributing](CONTRIBUTING.md): how we work, and how the project holds itself to its own standard.

## What it does

paper-writing-agent helps you draft and revise scientific papers so that the
prose is precise, the statistics are honest, the citations are real, and the
text carries no AI fingerprints. It is a **hybrid**: a deterministic Python core
(`pip install paper-writing-agent`, command `pwa`) plus a Claude Code plugin that
drives the core agentically.

Sensible defaults out of the box; everything overridable through `pwa init`.

## License

MIT (see [LICENSE](LICENSE)). Attribution for adapted content is in
[NOTICE](NOTICE).
