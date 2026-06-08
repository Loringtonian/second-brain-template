#!/usr/bin/env python3
"""
PostToolUse hook: Mark files as pending embedding update.
Fast (<1ms) - just appends to a pending file.
Actual rebuild happens on next search (searcher.py::check_and_rebuild_if_pending).

Reads tool_input.file_path from JSON stdin (CC 2.1.x pattern, mirrors
validate_template_b.py). CLAUDE_FILE_PATH is dead since 2.1.x.
"""

import json
import sys
from pathlib import Path

PENDING_FILE = Path("$SECOND_BRAIN_ROOT/.claude/embeddings/pending.txt")
SECOND_BRAIN_PATH = "$SECOND_BRAIN_ROOT/"


def silent_exit():
    sys.exit(0)


def main():
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw:
        silent_exit()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        silent_exit()

    if data.get("tool_name") not in ("Write", "Edit"):
        silent_exit()

    filepath = (data.get("tool_input") or {}).get("file_path") or ""
    if not filepath.endswith(".md"):
        silent_exit()
    if SECOND_BRAIN_PATH not in filepath:
        silent_exit()

    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PENDING_FILE, "a") as f:
        f.write(filepath + "\n")


if __name__ == "__main__":
    main()
