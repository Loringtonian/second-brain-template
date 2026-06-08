#!/usr/bin/env python3
"""
PostToolUse hook: log per-tool-call size (chars in/out) to a JSONL trace.

Active only when the marker file /tmp/token_trace.active exists,
so this hook is a silent no-op during normal use. To start a trace:

    touch /tmp/token_trace.active

To stop:

    rm /tmp/token_trace.active

Trace lines land in /tmp/token_trace.jsonl (append-only, never rotated
automatically — rename or delete between runs to keep them separate).

Char counts are a stand-in for tokens (≈ chars/4 for English). Good enough
for relative attribution: which tool calls dominate the context budget.
"""
import json
import os
import sys
import time

MARKER = "/tmp/token_trace.active"
LOG = "/tmp/token_trace.jsonl"


def chars(x) -> int:
    if x is None:
        return 0
    if isinstance(x, str):
        return len(x)
    try:
        return len(json.dumps(x, default=str, ensure_ascii=False))
    except Exception:
        return 0


def main() -> None:
    if not os.path.exists(MARKER):
        return

    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw:
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    tool_name = data.get("tool_name")
    tool_input = data.get("tool_input") or {}
    tool_response = data.get("tool_response")

    entry = {
        "ts": time.time(),
        "tool_name": tool_name,
        "input_chars": chars(tool_input),
        "response_chars": chars(tool_response),
        "duration_ms": data.get("duration_ms"),
        "agent_id": data.get("agent_id"),
        "agent_type": data.get("agent_type"),
        "session_id": data.get("session_id"),
    }

    # Tool-specific identifiers so the analyzer can attribute cost
    if tool_name in ("Read", "Write", "Edit"):
        entry["file_path"] = tool_input.get("file_path")
        if tool_name == "Read":
            entry["offset"] = tool_input.get("offset")
            entry["limit"] = tool_input.get("limit")
    elif tool_name == "Bash":
        cmd = tool_input.get("command", "") or ""
        entry["command_head"] = cmd[:120]
    elif tool_name in ("Glob", "Grep"):
        entry["pattern"] = tool_input.get("pattern") or tool_input.get("query")
        entry["path"] = tool_input.get("path")
    elif tool_name in ("Task", "Agent"):
        entry["subagent_type"] = tool_input.get("subagent_type")
        entry["description"] = tool_input.get("description")
        # Prompt size is the most useful single number for subagent dispatch
        entry["prompt_chars"] = chars(tool_input.get("prompt"))

    try:
        with open(LOG, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        # Never break the user's session because trace logging failed
        pass


if __name__ == "__main__":
    main()
