#!/usr/bin/env python3
"""Estimate how many tokens a source would cost to read in full.

Run this BEFORE bulk-reading a large source (a whole Drive export, a notes
archive, years of files) so you can budget it against the owner's plan instead
of discovering mid-session that you burned the whole window. Pairs with /mine
(Phase 0 triage) and /setup (Phase 8 ingestion scope).

The estimate is deliberately rough: ~4 characters per token, sized from file
bytes (no file is opened), so it's fast on huge trees and good to an order of
magnitude — enough to decide "read now" vs "stage across quota resets."

Usage:
    python3 scripts/estimate_tokens.py [PATH]                  # size up a folder
    python3 scripts/estimate_tokens.py [PATH] --budget 200000  # compare to a token budget
"""
import argparse
import os
from collections import Counter
from pathlib import Path

# Text-like extensions worth counting; binary/media are skipped (you don't read them as text).
TEXT_EXT = {
    ".md", ".txt", ".rst", ".org", ".py", ".js", ".ts", ".json", ".yaml", ".yml",
    ".toml", ".csv", ".tsv", ".html", ".htm", ".xml", ".rtf", ".tex", ".srt",
    ".vtt", ".log", ".ipynb", ".docx", ".pdf",
}
SKIP_DIRS = {".git", ".claude", "__pycache__", "node_modules", ".venv", "venv"}
CHARS_PER_TOKEN = 4


def scan(root: Path):
    by_ext, bytes_by_ext = Counter(), Counter()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            ext = Path(name).suffix.lower()
            if ext not in TEXT_EXT:
                continue
            try:
                size = (Path(dirpath) / name).stat().st_size
            except OSError:
                continue
            by_ext[ext] += 1
            bytes_by_ext[ext] += size
    return by_ext, bytes_by_ext


def main() -> int:
    ap = argparse.ArgumentParser(description="Estimate tokens to read a source in full.")
    ap.add_argument("path", nargs="?", default=os.environ.get("SECOND_BRAIN_ROOT", "."))
    ap.add_argument("--budget", type=int, default=None,
                    help="token budget to compare against (e.g. a plan/session estimate)")
    args = ap.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"path not found: {root}")
        return 1

    by_ext, bytes_by_ext = scan(root)
    total_files = sum(by_ext.values())
    total_bytes = sum(bytes_by_ext.values())
    est_tokens = total_bytes // CHARS_PER_TOKEN

    print(f"Source: {root}")
    print(f"Text-like files: {total_files:,}   Total size: {total_bytes / 1_000_000:.1f} MB")
    print(f"Estimated tokens to read in full: ~{est_tokens:,}  (≈ bytes ÷ {CHARS_PER_TOKEN})")
    print(f"  ≈ {est_tokens / 200_000:.1f}× a 200K context window  ·  {est_tokens / 1_000_000:.2f}× a 1M window")
    if args.budget:
        pct = 100 * est_tokens / args.budget
        verdict = "fits — read it (cheap/fast model, in batches)" if pct <= 50 \
            else "too big for one go — stage it across quota resets"
        print(f"  ≈ {pct:.0f}% of a {args.budget:,}-token budget → {verdict}")
    if by_ext:
        print("By type (largest first):")
        for ext, n in by_ext.most_common(8):
            mb = bytes_by_ext[ext] / 1_000_000
            print(f"  {ext:8} {n:>6,} files   {mb:>7.1f} MB   ~{bytes_by_ext[ext] // CHARS_PER_TOKEN:>10,} tok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
