#!/usr/bin/env python3
"""
build_brain_snapshot.py — build a concatenated snapshot of your Second Brain.  *** STUB ***

This is a placeholder. The `/load-brain` skill calls this script; until you implement
it, /load-brain will not be able to load your brain into context.

What this script should do when implemented:
  1. Walk your content folders (Inventions/, Journal_Intellectual/, Journal_Personal/,
     Writing_SciFi/, Predictions/, Writing_AllElse/, Health/, and any others you add)
     and collect all .md files recursively.
  2. Optionally skip sub-folders or file sets you want to exclude (e.g., bulk fiction
     sub-folders, external-source folders, AI-generated drafts). Document your policy
     in SETUP.md.
  3. Apply a light trim: strip redundant template sections (## Metadata, ## Classification,
     ## Source, ## Status) while keeping the meaningful content sections (## Summary,
     ## Keywords, ## Original Text, ## Connections, etc.).
  4. Concatenate all files into a single snapshot:
         .claude/brain_snapshot.md
     Prepend a FILE: marker before each file so the source is traceable.
  5. Generate the companion instruction file:
         .claude/brain_load_instructions.md
     This file contains the exact Read(file_path=..., offset=..., limit=...) calls
     that /load-brain will fire to page the snapshot into context. Chunk size must
     be ≤650 lines per call (~8,125 tokens, under the 10,000-token Read tool limit).
     Group calls into batches of ≤20 parallel reads.
  6. Print a summary: file count, line count, size, estimated tokens, per-folder
     breakdown, and the number of batches written to the instruction file.

Configuration:
  - List your content folders in ESSENTIAL_DIRS (or read them from SETUP.md / a
    config file). Do not hardcode absolute paths — use Path(__file__).parent.parent
    as the repo root.
  - Set CHUNK_SIZE = 650 and BATCH_SIZE = 20 (tested safe for the Claude Code Read tool).
  - Set a token budget constant and warn if the snapshot exceeds it.

See SETUP.md at the repo root for implementation guidance.

Output files (both gitignored by default):
  .claude/brain_snapshot.md
  .claude/brain_load_instructions.md
"""

import sys


def main() -> int:
    sys.stderr.write(
        "[build_brain_snapshot] stub — not yet implemented.\n"
        "Implement this script to enable /load-brain. See SETUP.md for guidance.\n"
    )
    return 2  # non-zero so callers (e.g. /load-brain) know the snapshot is unavailable


if __name__ == "__main__":
    raise SystemExit(main())
