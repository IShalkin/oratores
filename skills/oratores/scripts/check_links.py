#!/usr/bin/env python3
"""Relative-link checker for the oratores package.

Verifies that every relative markdown link resolves to a file or directory
that exists. External links (http/https/mailto) are not fetched.

Run from anywhere:
    python skills/oratores/scripts/check_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent.parent.parent

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")
EXTERNAL = ("http://", "https://", "mailto:", "#")

SKIP_DIRS = {".git", ".github", "__pycache__", "node_modules"}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO)).replace("\\", "/")
    except ValueError:
        return str(path)


def markdown_files() -> list[Path]:
    out: list[Path] = []
    for path in REPO.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        out.append(path)
    return sorted(out)


def main() -> int:
    broken: list[str] = []
    checked = 0

    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if target.startswith(EXTERNAL):
                continue
            # strip any anchor
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            checked += 1
            if not (resolved.is_file() or resolved.is_dir()):
                broken.append(f"{rel(path)} -> {target}")

    for b in broken:
        print(f"FAIL  broken link: {b}")

    if broken:
        print(f"\n{len(broken)} broken link(s) out of {checked} checked.")
        return 1

    print(f"OK  {checked} relative link(s) resolve across {len(markdown_files())} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
