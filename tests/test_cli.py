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
