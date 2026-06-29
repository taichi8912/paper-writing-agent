"""Integration tests for the command-line interface."""

from __future__ import annotations

import json

from paper_writing_agent.cli import main


def test_no_command_prints_help_and_succeeds(capsys):
    assert main([]) == 0
    assert "usage:" in capsys.readouterr().out


def test_version(capsys):
    # argparse --version raises SystemExit(0).
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    assert "paper-writing-agent" in capsys.readouterr().out


def test_init_writes_config_and_workspace(tmp_path):
    rc = main(["init", str(tmp_path), "--yes"])
    assert rc == 0
    assert (tmp_path / "paper-writing-agent.toml").is_file()
    assert (tmp_path / "README.md").is_file()
    assert (tmp_path / "bib" / "README.md").is_file()


def test_init_no_workspace(tmp_path):
    rc = main(["init", str(tmp_path), "--yes", "--no-workspace"])
    assert rc == 0
    assert (tmp_path / "paper-writing-agent.toml").is_file()
    assert not (tmp_path / "PROJECT_PROFILE.md").exists()


def test_init_refuses_overwrite_without_force(tmp_path):
    assert main(["init", str(tmp_path), "--yes"]) == 0
    assert main(["init", str(tmp_path), "--yes"]) == 1
    assert main(["init", str(tmp_path), "--yes", "--force"]) == 0


def test_lint_clean_and_dirty(tmp_path):
    clean = tmp_path / "clean.md"
    clean.write_text("We measured a 32% improvement over the baseline.", encoding="utf-8")
    assert main(["lint", str(clean)]) == 0

    dirty = tmp_path / "dirty.md"
    dirty.write_text("We delve into a pivotal idea.", encoding="utf-8")
    assert main(["lint", str(dirty)]) == 1
    assert main(["lint", str(dirty), "--exit-zero"]) == 0


def test_lint_json_output(tmp_path, capsys):
    dirty = tmp_path / "dirty.md"
    dirty.write_text("We leverage a pivotal trick.", encoding="utf-8")
    main(["lint", str(dirty), "--format", "json", "--exit-zero"])
    payload = json.loads(capsys.readouterr().out)
    assert "findings" in payload and "summary" in payload


def test_bib_build_validate_ground(tmp_path):
    bib = tmp_path / "refs.bib"
    bib.write_text(
        "@article{a2020, title={A Study of X}, author={A, B}, journal={J}, year={2020}}\n"
        '@inproceedings{c2021, title="A GPU Method", author="C, D", booktitle="P", year="2021"}\n',
        encoding="utf-8",
    )
    index = tmp_path / "index.yaml"
    assert main(["bib", "build", str(bib), "--output", str(index)]) == 0
    assert index.is_file()
    assert main(["bib", "validate", str(index), "--bib", str(bib)]) == 0

    prior = tmp_path / "prior.tex"
    prior.write_text("\\section{Intro}\nText \\cite{a2020} here.", encoding="utf-8")
    assert main(["bib", "ground", str(index), "--from", str(prior)]) == 0


def test_bib_without_action_returns_one(tmp_path):
    assert main(["bib"]) == 1


def test_sections_flow(tmp_path):
    root = tmp_path / "main.tex"
    root.write_text("\\input{introduction}\n\\subfile{results.tex}\n", encoding="utf-8")
    tracker = tmp_path / "section_status.yaml"
    assert main(["sections", "sync", str(root), "--tracker", str(tracker)]) == 0
    assert main(["sections", "set", "introduction", "high", "--date", "2026-06-29",
                 "--tracker", str(tracker)]) == 0
    assert main(["sections", "status", "--tracker", str(tracker)]) == 0
    assert main(["sections", "exemplars", "results", "--tracker", str(tracker)]) == 0


def test_defs_check_and_build(tmp_path, capsys):
    forward = tmp_path / "f.md"
    forward.write_text(
        "We use the CNN first. A Convolutional Neural Network (CNN) is a model.",
        encoding="utf-8",
    )
    assert main(["defs", "check", str(forward)]) == 1
    assert main(["defs", "check", str(forward), "--exit-zero"]) == 0

    clean = tmp_path / "c.md"
    clean.write_text(
        "A Convolutional Neural Network (CNN) is a model. We use the CNN.",
        encoding="utf-8",
    )
    assert main(["defs", "check", str(clean)]) == 0
    assert main(["defs", "build", str(clean)]) == 0


def test_check_aggregate(tmp_path):
    dirty = tmp_path / "d.md"
    dirty.write_text("We delve into results (P = 0.01).", encoding="utf-8")
    assert main(["check", str(dirty)]) == 1
    assert main(["check", str(dirty), "--exit-zero"]) == 0
