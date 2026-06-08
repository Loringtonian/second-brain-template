#!/usr/bin/env python3
"""
PostToolUse hook: validate Template B files written under
External_Sources/podcast_clips/ and append the result to the tool
output the model sees.

Fires only on Write/Edit. Silent no-op for other tools/paths.
Smoke-test markers (filenames starting with `_`) are skipped.
"""
import sys
import os
import json
import subprocess

VALIDATOR = "$SECOND_BRAIN_ROOT/.claude/scripts/validate_template.py"
TARGET_SUBSTR = "External_Sources/podcast_clips/"


def emit(obj):
    print(json.dumps(obj))


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

    file_path = (data.get("tool_input") or {}).get("file_path") or ""
    if TARGET_SUBSTR not in file_path or not file_path.endswith(".md"):
        silent_exit()

    base = os.path.basename(file_path)
    if base.startswith("_"):
        silent_exit()

    if not os.path.exists(file_path):
        silent_exit()

    try:
        proc = subprocess.run(
            ["python3", VALIDATOR, file_path, "--json"],
            capture_output=True, text=True, timeout=10,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        silent_exit()

    try:
        result = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        silent_exit()

    valid = bool(result.get("valid"))
    template = result.get("template", "?")
    issues = result.get("issues", []) or []
    warnings = result.get("warnings", []) or []

    if valid:
        note = f"✓ Template {template} valid (auto-validated)"
        if warnings:
            note += " — warnings: " + "; ".join(warnings[:3])
    else:
        note = f"⚠ Template {template} validation FAILED — issues: " + "; ".join(issues[:5])

    appendix = f"[validate_template_b] {note}"

    # additionalContext appends to model context without replacing tool output.
    # updatedToolOutput replaces it (2.1.121+). Emit both so whichever the
    # runtime honors becomes visible.
    original = f"File written successfully at: {file_path}"
    emit({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": appendix,
            "updatedToolOutput": f"{original}\n\n{appendix}",
        }
    })


if __name__ == "__main__":
    main()
