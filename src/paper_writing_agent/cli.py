"""Command-line interface for paper-writing-agent.

Uses the standard-library :mod:`argparse` so the core has no CLI dependency and
runs anywhere. Rich is used for nicer output when available and degrades to
plain text otherwise.

Subcommands:

    init        create a config (and, once templates land, a manuscript workspace)
    lint        run the anti-AI-slop linter over files                  (P2)
    bib         build / validate a bibliography context index           (P3)
    stats       run the statistical-honesty linter                      (P4)
    sections    show / update the section-status tracker                (P4)
    defs        check the symbol/abbreviation registry                  (P4)
    check       run all configured linters and consolidate the result   (P4)
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence

from . import __version__
from .config import CONFIG_FILENAME, PRESET_NAMES, Config, load_config, run_wizard
from .slop import format_json, format_text, has_errors, lint_paths

_NOT_YET = "this subcommand is scaffolded; its implementation lands in a later phase"


def _echo(message: str = "") -> None:
    print(message)


def _warn(message: str) -> None:
    print(message, file=sys.stderr)


# --------------------------------------------------------------------------- #
# init
# --------------------------------------------------------------------------- #
def _cmd_init(args: argparse.Namespace) -> int:
    target_dir = os.path.abspath(args.path)
    os.makedirs(target_dir, exist_ok=True)
    config_path = os.path.join(target_dir, CONFIG_FILENAME)

    if os.path.exists(config_path) and not args.force:
        _warn(f"Refusing to overwrite existing {config_path} (use --force).")
        return 1

    config = run_wizard(assume_yes=args.yes, preset=args.preset)
    config.save(config_path)

    _echo(f"Wrote {config_path}")
    _echo("")
    _echo("Configuration summary:")
    _echo(f"  field            {config.project.research_field}")
    _echo(f"  venue tier       {config.project.venue_tier}")
    _echo(f"  preset           {config.project.preset}")
    _echo(f"  citation style   {config.style.citation_style}")
    _echo(f"  spelling         {config.style.spelling}")
    _echo(f"  language         {config.project.operating_language}")
    _echo("")
    _echo("Every value is safe to edit by hand. Next: run `pwa check <path>`.")
    return 0


# --------------------------------------------------------------------------- #
# stubs (implemented in later phases)
# --------------------------------------------------------------------------- #
def _cmd_lint(args: argparse.Namespace) -> int:
    config = Config.load(args.config) if args.config else load_config()
    findings = lint_paths(args.paths, config=config)

    if args.format == "json":
        _echo(format_json(findings))
    else:
        _echo(format_text(findings))

    if args.exit_zero:
        return 0
    # By default only error-severity findings fail the run; warnings are advisory.
    return 1 if has_errors(findings) else 0


def _cmd_stub(name: str, phase: str) -> int:
    _warn(f"{name}: {_NOT_YET} ({phase}).")
    return 0


# --------------------------------------------------------------------------- #
# parser
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="paper-writing-agent",
        description=(
            "Evidence-grounded, anti-AI-slop manuscript-writing agent for "
            "computer-science and software-engineering papers."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p_init = sub.add_parser("init", help="create a configuration")
    p_init.add_argument("path", nargs="?", default=".", help="target directory (default: .)")
    p_init.add_argument(
        "--preset", choices=PRESET_NAMES, default="balanced", help="starting preset"
    )
    p_init.add_argument(
        "--yes", action="store_true", help="accept defaults without prompting"
    )
    p_init.add_argument("--force", action="store_true", help="overwrite an existing config")
    p_init.set_defaults(func=_cmd_init)

    p_lint = sub.add_parser("lint", help="run the anti-AI-slop linter")
    p_lint.add_argument("paths", nargs="*", default=["."], help="files or directories")
    p_lint.add_argument("--exit-zero", action="store_true", help="always exit 0 (warn-only)")
    p_lint.add_argument("--format", choices=("text", "json"), default="text")
    p_lint.add_argument("--config", default=None, help="path to a config file")
    p_lint.set_defaults(func=_cmd_lint)

    for name, phase, helptext in (
        ("bib", "P3", "build / validate a bibliography context index"),
        ("stats", "P4", "run the statistical-honesty linter"),
        ("sections", "P4", "show / update the section-status tracker"),
        ("defs", "P4", "check the symbol/abbreviation registry"),
        ("check", "P4", "run all configured linters"),
    ):
        sp = sub.add_parser(name, help=f"{helptext} ({phase})")
        sp.add_argument("paths", nargs="*", default=["."], help="files or directories")
        sp.set_defaults(func=lambda a, n=name, ph=phase: _cmd_stub(n, ph))

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
