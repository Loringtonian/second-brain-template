#!/usr/bin/env python3
"""
PreCompact hook (type: command): durable, model-free session checkpoint.

Why this exists:
  The PreCompact `type: prompt` hook that asks the model to run /wind-down only
  works in the interactive REPL. In autonomous / headless runs the model gets no
  turn at compaction, so that hook dies with "Prompt stop hooks are not yet
  supported outside REPL" and long sessions compact with NO durable checkpoint.
  A `type: command` hook ALWAYS runs (interactive + headless) and needs no model,
  so it can guarantee a durable artifact at every compaction.

What it does (pure I/O, no model, no git mutation):
  Reads the hook JSON from stdin — {session_id, transcript_path, trigger, cwd}.
  1. Copies the full session transcript JSONL (the complete in-flight session
     state) to ~/.claude/wind_down_checkpoints/<UTC-ts>_<sid8>_<trigger>.jsonl
  2. Writes a sidecar <...>.meta.json manifest: timestamp, session, trigger,
     git branch/HEAD/status-short, and transcript line count.
  Nothing is ever lost at compaction: the raw session is preserved on disk and a
  resume-pointer + git snapshot is recorded, regardless of run mode.

Safety:
  - Never blocks compaction: every failure is swallowed; the process always
    exits 0.
  - Never mutates git (no add/commit) — the shared working tree + git-etiquette
    rules forbid autonomous staging. This hook only reads git state.
  - Never deletes anything. Checkpoints accumulate in
    ~/.claude/wind_down_checkpoints/; prune that dir manually if disk is tight
    (kept deletion out of the hook deliberately — a misfiring hook must not be
    able to remove data).

Mirrors the existing command-hook pattern (arm_trace_oneshot.py reads stdin
JSON; disarm_trace_oneshot.py does scoped file I/O).
"""
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CHECKPOINT_DIR = Path.home() / ".claude" / "wind_down_checkpoints"
DEFAULT_REPO = "$SECOND_BRAIN_ROOT"


def _git(cwd: str, args: list[str]) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", cwd, *args],
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    transcript_path = data.get("transcript_path") or ""
    session_id = data.get("session_id") or "unknown"
    trigger = data.get("trigger") or "unknown"
    cwd = data.get("cwd") or DEFAULT_REPO

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{ts}_{str(session_id)[:8]}_{trigger}"

    transcript_copy = None
    transcript_lines = None
    src = Path(transcript_path) if transcript_path else None
    if src and src.is_file():
        dest = CHECKPOINT_DIR / f"{stem}.jsonl"
        try:
            shutil.copy2(src, dest)
            transcript_copy = str(dest)
            with dest.open("r", errors="replace") as fh:
                transcript_lines = sum(1 for _ in fh)
        except Exception:
            transcript_copy = None

    manifest = {
        "captured_at_utc": ts,
        "session_id": session_id,
        "trigger": trigger,
        "transcript_source": transcript_path,
        "transcript_copy": transcript_copy,
        "transcript_lines": transcript_lines,
        "git_branch": _git(cwd, ["rev-parse", "--abbrev-ref", "HEAD"]),
        "git_head": _git(cwd, ["rev-parse", "HEAD"])[:12],
        "git_status_short": _git(cwd, ["status", "--short"]),
    }
    try:
        (CHECKPOINT_DIR / f"{stem}.meta.json").write_text(
            json.dumps(manifest, indent=2) + "\n"
        )
    except Exception:
        pass

    # If a model loop is present (REPL), nudge toward the richer semantic pass.
    if transcript_copy:
        sys.stderr.write(
            f"[precompact_checkpoint] durable checkpoint saved -> {transcript_copy} "
            f"(+ .meta.json). In REPL, run /wind-down for the semantic checkpoint.\n"
        )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
