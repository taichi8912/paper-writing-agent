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
from datetime import date as _date

import yaml

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
from .definitions import build_registry, lint_definitions
from .sections import (
    LEVELS,
    discover_units,
    exemplars,
    load_tracker,
    new_tracker,
    save_tracker,
    set_level,
    summarize,
    sync_tracker,
)
from .slop import default_extensions, format_json, format_text, has_errors, lint_paths
from .stats import lint_stats

_TRACKER_DEFAULT = "section_status.yaml"

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
# stats
# --------------------------------------------------------------------------- #
def _gather_files(paths: Sequence[str]) -> list[str]:
    extensions = default_extensions()
    found: list[str] = []
    for entry in paths:
        if os.path.isdir(entry):
            for root, _dirs, files in os.walk(entry):
                found.extend(
                    os.path.join(root, name)
                    for name in sorted(files)
                    if name.lower().endswith(extensions)
                )
        elif os.path.isfile(entry):
            found.append(entry)
    return found


def _cmd_stats(args: argparse.Namespace) -> int:
    config = Config.load(args.config) if args.config else load_config()
    findings = []
    for path in _gather_files(args.paths):
        with open(path, encoding="utf-8") as handle:
            findings.extend(lint_stats(handle.read(), path=path, config=config))

    _echo(format_json(findings) if args.format == "json" else format_text(findings))
    if args.exit_zero:
        return 0
    return 1 if has_errors(findings) else 0


# --------------------------------------------------------------------------- #
# sections
# --------------------------------------------------------------------------- #
def _load_or_new_tracker(path: str) -> dict:
    return load_tracker(path) if os.path.isfile(path) else new_tracker()


def _cmd_sections_status(args: argparse.Namespace) -> int:
    tracker = _load_or_new_tracker(args.tracker)
    counts = summarize(tracker)
    _echo(f"Units: {counts['total']} (high {counts['high']}, middle {counts['middle']}, low {counts['low']})")
    for unit in tracker["units"]:
        present = "" if unit.get("present", True) else "  [missing]"
        _echo(f"  {unit.get('level', 'low'):6} {unit['name']}{present}")
    return 0


def _cmd_sections_sync(args: argparse.Namespace) -> int:
    tracker = _load_or_new_tracker(args.tracker)
    discovered = discover_units(args.root)
    sync_tracker(tracker, discovered)
    save_tracker(args.tracker, tracker)
    _echo(f"Synced {len(discovered)} unit(s) into {args.tracker}.")
    return _cmd_sections_status(args)


def _cmd_sections_set(args: argparse.Namespace) -> int:
    tracker = _load_or_new_tracker(args.tracker)
    when = args.date or _date.today().isoformat()
    set_level(tracker, args.unit, args.level, reason=args.reason, date=when)
    save_tracker(args.tracker, tracker)
    _echo(f"Set {args.unit} -> {args.level} ({when}).")
    return 0


def _cmd_sections_exemplars(args: argparse.Namespace) -> int:
    tracker = _load_or_new_tracker(args.tracker)
    picks = exemplars(tracker, target=args.unit)
    if not picks:
        _echo("No high/middle exemplars available yet.")
        return 0
    _echo(f"Exemplars to imitate when drafting {args.unit!r} (strongest first):")
    for pick in picks:
        _echo(f"  {pick['level']:6} {pick['name']}  {pick['path']}")
    return 0


# --------------------------------------------------------------------------- #
# defs
# --------------------------------------------------------------------------- #
def _cmd_defs_check(args: argparse.Namespace) -> int:
    files = _gather_files(args.files)
    findings = lint_definitions(files)
    _echo(format_json(findings) if args.format == "json" else format_text(findings))
    if args.exit_zero:
        return 0
    return 1 if has_errors(findings) else 0


def _cmd_defs_build(args: argparse.Namespace) -> int:
    registry = build_registry(_gather_files(args.files))
    text = yaml.safe_dump(registry, sort_keys=False, allow_unicode=True, width=100)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(text)
        _echo(f"Wrote {args.output} ({len(registry['abbreviations'])} abbreviations).")
    else:
        _echo(text)
    return 0


