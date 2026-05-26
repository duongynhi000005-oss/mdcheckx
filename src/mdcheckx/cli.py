from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable
from pathlib import Path

UNCHECKED = re.compile(r"^\s*[-*+]\s+\[ \]\s+")
CHECKED = re.compile(r"^\s*[-*+]\s+\[[xX]\]\s+")
MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdown"}


def read_text(path: Path | str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def stats(text: str) -> tuple[int, int]:
    done = 0
    todo = 0
    for line in text.splitlines():
        if CHECKED.search(line):
            done += 1
        elif UNCHECKED.search(line):
            todo += 1
    return done, todo


def iter_markdown_files(paths: list[str]) -> list[Path | str]:
    if not paths:
        return ["-"]

    files: list[Path | str] = []
    for raw in paths:
        if raw == "-":
            files.append(raw)
            continue
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix.lower() in MARKDOWN_SUFFIXES:
                    files.append(child)
        else:
            files.append(path)
    return files


def summarize(paths: list[str]) -> dict[str, object]:
    files = []
    done = 0
    todo = 0

    for path in iter_markdown_files(paths):
        text = read_text(path)
        file_done, file_todo = stats(text)
        total = file_done + file_todo
        done += file_done
        todo += file_todo
        files.append(
            {
                "path": str(path),
                "done": file_done,
                "todo": file_todo,
                "total": total,
                "percent": 0.0 if total == 0 else round((file_done / total) * 100, 2),
            }
        )

    total = done + todo
    return {
        "done": done,
        "todo": todo,
        "total": total,
        "percent": 0.0 if total == 0 else round((done / total) * 100, 2),
        "files": files,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mdcheckx", description="Markdown checklist progress reporter CLI")
    parser.add_argument("paths", nargs="*", help="Markdown file(s), dirs, or - for stdin")
    parser.add_argument("--json", action="store_true", help="print JSON output")
    parser.add_argument("--per-file", action="store_true", help="print each file's stats")
    parser.add_argument("--fail-under", type=float, default=None, metavar="PCT", help="exit 2 if overall percent is below PCT")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        data = summarize(args.paths)
        if args.json:
            print(json.dumps(data, separators=(",", ":"), ensure_ascii=False))
        else:
            print(f"done: {data['done']}")
            print(f"todo: {data['todo']}")
            print(f"total: {data['total']}")
            print(f"percent: {data['percent']}%")
            if args.per_file:
                for item in data["files"]:
                    print(f"{item['path']}: {item['done']}/{item['total']} ({item['percent']}%)")
        if args.fail_under is not None and data["percent"] < args.fail_under:
            return 2
        return 0
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
