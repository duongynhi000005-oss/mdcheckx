from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-m", "mdcheckx", *args]
    return subprocess.run(
        command,
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        env={"PYTHONPATH": str(ROOT / "src")},
    )


def test_counts_checkboxes(tmp_path: Path) -> None:
    doc = tmp_path / "todo.md"
    doc.write_text("- [x] done\n- [ ] wait\n", encoding="utf-8")

    result = run_cli(str(doc))

    assert result.returncode == 0
    assert "done: 1" in result.stdout
    assert "todo: 1" in result.stdout


def test_json_output(tmp_path: Path) -> None:
    doc = tmp_path / "todo.md"
    doc.write_text("- [ ] wait\n", encoding="utf-8")

    result = run_cli(str(doc), "--json")

    assert result.returncode == 0
    assert '"todo":1' in result.stdout


def test_reads_stdin() -> None:
    result = run_cli("-", input_text="- [x] done\n")

    assert result.returncode == 0
    assert "percent: 100.0%" in result.stdout


def test_walks_directory_and_prints_per_file(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("- [x] ship\n", encoding="utf-8")
    (docs / "b.markdown").write_text("- [ ] wait\n- [ ] review\n", encoding="utf-8")
    (docs / "ignore.txt").write_text("- [x] skip\n", encoding="utf-8")

    result = run_cli(str(docs), "--per-file")

    assert result.returncode == 0
    assert "done: 1" in result.stdout
    assert "todo: 2" in result.stdout
    assert "a.md: 1/1 (100.0%)" in result.stdout
    assert "b.markdown: 0/2 (0.0%)" in result.stdout


def test_json_includes_file_details(tmp_path: Path) -> None:
    first = tmp_path / "one.md"
    second = tmp_path / "two.md"
    first.write_text("- [x] done\n", encoding="utf-8")
    second.write_text("- [ ] todo\n", encoding="utf-8")

    result = run_cli(str(first), str(second), "--json")

    assert result.returncode == 0
    assert '"files":[' in result.stdout
    assert '"path":"' in result.stdout


def test_fail_under_exits_nonzero(tmp_path: Path) -> None:
    doc = tmp_path / "todo.md"
    doc.write_text("- [ ] wait\n", encoding="utf-8")

    result = run_cli(str(doc), "--fail-under", "50")

    assert result.returncode == 2
    assert "percent: 0.0%" in result.stdout


def test_fail_under_passes_when_threshold_met(tmp_path: Path) -> None:
    doc = tmp_path / "todo.md"
    doc.write_text("- [x] done\n- [ ] wait\n", encoding="utf-8")

    result = run_cli(str(doc), "--fail-under", "50")

    assert result.returncode == 0
