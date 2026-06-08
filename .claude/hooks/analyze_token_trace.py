#!/usr/bin/env python3
"""
Read /tmp/token_trace.jsonl and print where context tokens went.

Usage: python3 .claude/hooks/analyze_token_trace.py [path-to-jsonl]
"""
import collections
import json
import sys
from pathlib import Path

DEFAULT_LOG = Path("/tmp/token_trace.jsonl")


def fmt(n: int) -> str:
    return f"{n:>12,}"


def label_for(entry: dict) -> str:
    t = entry["tool_name"]
    if t in ("Read", "Write", "Edit"):
        path = entry.get("file_path") or ""
        # Trim the long Second_Brain prefix for readability
        path = path.replace("$SECOND_BRAIN_ROOT/", "SB/")
        path = path.replace("$SECOND_BRAIN_ROOT/", "ROOT/")
        return path
    if t == "Bash":
        return entry.get("command_head", "")
    if t in ("Glob", "Grep"):
        return f"{entry.get('pattern', '')} @ {entry.get('path', '')}"
    if t in ("Task", "Agent"):
        return f"{entry.get('subagent_type', '?')}: {entry.get('description', '')}"
    return ""


def main():
    args = sys.argv[1:]
    session_filter = None
    log_arg = None
    for a in args:
        if a.startswith("--session="):
            session_filter = a.split("=", 1)[1]
        else:
            log_arg = a
    log_path = Path(log_arg) if log_arg else DEFAULT_LOG
    if not log_path.exists():
        print(f"No trace file at {log_path}")
        sys.exit(1)

    raw_entries = []
    for line in log_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            raw_entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    if not raw_entries:
        print("Trace file is empty.")
        sys.exit(1)

    # Show session breakdown first (helpful when multiple CC sessions are open)
    sessions = collections.Counter(e.get("session_id") for e in raw_entries)
    if len(sessions) > 1 and not session_filter:
        print(f"Trace contains {len(sessions)} concurrent sessions:")
        for sid, n in sessions.most_common():
            sid_show = sid or "(none)"
            sess_resp = sum(e.get("response_chars", 0) for e in raw_entries if e.get("session_id") == sid)
            print(f"  {sid_show}  {n:>4d} calls  {fmt(sess_resp)} resp chars")
        print()
        print("To restrict to one session, re-run with --session=<id>")
        print()

    entries = (
        [e for e in raw_entries if e.get("session_id") == session_filter]
        if session_filter else raw_entries
    )
    if not entries:
        print(f"No entries match session={session_filter}")
        sys.exit(1)

    total_resp = sum(e.get("response_chars", 0) for e in entries)
    total_input = sum(e.get("input_chars", 0) for e in entries)
    print(f"Trace: {log_path}")
    print(f"Tool calls: {len(entries)}")
    print(f"Total tool input chars:    {fmt(total_input)}  (~{total_input//4:,} tokens)")
    print(f"Total tool response chars: {fmt(total_resp)}  (~{total_resp//4:,} tokens)")
    print(f"Combined: ~{(total_resp + total_input)//4:,} tokens")
    print()

    # By tool
    by_tool: dict[str, dict] = collections.defaultdict(
        lambda: {"count": 0, "response_chars": 0, "input_chars": 0}
    )
    for e in entries:
        t = e.get("tool_name") or "?"
        by_tool[t]["count"] += 1
        by_tool[t]["response_chars"] += e.get("response_chars", 0)
        by_tool[t]["input_chars"] += e.get("input_chars", 0)

    print("By tool (sorted by response chars):")
    print(f"  {'tool':10s}  {'calls':>6s}  {'in chars':>12s}  {'resp chars':>12s}  {'% of resp':>10s}")
    for tool, s in sorted(by_tool.items(), key=lambda x: -x[1]["response_chars"]):
        pct = 100 * s["response_chars"] / total_resp if total_resp else 0
        print(f"  {tool:10s}  {s['count']:>6d}  {fmt(s['input_chars'])}  {fmt(s['response_chars'])}  {pct:>9.1f}%")
    print()

    # Main vs subagent
    main_resp = sum(e.get("response_chars", 0) for e in entries if not e.get("agent_id"))
    sub_resp = sum(e.get("response_chars", 0) for e in entries if e.get("agent_id"))
    main_n = sum(1 for e in entries if not e.get("agent_id"))
    sub_n = sum(1 for e in entries if e.get("agent_id"))
    print("Main thread vs subagent:")
    print(f"  main      {main_n:>6d} calls  {fmt(main_resp)}  ({100*main_resp/total_resp:.1f}%)")
    print(f"  subagent  {sub_n:>6d} calls  {fmt(sub_resp)}  ({100*sub_resp/total_resp:.1f}%)")
    print()

    # Top responses
    print("Top 15 single tool responses by size:")
    print(f"  {'resp chars':>12s}  {'tool':10s}  agent  label")
    top = sorted(entries, key=lambda e: -e.get("response_chars", 0))[:15]
    for e in top:
        agent = "sub" if e.get("agent_id") else "main"
        print(f"  {fmt(e.get('response_chars', 0))}  {e.get('tool_name', '?'):10s}  {agent:5s}  {label_for(e)[:80]}")


if __name__ == "__main__":
    main()
