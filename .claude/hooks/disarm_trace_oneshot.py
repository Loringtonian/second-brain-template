#!/usr/bin/env python3
"""
Stop hook: end-of-turn cleanup for one-shot token traces.

If the trace marker /tmp/token_trace.active exists AND its content
starts with "oneshot|", this hook:

  1. Archives /tmp/token_trace.jsonl → /tmp/token_trace.<ts>.jsonl
  2. Removes the marker.
  3. Writes a one-line summary to stderr so the next prompt sees it.

Manually-armed traces (marker without "oneshot|" prefix) are left alone.
"""
import os
import shutil
import sys
import time

MARKER = "/tmp/token_trace.active"
LOG = "/tmp/token_trace.jsonl"


def main() -> None:
    if not os.path.exists(MARKER):
        return
    try:
        with open(MARKER) as f:
            content = f.read().strip()
    except OSError:
        return

    if not content.startswith("oneshot"):
        return  # manual arming — don't touch

    archived = None
    if os.path.exists(LOG):
        ts = int(time.time())
        base, ext = os.path.splitext(LOG)
        archived = f"{base}.{ts}{ext}"
        try:
            shutil.copy(LOG, archived)
            os.unlink(LOG)
        except OSError:
            archived = None

    try:
        os.unlink(MARKER)
    except OSError:
        pass

    if archived:
        sys.stderr.write(
            f"[trace_tokens] one-shot trace archived to {archived}. "
            f"Run: python3 .claude/hooks/analyze_token_trace.py {archived}\n"
        )


if __name__ == "__main__":
    main()
