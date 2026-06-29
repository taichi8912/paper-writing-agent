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
from .bibindex import (
    apply_grounding,
    build_index,
    extract_usage,
    load_index,
    merge_index,
    parse_bibtex,
    save_index,
    validate_index,
)
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
# bib
# --------------------------------------------------------------------------- #
def _require_subcommand(parser: argparse.ArgumentParser) -> int:
    parser.print_help()
    return 1


def _default_index_path(bib_path: str) -> str:
    directory = os.path.dirname(os.path.abspath(bib_path))
    return os.path.join(directory, "bib_index.yaml")


def _cmd_bib_build(args: argparse.Namespace) -> int:
    with open(args.bib_file, encoding="utf-8") as handle:
        entries = parse_bibtex(handle.read())
    fresh = build_index(entries, source_bib=os.path.basename(args.bib_file))

    output = args.output or _default_index_path(args.bib_file)
    index = fresh
    if args.update and os.path.isfile(output):
        index = merge_index(load_index(output), fresh)

    meta = index["metadata"]
    _echo(f"Parsed {meta['total_entries']} entries, {meta['unique_keys']} unique keys.")
    if meta["duplicate_keys"]:
        _echo(f"Duplicate keys: {', '.join(meta['duplicate_keys'])}")
    top = sorted(index["topics"].items(), key=lambda kv: (-len(kv[1]), kv[0]))[:5]
    if top:
        _echo("Top topics: " + ", ".join(f"{tag} ({len(ids)})" for tag, ids in top))
    missing = sum(1 for e in index["entries"] if not e.get("doi") and not e.get("url"))
    if missing:
        _echo(f"Entries with no DOI or URL: {missing}")

    if args.dry_run:
        _echo("Dry run: no file written.")
        return 0
    save_index(output, index)
    _echo(f"Wrote {output}")
    return 0


def _cmd_bib_validate(args: argparse.Namespace) -> int:
    index = load_index(args.index_file)
    bib_keys = None
    if args.bib:
        with open(args.bib, encoding="utf-8") as handle:
            bib_keys = [entry.key for entry in parse_bibtex(handle.read())]
    report = validate_index(index, bib_keys=bib_keys, strict=args.strict)
    _echo(report.render())
    return 0 if report.ok else 1


def _cmd_bib_ground(args: argparse.Namespace) -> int:
    index = load_index(args.index_file)
    combined = []
    for source in args.source:
        with open(source, encoding="utf-8") as handle:
            combined.append(handle.read())
    usage = extract_usage("\n".join(combined))
    grounded = apply_grounding(index, usage, mark_verified=not args.no_verified)

    output = args.output or args.index_file
    save_index(output, index)
    _echo(f"Grounded {grounded} entr(y/ies) from {len(args.source)} source file(s).")
    _echo(f"Wrote {output}")
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

    p_bib = sub.add_parser("bib", help="build / validate / ground a bibliography context index")
    bib_sub = p_bib.add_subparsers(dest="bib_command", metavar="<action>")

    b_build = bib_sub.add_parser("build", help="build a context index from a .bib file")
    b_build.add_argument("bib_file", help="path to a BibTeX file")
    b_build.add_argument("--output", default=None, help="output index path (YAML)")
    b_build.add_argument("--update", action="store_true", help="merge into an existing index")
    b_build.add_argument("--dry-run", action="store_true", help="report stats; write nothing")
    b_build.set_defaults(func=_cmd_bib_build)

    b_validate = bib_sub.add_parser("validate", help="validate an index against the schema/gates")
    b_validate.add_argument("index_file", help="path to a context index (YAML)")
    b_validate.add_argument("--bib", default=None, help="source .bib for coverage checking")
    b_validate.add_argument("--strict", action="store_true", help="treat needs_review as an error")
    b_validate.set_defaults(func=_cmd_bib_validate)

    b_ground = bib_sub.add_parser("ground", help="attach real citation usage from a prior paper")
    b_ground.add_argument("index_file", help="path to a context index (YAML)")
    b_ground.add_argument("--from", dest="source", nargs="+", required=True, help="prior .tex files")
    b_ground.add_argument("--output", default=None, help="output path (default: in place)")
    b_ground.add_argument(
        "--no-verified", action="store_true", help="do not mark grounded entries verified"
    )
    b_ground.set_defaults(func=_cmd_bib_ground)
    p_bib.set_defaults(func=lambda a: _require_subcommand(p_bib))

    for name, phase, helptext in (
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
