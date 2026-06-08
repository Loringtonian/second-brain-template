---
depth: 1
---
# Second Brain — Memory Index

> Your cross-session memory: durable facts, preferences, and rules an agent should
> recall **every** session. `CLAUDE.md` `@`-imports `MEMORY.md`, so it loads at Tier 0.
>
> **First run:** `cp MEMORY.example.md MEMORY.md` (just like `.env.example` → `.env`), then
> fill the slots below. `MEMORY.md` is gitignored — it accrues personal facts — so only this
> `.example` ships in the repo.
>
> **Two memory surfaces — and why this file exists:**
> - **This file (`MEMORY.md`)** — plain text in *your* repo. **Portable**: it travels with the
>   brain across machines, models, and agents. This is the owner-owned memory the `INTENT_SPEC`
>   promises ("plain files you own… your self-model comes with you").
> - **Claude Code's native memory** — lives at `~/.claude/projects/<project>/memory/MEMORY.md`,
>   *outside* the repo, written by the runtime and the `/breadcrumb` skill. Convenient, but
>   machine-local and not portable. Use it for runtime gotchas; use *this* file for what should
>   travel with the brain.
>
> Keep entries terse — one line each. **Safety / NEVER rules go FIRST** so they survive any
> context trim. Link related topic files with `[[name]]` as your memory grows.

## Hard rules / NEVERs (safety floor — keep first)
<!-- __FILL_FROM_USER__:memory_hard_rules — your inviolable rules, one terse line each
     (e.g. "never delete or overwrite my files without asking", "never post as me without review").
     /setup seeds these from your privacy + inviolable-rules answers. -->

## About me (pointers)
<!-- __FILL_FROM_USER__:memory_about_me — one-liners an agent should always know about you.
     For depth, point to Orientation_Docs/INTELLECTUAL_LANDSCAPE_LITE.md rather than restating it. -->

## Workflow preferences
<!-- __FILL_FROM_USER__:memory_workflow_prefs — how you like the agent to work
     (e.g. "be terse", "run commands yourself — don't hand me terminal steps", "ask before deploying"). -->
