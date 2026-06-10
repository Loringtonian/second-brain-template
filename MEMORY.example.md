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
> Keep entries terse — one line each. **Safety / NEVER rules go FIRST** so that if memory is ever
> trimmed to fit context, the cold tail drops — never a safety rule. Link related topic files with
> `[[name]]` as your memory grows.
>
> **Hygiene (so memory stays usable at scale):**
> - **One line per entry here; detail lives in a linked topic file** — never expand an index line back
>   into a paragraph. As a fact grows, move its body to a `topic-file.md` and leave a one-line pointer.
> - **Keep this index small.** Claude Code loads it every session; treat **~200 lines / ~25 KB** as a
>   soft cap and prune the cold tail past it. A short, ordered index beats a long one the agent skims.
> - **Live project state does NOT belong here** — it goes in that project's `STATE.md`/`TODO`. Memory
>   holds durable *rules and patterns*, not changing status.

## Hard rules / NEVERs (safety floor — keep first)
<!-- __FILL_FROM_USER__:memory_hard_rules — your inviolable rules, one terse line each
     (e.g. "never delete or overwrite my files without asking", "never post as me without review").
     /setup seeds these from your privacy + inviolable-rules answers. -->

## Ambient — every reply / turn (sensible defaults — edit or delete freely)
<!-- These are universal good-practice defaults seeded so the agent behaves well from day one.
     They are NOT inviolable — change the wording, drop what you disagree with, add your own at
     __FILL_FROM_USER__:memory_ambient_rules below. -->
- **Be terse and meaning-dense.** Lead with the answer; expand only when asked. Skip preamble/postamble.
- **Give full, clickable file paths** (absolute) so they resolve in the editor.
- **Decisions and options go in chat, with the content in front of you** — not parked in a doc to read later.
- **Pose open questions directly** (ask them), rather than burying them in a file.
- **Don't say "done" while async work is in flight** — report progress, projected result, and an ETA.
- **Verify a fix before claiming it** — and make sure it generalizes; never tune to pass one example.
- **Independent work runs in parallel by default.**
- **For clearly-scoped, reversible actions, act and report** — don't hand over a menu for trivial calls.
<!-- __FILL_FROM_USER__:memory_comms_style — your comms-style answers from /setup Phase 3.5 land here
     (reply length/density, pushback vs execute, decisions in chat vs docs). Mirrored from
     INTENT_SPEC.md `agent_comms_style`; this copy is the one that loads every session. -->
<!-- __FILL_FROM_USER__:memory_ambient_rules — add your own every-reply preferences here. -->

## About me (pointers)
<!-- __FILL_FROM_USER__:memory_about_me — one-liners an agent should always know about you.
     For depth, point to Orientation_Docs/INTELLECTUAL_LANDSCAPE_LITE.md rather than restating it. -->

## Workflow preferences
<!-- __FILL_FROM_USER__:memory_workflow_prefs — how you like the agent to work
     (e.g. "be terse", "run commands yourself — don't hand me terminal steps", "ask before deploying"). -->
