#!/usr/bin/env python3
"""
UserPromptSubmit hook: one-shot arm of the token trace.

When the user invokes a skill you want to profile (e.g. process-content) AND the sentinel file
/tmp/token_trace.next_oneshot exists, this hook:

  1. Creates /tmp/token_trace.active with content "oneshot|<ts>"
     so trace_tokens.py starts logging.
  2. Deletes the sentinel so subsequent runs aren't auto-armed.

The companion Stop hook (disarm_trace_oneshot.py) detects the "oneshot|"
prefix and archives + removes the marker when the agent's turn ends.

Manual arming via `touch /tmp/token_trace.active` (no oneshot prefix)
is unaffected by either hook.
"""
import json
import os
import re
import sys
import time

SENTINEL = "/tmp/token_trace.next_oneshot"
MARKER = "/tmp/token_trace.active"

# Match the user invoking the skill you want to profile (here: process-content).
# Adapt this pattern to whichever skill or phrase you want to auto-trace.
PATTERN = re.compile(
    r"(?:^|[\s/])(?:process[- ]?content|make files from this)\b",
    re.IGNORECASE,
)


def main() -> None:
    # Sentinel must already exist — this is one-shot, not always-on.
    if not os.path.exists(SENTINEL):
        return

    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw:
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    prompt = data.get("prompt") or ""
    if not PATTERN.search(prompt):
        return

    # Don't clobber an existing manually-armed marker.
    if os.path.exists(MARKER):
        try:
            os.unlink(SENTINEL)
        except OSError:
            pass
        return

    try:
        with open(MARKER, "w") as f:
            f.write(f"oneshot|{int(time.time())}\n")
        os.unlink(SENTINEL)
    except OSError:
        return


if __name__ == "__main__":
    main()
