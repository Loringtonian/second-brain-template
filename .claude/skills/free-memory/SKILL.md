---
name: free-memory
description: >-
  On-demand RAM reclamation for your machine. Audits memory-hungry processes
  (footprint-accurate, counting swapped/compressed pages), then presents them in
  four buckets — KILL CANDIDATES (orphan/restartable servers, e.g. a forgotten
  local-model server or dev server), REVIEW (uncertain), INTERACTIVE sessions
  (your editor / agent CLI / browser — surfaced for eyeballing, never auto-killed),
  and MANAGED (supervised services, left alone). Kills NOTHING without explicit
  per-item confirmation, then re-checks memory and reports what was reclaimed.
  Use when the user says "/free-memory", "free up memory", "free up some ram",
  "what's eating my memory", "my machine is slow/swapping", "kill stale
  processes", or "clean up processes". **Calibrate it to your machine via /setup**
  (RAM size, which servers are disposable, which apps are interactive) — it works
  with safe defaults until then.
user_invocable: true
allowed_tools:
  - Read
  - Bash
  - AskUserQuestion
---

# free-memory

On-demand memory reclamation. The detector is read-only; **this skill kills only
with the user's explicit confirmation** (the default kill policy — change it in
your machine profile at `/setup`).

> **Calibrate this at `/setup`.** This skill is sharper when it knows *your*
> machine: how much RAM you have (so it knows what "pressure" means), which
> long-running servers are disposable (safe to kill — they relaunch), and which
> apps are interactive (never auto-killed). The `/setup` machine-&-environment
> phase records that at `__FILL_FROM_USER__:machine_profile` (in `CLAUDE.md`).
> Until you calibrate, it uses conservative defaults and confirms before doing
> anything. macOS commands are shown below; on Linux substitute the equivalents
> (`free -m`, `ps`/`smem`, `systemctl`) during setup.

## Why this exists

On macOS, `ps`/RSS lies under memory pressure — a multi-GB swapped-out process
can report a few MB of RSS. The audit leads with `top -l 1 -stats pid,mem`, which
counts swapped/compressed pages (phys_footprint), so the real hogs can't hide.

## Hard rules

- **Always confirm before killing.** Present each candidate (PID, footprint, age,
  cwd, full command). Kill only the PIDs the user names or approves. No "kill all
  candidates" shortcut unless the user says so explicitly this run.
- **Never propose killing INTERACTIVE sessions** (your agent CLI, editor, browser,
  terminal). They sit at 0% CPU because they are *waiting for the human*, not
  because they are dead. Surface them with cwd + age + ppid so the user can spot a
  genuinely abandoned tab, but they decide — you never auto-list them as kill
  targets.
- **Never kill MANAGED (supervised) services** — they are supposed to be up and
  will often just respawn.
- **Never kill the current session.** Before killing any agent-CLI PID the user
  approved, confirm it is not this process (`echo $PPID` / compare).
- Graceful first: `kill <pid>` (SIGTERM), wait ~3s, only `kill -9` if it survives.

## Procedure

1. **Audit (read-only, ~1s).** List the real memory hogs by footprint:
   ```bash
   top -l 1 -stats pid,mem,command -o mem | head -25
   top -l 1 -n 0 | grep PhysMem        # the live pressure line
   ```
   Then sort each hog into the four buckets using the machine profile: KILL
   CANDIDATES (disposable servers the user listed), MANAGED (their supervised
   services), INTERACTIVE (their editor/agent/browser), REVIEW (everything else).
   *(Optional: a fuller footprint-audit script can be added during `/setup` — the
   inline `top` audit above is enough for the common case.)*
2. **Present in chat.** Show the KILL CANDIDATES and any stale INTERACTIVE
   sessions verbatim — PID, footprint (GB), age, cwd, command. This is a decision
   surface; put the content in front of the user, don't summarize it away.
3. **Confirm.** For KILL CANDIDATES, ask which to kill (default-suggest the idle,
   old, orphan-server ones — they restart trivially). For stale interactive tabs,
   only act on ones the user explicitly names.
4. **Kill (graceful).** For each approved PID: `kill <pid>`; sleep 3; if still
   alive, `kill -9 <pid>`. Verify each is gone.
5. **Re-check + report.** Re-run the PhysMem line
   (`top -l 1 -n 0 | grep PhysMem`) and report before/after compressor + unused,
   and total GB reclaimed.

## Notes

- **The biggest interactive app is often the real lever.** If your editor or
  browser is the largest footprint (common after days of uptime), the fix is
  restarting *that app* or rebooting — not killing background processes. Say so.
- **A periodic notify-only check** (e.g. a launchd/systemd job that messages you
  when memory crosses a threshold) pairs well with this skill — wire it up at
  setup if you want it. On macOS, keep any such script *off* TCC-protected dirs
  like `~/Desktop` (launchd can't exec there); put it under `~/.local/` or similar.
- Killing a restartable server (local model server, dev server, build watcher) is
  fully reversible — relaunch when needed. List those servers in your machine
  profile so this skill knows they're safe candidates.