# --------------------------------------------------------------------------- #
# check (aggregate)
# --------------------------------------------------------------------------- #
def _cmd_check(args: argparse.Namespace) -> int:
    config = Config.load(args.config) if args.config else load_config()
    files = _gather_files(args.paths)

    findings = list(lint_paths(args.paths, config=config))
    for path in files:
        with open(path, encoding="utf-8") as handle:
            findings.extend(lint_stats(handle.read(), path=path, config=config))
    findings.extend(lint_definitions(files))
    findings.sort(key=lambda f: (f.path, f.line, f.col, f.rule_id))

    _echo(format_json(findings) if args.format == "json" else format_text(findings))
    if args.exit_zero:
        return 0
    return 1 if has_errors(findings) else 0


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

    p_stats = sub.add_parser("stats", help="run the statistical-honesty linter")
    p_stats.add_argument("paths", nargs="*", default=["."], help="files or directories")
    p_stats.add_argument("--exit-zero", action="store_true", help="always exit 0 (warn-only)")
    p_stats.add_argument("--format", choices=("text", "json"), default="text")
    p_stats.add_argument("--config", default=None, help="path to a config file")
    p_stats.set_defaults(func=_cmd_stats)

    p_sections = sub.add_parser("sections", help="show / update the section-status tracker")
    sec_sub = p_sections.add_subparsers(dest="sections_command", metavar="<action>")

    s_status = sec_sub.add_parser("status", help="show the completion table")
    s_status.add_argument("--tracker", default=_TRACKER_DEFAULT, help="tracker YAML path")
    s_status.set_defaults(func=_cmd_sections_status)

    s_sync = sec_sub.add_parser("sync", help="discover units from a root and update the tracker")
    s_sync.add_argument("root", help="LaTeX root (\\input/\\subfile) or a Markdown file")
    s_sync.add_argument("--tracker", default=_TRACKER_DEFAULT, help="tracker YAML path")
    s_sync.set_defaults(func=_cmd_sections_sync)

    s_set = sec_sub.add_parser("set", help="set a unit's completion level (explicit)")
    s_set.add_argument("unit", help="unit name")
    s_set.add_argument("level", choices=LEVELS, help="completion level")
    s_set.add_argument("--reason", default="", help="why the level changed")
    s_set.add_argument("--date", default="", help="ISO date (default: today)")
    s_set.add_argument("--tracker", default=_TRACKER_DEFAULT, help="tracker YAML path")
    s_set.set_defaults(func=_cmd_sections_set)

    s_ex = sec_sub.add_parser("exemplars", help="list high/middle units to imitate")
    s_ex.add_argument("unit", help="the unit you are about to draft")
    s_ex.add_argument("--tracker", default=_TRACKER_DEFAULT, help="tracker YAML path")
    s_ex.set_defaults(func=_cmd_sections_exemplars)
    p_sections.set_defaults(func=lambda a: _require_subcommand(p_sections))

    p_defs = sub.add_parser("defs", help="check the symbol/abbreviation registry")
    defs_sub = p_defs.add_subparsers(dest="defs_command", metavar="<action>")

    d_check = defs_sub.add_parser("check", help="flag forward references and redefinitions")
    d_check.add_argument("files", nargs="+", help="files in reading order")
    d_check.add_argument("--exit-zero", action="store_true", help="always exit 0 (warn-only)")
    d_check.add_argument("--format", choices=("text", "json"), default="text")
    d_check.set_defaults(func=_cmd_defs_check)

    d_build = defs_sub.add_parser("build", help="emit an abbreviation registry")
    d_build.add_argument("files", nargs="+", help="files in reading order")
    d_build.add_argument("--output", default=None, help="output YAML path (default: stdout)")
    d_build.set_defaults(func=_cmd_defs_build)
    p_defs.set_defaults(func=lambda a: _require_subcommand(p_defs))

    p_check = sub.add_parser("check", help="run all linters (slop + stats + defs)")
    p_check.add_argument("paths", nargs="*", default=["."], help="files or directories")
    p_check.add_argument("--exit-zero", action="store_true", help="always exit 0 (warn-only)")
    p_check.add_argument("--format", choices=("text", "json"), default="text")
    p_check.add_argument("--config", default=None, help="path to a config file")
    p_check.set_defaults(func=_cmd_check)

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
