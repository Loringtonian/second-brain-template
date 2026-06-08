---
name: setup
description: >-
  Onboard a human into THEIR own second brain — the guided interview that turns this blank
  template into their personalized system. Use when the user says "set this up", "let's set it
  up", "set up my second brain", "personalize", "personalise", "make this mine", "onboard me",
  "help me fill this in", "walk me through PERSONALIZE", or starts a fresh session wanting to
  begin. Drives the whole __FILL_FROM_USER__ fill-in via an interview. Resumable — pick up where
  you left off. NOT for ingesting content (use /ingest-brain-dump) — this is first-run setup.
allowed-tools: Read, Edit, Write, Bash, AskUserQuestion, Glob, Grep
---

# Setup — Onboarding Interview

You are the onboarding interviewer. Your job is to turn this blank template into the user's own
second brain by **interviewing them** and writing their answers into the scaffolds. The repo ships
full of `__FILL_FROM_USER__` markers; this skill fills the load-bearing ones in a sensible order so
the brain is useful within ~20 minutes and grows from there.

## THE HARD RULE — interview with the tool, not with prose

**Use the `AskUserQuestion` tool for every question below.** Do not ask questions as plain chat
text — people answer a clean multiple-choice/short-answer prompt far better than a wall of prose.
Batch 2–4 related questions per `AskUserQuestion` call. Offer concrete options *and* rely on the
free-text "Other" for their own words. After each phase, **write their answers into the files**
(don't just collect them), confirm what you wrote, then move to the next phase. You do not have to
finish in one sitting — say so, and this skill can resume.

> If you find yourself typing "What would you like…?" into the chat, stop and use AskUserQuestion instead.

## Before you start

1. `grep -rn "__FILL_FROM_USER__" .` to see every fill-in site, and skim `PERSONALIZE.md` (the worksheet).
2. Tell the user, briefly: the brain ships blank by design; you'll interview them; ~20 min gets a
   working core (purpose + who-they-are), the rest accretes. Then begin Phase 1.

## The interview (in order — purpose first)

### Phase 0 — Environment bootstrap (make the brain runnable)
Before interviewing, get the tooling working so the brain can run its own scripts (use Bash):
- **Verify Python and Git** — `python3 --version` and `git --version`. If either is missing, give the
  user the one-line install for their OS and pause until it's present.
- **Create a virtualenv + install dependencies** — from the repo root:
  `python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`. This makes the
  bundled scripts (`/remove-watermark`, the `/nano-banana` image skills) run out of the box.
- Do this automatically; only surface a manual step if something genuinely can't be set up for them
  (no system Python, a wheel that won't build). Then continue to the interview.

### Phase 1 — Purpose: what is this FOR?
The most important question, and the one most setups skip. Ask (AskUserQuestion):
- **"What do you want this second brain to DO for you?"** (e.g. never lose an idea / be a thinking
  partner / draft in your voice / track projects to the finish / remember your life / prep for
  agent-to-agent use). Multi-select + Other.
- **"What would make it a clear win 3 months from now?"**
Write the answer into `CLAUDE.md` (`__FILL_FROM_USER__:owner_one_liner` if it doubles as identity),
the **"WHAT THIS BRAIN IS FOR"** section of `Orientation_Docs/INTELLECTUAL_LANDSCAPE_LITE.md`, and the
**Owner Intent** section of `INTENT_SPEC.md` (`brain_purpose`, `owner_goals`, `success_criteria`).

### Phase 2 — Gaps: what should it shore up?
A second brain earns its keep by filling *your* gaps. Ask:
- **"What are the weaknesses or blind spots you want this brain to help with?"** (e.g. start things
  but don't finish / forget good ideas / scattered focus / poor recall of past decisions / lose
  track of people). Multi-select + Other.
Write into `Orientation_Docs/INTELLECTUAL_LANDSCAPE_LITE.md` ("GAPS IT FILLS"), `INTENT_SPEC.md`
(`gaps_filled`, `owner_non_goals`), and reflect it in `Orientation_Docs/COGNITIVE_PROFILE.md`
(`strengths_and_friction`).

### Phase 3 — Who you are (identity-lite)
Fill the always-loaded identity doc. Ask, a few at a time:
- one-line self-description; background/throughline; 3–6 core beliefs ("what do you believe that
  most people you know don't?"); recurring obsessions; what kind of idea makes you lean in vs tune
  out; your active projects (name + one line each).
Write into `Orientation_Docs/INTELLECTUAL_LANDSCAPE_LITE.md` (and seed the fuller
`INTELLECTUAL_LANDSCAPE.md` if they want to go deep). Preserve their exact words — no paraphrasing.

### Phase 4 — Voice
Ask them to paste **3–10 short pieces of their own writing** they feel "sound like me," and what to
avoid. Extract the patterns into `Orientation_Docs/VOICE_GUIDE.md` (examples teach voice better than
rules). **Strongly push them to make voice a default input** — talking is the highest-bandwidth,
most human way to feed a brain, and the easiest habit to make a second brain stick. Recommend
**superwhisper** (Mac, subscription), **Claude Code's native voice input** (built in), or **Wispr
Flow** (cross-app) — see the "Capture by voice" block in `SETUP.md`. Ask (AskUserQuestion) whether
they already dictate; if not, get them set up with one of those.

### Phase 5 — Tools, APIs & "superpowers"
This brain gets much stronger with a few external tools — none ship in the repo. Your job here is
to **show them what's possible and match tools to how they actually work**, not to install
everything. **Read the "Companion tools" catalog in `SETUP.md` first**, then walk them through it:

- **Ask what they do** (AskUserQuestion, multi-select): which of these are part of their world —
  *coding & shipping · media or podcasts · deploying services · 3D / CAD · messaging capture ·
  image generation · semantic search over their own notes*? Their answers tell you which catalog
  rows matter, so you recommend the right tools instead of dumping the whole list.
- **For each workflow they pick, surface the matching tool** and help set it up: the key in `.env`
  (`cp .env.example .env`), the install one-liner, or the connector toggle. (image gen →
  `GEMINI_API_KEY`; coding → gstack via `./setup`, needs Bun; media → ffmpeg + yt-dlp; deploys →
  fly + tailscale; 3D → Blender / ForgeCAD; messaging → Hermes.)
- **Strongly suggest the always-useful core** regardless of workflow: **gstack** (a virtual eng
  team), a **headless browser** (browser-harness or gstack's `/browse`, which powers the `$B`
  protocol in `CLAUDE.md`), an **embedding engine** for semantic search, and **ripgrep + jq**.
- **The connectors** (Gmail / Drive / Calendar / Notion) are zero-install — mention they can toggle
  them on in Claude settings to pull their real life into the brain.
- **"Any 'superpowers' (custom skills) you want wired in?"** Note them under `CLAUDE.md`
  `__FILL_FROM_USER__:domain_skills` and in `SETUP.md`.

Write keys into `.env` (never commit it); never auto-install — recommend, link, and let them run it.
Record which tools they chose and which credentials they'll wire (names only — values live in `.env`)
in `INTENT_SPEC.md` (`toolchain`, `credentials_to_wire`).

### Phase 6 — Your machine & environment (calibrates /free-memory + /disk-cleanup)
The resource skills work much better when they know your hardware — and your phone shapes how you
capture. Ask (AskUserQuestion, batch 2–4):
- **Machine + RAM + OS** — make/chip, how much RAM, which OS. (RAM size is what defines "memory
  pressure," so `/free-memory` needs it.)
- **Disposable vs interactive processes** — which long-running servers are safe to kill because they
  just relaunch (local model servers, dev servers, build watchers) vs which apps are interactive and
  must *never* be auto-killed (your editor, agent CLI, browser).
- **Disk + drives** — internal disk size, and any external drive you use for archival (that's what
  `/disk-cleanup` Phase 2 tars big folders to).
- **Phone** — iOS or Android (it shapes your capture / inbox tooling and which apps you sync from).
- **Other tooling** — GPUs, key CLIs, local model stores — anything the agent should be
  resource-aware of.

Write the answers into `CLAUDE.md` `__FILL_FROM_USER__:machine_profile`. If they named a *production*
local model that must never be deleted, also record it at the `disk-cleanup` skill's
`__FILL_FROM_USER__:production-ollama-model`. Then tell them: `/free-memory` and `/disk-cleanup` both
**ship working on safe defaults**, and this profile is what makes them precise (and safe to let run on
your real processes / disk).

### Phase 7 — Privacy depth (define your levels)
Read `Orientation_Docs/PRIVACY_DEPTH.md` with them, then run its calibration loop:
- Ask for their **register test** in one line ("what makes something feel too private to share?").
- Hand-rule ~6 of their own files/topics across **D1–D5** (AskUserQuestion per file: which level?),
  surfacing the drivers (privacy/intimacy, strategic value) and the D4↔D5 register rule.
- Record their rulings at `__FILL_FROM_USER__:depth_calibration` in `PRIVACY_DEPTH.md`, and their
  one-line register test in `INTENT_SPEC.md` (`privacy_register`).
- Show them `scripts/stamp_depth.py <file> <N>` so they can stamp as they create files, and note the
  publish rule (ship depth ≤ 2, review 3, keep 4–5 private).

### Phase 8 — Folders
The content folders ship as empty stubs. Ask (AskUserQuestion) which fit their life — prune the ones
they won't use, and capture any custom folders at `FOLDER_ORIENTATION.md` `__FILL_FROM_USER__:custom_folders`.

## Finishing
- Regenerate the worksheet so line numbers stay honest (re-scan `__FILL_FROM_USER__` across the tree
  and rewrite `PERSONALIZE.md`), then show the user what's still unfilled.
- Tell them the routing already works now, and that they can deepen `INTELLECTUAL_LANDSCAPE.md`,
  `VOICE_GUIDE.md`, and the depth calibration any time by re-running `/setup`.
- Hand off to `/ingest-brain-dump` for their first real content.

## Verification (before you call setup "done for now")
Confirm: you used AskUserQuestion (not prose) for every phase you ran; Phase 1 (purpose) and Phase 2
(gaps) were asked and written; the owner one-liner + landscape-lite have real content; any API keys
they gave went into `.env` (gitignored), not into a tracked file.
