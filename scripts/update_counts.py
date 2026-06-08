#!/usr/bin/env python3
"""Count the brain's Markdown files per top-level folder.

Used by /sync-orientation-docs and /weekly-maintenance to keep the documented
file counts (in SECOND_BRAIN_MASTER_INDEX.md and CONTENT_TAXONOMY.md) honest.
Those skills read this script's stdout and compare it to the documented tables.

Generic by design: it auto-discovers your top-level content folders, so it keeps
working as you add or prune folders — nothing hardcoded to one person's brain.

Usage:
    python3 scripts/update_counts.py        # print the counts table
"""
import datetime
import os
from pathlib import Path

# Repo root: $SECOND_BRAIN_ROOT if set, else the parent of this scripts/ dir.
ROOT = Path(os.environ.get("SECOND_BRAIN_ROOT", Path(__file__).resolve().parent.parent))

# Infra folders that hold the machinery, not the owner's content.
SKIP = {".git", ".claude", "scripts", "examples"}


def count_md(folder: Path) -> int:
    return sum(1 for _ in folder.rglob("*.md"))


def main() -> int:
    folders = sorted(
        p for p in ROOT.iterdir()
        if p.is_dir() and not p.name.startswith(".") and p.name not in SKIP
    )
    counts = {p.name: count_md(p) for p in folders}
    total = sum(counts.values())

    width = max((len(name) for name in counts), default=6)
    print(f"FILE COUNTS  ({datetime.date.today().isoformat()})  root={ROOT}")
    print("-" * (width + 10))
    for name, n in counts.items():
        print(f"{name.ljust(width)}  {n:>6}")
    print("-" * (width + 10))
    print(f"{'TOTAL'.ljust(width)}  {total:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
