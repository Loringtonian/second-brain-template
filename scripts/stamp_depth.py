#!/usr/bin/env python3
"""
stamp_depth.py — set the privacy `depth: N` (1-5) in a file's YAML frontmatter.

`depth` is the per-file privacy/disclosure level (1 = public … 5 = sealed). See
`Orientation_Docs/PRIVACY_DEPTH.md` for what the levels mean and how to calibrate them.
Idempotent: re-running with the same value makes no change.

Usage:
    python3 scripts/stamp_depth.py <file.md> <N>            # set depth to N (1-5)
    python3 scripts/stamp_depth.py <file.md> <N> --dry-run  # show what would change
    python3 scripts/stamp_depth.py <file.md>                # print the current depth (or "none")
"""
import re
import sys
from pathlib import Path

DEPTH_RE = re.compile(r"^depth:\s*(\d+)\s*$", re.MULTILINE)


def split_frontmatter(text: str):
    """Return (frontmatter_without_fences, body) or (None, text) if there is no block."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5:]
    return None, text


def get_depth(text: str):
    fm, _ = split_frontmatter(text)
    if fm is None:
        return None
    m = DEPTH_RE.search(fm)
    return int(m.group(1)) if m else None


def set_depth(text: str, depth: int) -> str:
    fm, body = split_frontmatter(text)
    if fm is None:
        return f"---\ndepth: {depth}\n---\n{text}"
    if DEPTH_RE.search(fm):
        fm = DEPTH_RE.sub(f"depth: {depth}", fm, count=1)
    else:
        fm = fm.rstrip("\n") + f"\ndepth: {depth}"
    return f"---\n{fm}\n---\n{body}"


def main() -> int:
    dry = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    if not args:
        print(__doc__)
        return 2
    path = Path(args[0])
    if not path.exists():
        print(f"not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")

    if len(args) == 1:  # read mode
        d = get_depth(text)
        print(d if d is not None else "none")
        return 0

    try:
        depth = int(args[1])
        assert 1 <= depth <= 5
    except Exception:
        print("depth must be an integer 1-5")
        return 2

    new = set_depth(text, depth)
    if new == text:
        print(f"unchanged (already depth {depth}): {path}")
        return 0
    if dry:
        print(f"would set depth {depth}: {path}")
        return 0
    path.write_text(new, encoding="utf-8")
    print(f"depth {depth}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
