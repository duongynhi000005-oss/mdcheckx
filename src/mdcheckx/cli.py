from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable

UNCHECKED = re.compile(r"^\s*[-*+]\s+\[ \]\s+")
CHECKED = re.compile(r"^\s*[-*+]\s+\[[xX]\]\s+")


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def stats(text: str) -> tuple[int, int]:
    done = 0
    todo = 0
    for line in text.splitlines():
        if CHECKED.search(line):
            done += 1
        elif UNCHECKED.search(line):
            todo += 1
    return done, todo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mdcheckx", description="Markdown checklist progress reporter CLI")
    parser.add_argument("path", nargs="?", default="-", help="Markdown file path (or - for stdin)")
    parser.add_argument("--json", action="store_true", help="print JSON output")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        text = read_text(args.path)
        done, todo = stats(text)
        total = done + todo
        pct = 0.0 if total == 0 else round((done / total) * 100, 2)
        if args.json:
            print(f'{{"done":{done},"todo":{todo},"total":{total},"percent":{pct}}}')
        else:
            print(f"done: {done}")
            print(f"todo: {todo}")
            print(f"total: {total}")
            print(f"percent: {pct}%")
        return 0
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
