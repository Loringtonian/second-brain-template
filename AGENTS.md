# AGENTS.md — For AI agents working in this repo (Codex and others)

> **Human?** You probably want **[START_HERE.md](START_HERE.md)** — a plain-English setup
> guide. This file is written for an AI coding agent that is **not** Claude Code.

## What this repo is

A **"second brain" template**: a personal knowledge base that an AI agent navigates using
tiered context loading, three document templates (A/B/C), reusable **skills**, and **hooks**.
It was built for **Claude Code**, so some mechanisms are Claude-specific. You can still operate
it — here's how.

## First — if you are running in a web portal / cloud sandbox, tell the user

If you are operating inside a **web portal or sandboxed cloud environment** — claude.ai on the
web, ChatGPT, or Codex cloud — **say this to the user before doing anything else:** this template
is designed for a **local** agent (the **Claude Desktop app** or the **Claude Code CLI**). A web
sandbox can't reliably run the template's skills, hooks, or Python helpers, so `/setup` may not
fire and onboarding can **silently underdeliver**. Recommend they switch to a local setup (see
`START_HERE.md`). Only continue in the web portal if they understand the limits and still choose to.

## If the user asks you to set it up

You do **not** have a `/setup` slash command (that is Claude Code-only). Instead:

1. **Read `.claude/skills/setup/SKILL.md`.** It is a complete, self-contained onboarding
   procedure — an interview that turns this blank template into the user's own brain.
2. **Read `CLAUDE.md`** (the repo's rules) and **`Orientation_Docs/ROUTER.md`** (how context is
   meant to load). Unlike Claude Code, you will not auto-load these, so read them explicitly.
3. **Run the interview yourself**, using your own way of asking the user questions. Go phase by
   phase, and **write their answers into the files the skill names** as you go.

The same pattern applies to any other skill: each `.claude/skills/<name>/SKILL.md` is a
procedure you can **read and execute manually**, even though you can't invoke it as `/<name>`.

## Hard rules (mirrored from CLAUDE.md — follow them)

Because you don't auto-load `CLAUDE.md`, its load-bearing rules are repeated here:

- **Preserve exact language.** Never paraphrase the owner's words — their keywords are how they
  find things again later.
- **Never rename files or folders.** Recall is keyword-based; renaming breaks it.
- **Ask before deleting or overwriting** anything, and verify the content is safe first.
- **Use the right template.** **A** = the owner's original thinking (kept verbatim).
  **B** = someone else's content (always attributed). **C** = AI synthesis made *from* their
  notes.
- **Show a note in full and get an explicit yes before creating it.**

## What is Claude-specific (may need a rebuild for your tool)

- **Skills** (`.claude/skills/`) are invoked as `/name` in Claude Code; for you they are
  procedures to read and run by hand.
- **Hooks** (`.claude/hooks/`) auto-fire only in Claude Code. Replicate their intent manually if
  you want them.
- **`@imports`** in `CLAUDE.md` and **silent tier-loading** via `ROUTER.md` are Claude
  behaviors — read those files yourself rather than expecting them to load.
- **Semantic search** needs an embedding engine (a stub ships at `scripts/sb_embed.py`); until
  it's built, use keyword search (`grep` / `rg`).

If you rebuild any of this for **Codex** or another tool, **please fork the repo and contribute
it back** — see **[CONTRIBUTING.md](CONTRIBUTING.md)**. This template is meant to grow into a
community project, and a working "other-tool" path is one of the most valuable contributions.

## Notes for Codex specifically

- Codex reads this **root `AGENTS.md`** automatically (it walks from the repo root down to your
  working directory). Everything you need is here.
- A second, narrower `AGENTS.md` lives in `.claude/skills/` and is read **only when you are
  working inside that folder** — treat it as optional, scoped guidance, not a second always-on
  instruction file.
- The Codex CLI can create a virtual environment and `pip install -r requirements.txt` to make
  the bundled Python helpers run; the cloud sandbox can too (its setup phase has network access).
