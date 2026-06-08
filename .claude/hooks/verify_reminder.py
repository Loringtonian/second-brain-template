#!/usr/bin/env python3
"""
PostToolUse hook: Remind Claude to verify UI changes in browser-based projects.
Fast (<10ms) - checks file path against registry, emits directive if match.

Reads tool_input.file_path from JSON stdin (CC 2.1.x pattern, mirrors
validate_template_b.py). CLAUDE_FILE_PATH is dead since 2.1.x.
"""

import os
import sys
import json
import time
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "verify_registry.json"
COOLDOWN_DIR = Path("/tmp")
COOLDOWN_SECONDS = 60

# Web-relevant file extensions
WEB_EXTENSIONS = {".py", ".html", ".css", ".js", ".jinja2", ".ts", ".tsx", ".svelte", ".vue"}


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
    if not filepath:
        silent_exit()

    # Check extension
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in WEB_EXTENSIONS:
        silent_exit()

    # Load registry
    try:
        with open(REGISTRY_PATH) as f:
            registry = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        silent_exit()

    # Match against registered projects
    matched = None
    for project in registry.get("projects", []):
        if project["dir_prefix"] in filepath:
            matched = project
            break

    if not matched:
        silent_exit()

    # Cooldown: one reminder per project per 60 seconds
    cooldown_file = COOLDOWN_DIR / f"claude_verify_{matched['name']}.lock"
    try:
        if cooldown_file.exists():
            last_fire = cooldown_file.stat().st_mtime
            if time.time() - last_fire < COOLDOWN_SECONDS:
                silent_exit()
    except OSError:
        pass

    # Write cooldown timestamp
    try:
        cooldown_file.write_text(str(time.time()))
    except OSError:
        pass

    # Emit directive
    basename = os.path.basename(filepath)
    print(f"""UI FILE CHANGED in project: {matched['name']}
File: {basename}

VERIFY YOUR CHANGE (Browser Verification Protocol):
1. State your INTENT if you haven't already
2. Read VERIFY.md: {matched['verify_md']}
3. Ensure server running: lsof -i :{matched['port']} -t
4. Run verification: screenshot + assertions from VERIFY.md
5. If verification FAILS: diagnose, fix, re-verify (up to 3 attempts)
6. If verification PASSES: update VERIFY.md changelog if UI changed
7. Attach screenshot evidence before claiming "done"
""")


if __name__ == "__main__":
    main()
