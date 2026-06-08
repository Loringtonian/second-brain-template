#!/usr/bin/env python3
"""
sb_embed.py — semantic search over your Second Brain.  *** STUB ***

This is a placeholder. The skills `/semantic-search`, `/verify-idea`, `/explore-second-brain`,
and `/connection-finder` call this CLI; until you implement it they fall back to `grep`
keyword search, so they still work — just less semantically.

To make it real, build a CLI that embeds your `.md` files and supports these subcommands:

    python3 scripts/sb_embed.py index [--rebuild]          # build/refresh the embedding index
    python3 scripts/sb_embed.py search "query" [--json]    # top-k matches by meaning
    python3 scripts/sb_embed.py verify "idea"  [--json]    # duplicate check (DUPLICATE/OVERLAP/NOT_FOUND)
    python3 scripts/sb_embed.py similar path.md [--json]   # files semantically near an existing one
    python3 scripts/sb_embed.py stats [--json]             # index health

A simple implementation: embed each file with sentence-transformers (e.g. BAAI/bge-large-en-v1.5),
cache the vectors, and cosine-rank against the query embedding. See SETUP.md at the repo root.
"""

import sys


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "(none)"
    sys.stderr.write(
        f"[sb_embed] stub — '{cmd}' not implemented. Semantic search is disabled; "
        "callers should fall back to grep. See SETUP.md to enable it.\n"
    )
    return 2  # non-zero so callers know the helper is unavailable


if __name__ == "__main__":
    raise SystemExit(main())
