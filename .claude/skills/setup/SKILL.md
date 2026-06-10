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
   working core (purpose + who-they-are), the rest accretes. **Reassure them they need no technical
   knowledge — you handle the setup steps (installing helpers, creating files); they just answer
   questions.** Then begin Phase 1.

## Setup levels (run Core now; go deeper later)

Setup is staged so the owner gets a working brain fast and deepens when they want. Read the invocation arg:

- **`/setup` → Core (~10–20 min):** Phases 0 (env bootstrap), 1 (purpose), 2 (gaps), 3 (who you are),
  3.5 (how the agent should talk to you), 7 (privacy depth — at least the register test), 10 (first
  loop — one real capture, end to end), then Finishing. This alone is a usable, personalized brain
  that has already run its core loop once.
- **`/setup voice` → Voice & sources:** Phases 4 (voice guide), 5 (tools/APIs/passive capture),
  6 (machine + preferred mobile interaction), 8 (folders & ingestion scope → hand off to `/mine`).
- **`/setup deep` → Deep personalization:** Phase 9 (make the spec yours), fleshing out
  `INTELLECTUAL_LANDSCAPE.md` + `COGNITIVE_PROFILE.md`, the full privacy-depth calibration, and
  familiarizing the owner with the judgment-tuning skills — **`/golden-evolver`** (better few-shot
  examples) and **`/harness-review`** (weekly self-improvement of the agent's behavior).
- **`/setup` with no arg, after Core is done,** resumes the next undone level.

Run only the phases for the requested level. Always tell the owner which level they just finished and what
the next one covers, so deepening is an obvious next step rather than a thing they forget exists.

## The interview (phases — grouped by level above)

### Phase 0 — Environment bootstrap (make the brain runnable)
Before interviewing, get the tooling working so the brain can run its own scripts (use Bash):
- **Verify Python and Git** — `python3 --version` and `git --version`. If either is missing, give the
  user the one-line install for their OS and pause until it's present.
- **Create a virtualenv + install dependencies** — from the repo root. macOS/Linux:
  `python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`. Windows:
  `py -m venv .venv; .venv\Scripts\pip install -r requirements.txt` (if `py` isn't found, use
  `python`). This makes the bundled scripts (`/remove-watermark`, the `/nano-banana` image skills)
  run out of the box.
- **Create the owner's scratch files** — `cp .env.example .env` and `cp MEMORY.example.md MEMORY.md`
  (both gitignored). `.env` holds the keys you'll wire in Phase 5; `MEMORY.md` is the owner's
  portable cross-session memory (`@`-imported by `CLAUDE.md`) — you'll seed it at the end.
- Do this automatically; only surface a manual step if something genuinely can't be set up for them
  (no system Python, a wheel that won't build). **If you can't run shell commands at all (e.g. a
  sandboxed web surface with no terminal), don't block — tell the user the helper scripts can be
  wired up later (see `SETUP.md`) and continue straight to the interview, which needs no Python.**
  Then continue to the interview.

### Phase 1 — Purpose: what is this FOR?
The most important question, and the one most setups skip. Ask (AskUserQuestion):
- **"What do you want this second brain to DO for you?"** (e.g. never lose an idea / be a thinking
  partner / draft in your voice / track projects to the finish / remember your life / prep for
  agent-to-agent use). Multi-select + Other.
- **"What would make it a clear win 1 month from now?"** (One month on purpose — near enough to feel,
  and it gets re-scored at the monthly intent check-in you'll seed in Finishing.)
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
Write into `Orientation_Docs/INTELLECTUAL_LANDSCAPE_LITE.md`, and **also seed the full
`INTELLECTUAL_LANDSCAPE.md`** — `who_i_am_full`, `worldview_full`, and `influences` ("whose ideas
shaped you most?") — and `COGNITIVE_PROFILE.md` `strengths_and_friction` (from their Phase-2 gaps).
Preserve their exact words — no paraphrasing. The deeper landscape fields that need *mined* content
(obsessions-with-evidence, predictions, tensions, keyword mines) ship as breadcrumb comments — leave
them; they get filled after real content lands, not at setup.

### Phase 3.5 — How should I talk to you? (agent comms style — first-class, not a nicety)
This preference shapes every single interaction, so it's elicited in Core, not buried in a follow-up.
Ask (AskUserQuestion, one batched call):
- **Reply style** — terse and dense (answer first, expand on request) vs. explain as you go?
- **Pushback** — challenge my ideas when you disagree vs. just execute what I ask?
- **Decisions** — present options and content in chat, in front of me, vs. write them to a doc I read later?
- **Anything else about how an assistant should (or should not) talk to you?** (free text)
Write the answers to `INTENT_SPEC.md` (`agent_comms_style`) **and** mirror them as one-liners into
`MEMORY.md` (the Ambient section — it's `@`-imported at Tier 0, so they load every session). These two
writes are the difference between a preference the owner stated once and a preference the agent
actually obeys tomorrow.

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
  reading / highlights sync (Readwise · Kindle · RSS) · image generation · semantic search over
  their own notes*? Their answers tell you which catalog rows matter, so you recommend the right
  tools instead of dumping the whole list.
- **For each workflow they pick, surface the matching tool** and help set it up: the key in `.env`
  (`cp .env.example .env`), the install one-liner, or the connector toggle. (image gen →
  `GEMINI_API_KEY`; coding → gstack via `./setup`, needs Bun; media → ffmpeg + yt-dlp; deploys →
  fly + tailscale; 3D → Blender / ForgeCAD; messaging → Hermes.)
- **Strongly suggest the always-useful core** regardless of workflow: **gstack** (a virtual eng
  team), a **headless browser** (browser-harness or gstack's `/browse`, which powers the `$B`
  protocol in `CLAUDE.md`), an **embedding engine** for semantic search, and **ripgrep + jq**.
- **The connectors** (Gmail / Drive / Calendar / Notion) are zero-install — mention they can toggle
  them on in Claude settings to pull their real life into the brain.
- **If they picked reading / highlights** (or want passive capture): point them at the **Passive
  capture** note in `SETUP.md`. No scraper ships — for X, they download their own archive from X
  and run `/ingest-brain-dump`; for Readwise/Kindle/RSS, the agent *builds a puller on request*
  using the `/media-pipeline-example` pattern + a key in `.env` (e.g. `READWISE_API_KEY`).
- **Capture a few small identifiers while you're here** (AskUserQuestion, batch): their
  **X/Twitter handle** (→ `launch-idea` `x_handle`, for drafting launch posts), the **command that
  opens their browser** (→ `CLAUDE.md` `browser_harness_path` + `html-tweaker` `browser_open_command`),
  and their **flagship writing/creative project** if they have one (→ `CONTENT_TAXONOMY.md`
  `flagship_writing_project`). Skip any that don't apply.
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
  `/disk-cleanup` Phase 2 tars big folders to). Note any large archival folder it should target
  → `disk-cleanup` `large-archival-folder`.
- **Timezone** — their IANA timezone (e.g. `America/Toronto`). Write it to `.env` as
  `SECOND_BRAIN_TZ` (used by `scripts/tz.py`) and to `Orientation_Docs/ORIENTATION.md` `timezone`.
- **Phone — and how you want to reach the brain from it.** iOS or Android, *and* (AskUserQuestion) the
  owner's **preferred way to interact with their second brain from their mobile device** — e.g. voice
  dictation into a notes app that syncs, a phone-inbox folder the agent ingests, a chat bridge
  (Telegram/WhatsApp/Signal/Discord) into the brain, or "desktop only, no mobile." The mobile surface is
  where most real capture happens, so name it now; record the answer at `__FILL_FROM_USER__:mobile_interaction`
  and, if it implies an inbox, wire it to the capture-surface routing in `CLAUDE.md` BOUNDARIES. Don't
  build the bridge here — just capture the preference so the brain knows the owner's primary mobile path.
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

### Phase 8 — Folders & sources
The content folders ship as empty stubs. Ask (AskUserQuestion) which fit their life — prune the ones
they won't use, and capture any custom folders at `FOLDER_ORIENTATION.md` `__FILL_FROM_USER__:custom_folders`.
Also ask, batched:
- **Protected / read-only originals** — any folder of irreplaceable source material that must never be
  modified? → `CLAUDE.md` `protected_folders` and `sync-orientation-docs` `protected_readonly_path`.
- **Where their original thinking lives** — voice notes, dictation, a notes-app export, daily
  transcripts? → `Orientation_Docs/ORIENTATION.md` `original_thinking_sources`.
- **External_Sources subfolders** they'll actually use (podcast clips, bookmarks, research) →
  `connection-finder` `external_source_subfolders`.
- **Decide the ingestion scope — and record it.** From their answers above (original-thinking sources +
  external sources + any large export they name), co-author the **`source_inventory` table** in
  `Orientation_Docs/CONTENT_TAXONOMY.md` (`__FILL_FROM_USER__:source_inventory`) — one row per source,
  with its content type and a status (`pending` if they have it ready to import, `future` if it's capture
  they'll do later). Read the rows back and confirm: "these are the sources you're ingesting, in this
  order — right?" This is the canonical record of what gets mined, so nothing is left implicit.
- **Large export ready now?** If any source is `pending` (a notes-app dump, chat history, a voice-note
  archive, bookmarks), point them at `/mine` — it **triages the source, then calibrates the agent's
  judgment on small batches** before the bulk pass, so thousands of items don't get mis-filed on the
  agent's cold first guess. This is principle "calibrate the AI judgement early" made runnable; full loop
  in `Orientation_Docs/MINING.md`.

### Phase 9 — Make the spec yours
`INTENT_SPEC.md` has two halves: a fixed **architecture intent** (what this kind of brain is and why)
and the **Owner Intent** slots you filled in Phases 1–5. Walk the owner through the architecture-intent
prose once and invite them to **re-author any of it in their own words** — this is *their* brain's spec
now, not the template's. Some owners keep it verbatim; some rewrite it wholesale. Both are right. (If
they want a clean break, offer to replace the shipped spec with one authored from scratch in their voice.)

### Phase 10 — First loop (run one real capture, end to end)
Configuration is not the product; the loop is. Before Finishing, run the brain's core loop **once, live,
with real content**, so the owner experiences capture → file → connection before the session ends:
- Ask (AskUserQuestion): **"Give me one real thought — something on your mind today. Dictate or paste
  1–3 paragraphs; rough is perfect."** Offer prompts if they blank: an idea they keep returning to, a
  decision they're weighing, something they read that stuck.
- Run it through **`/ingest-brain-dump`**: segment, classify, present the Template A file for approval
  (their exact words, never paraphrased), file it, and point at any connection it makes — even on a
  fresh brain, connect it to what Phases 1–3 captured about them ("this echoes the gap you named").
- Close the phase explicitly: **"That was the loop. Now the real work begins — everything else in this
  brain is that loop, deepened: you bring your actual content in, and the model of you compounds."**
- If they genuinely have nothing in the moment, allow a skip — but seed the top item of `TODO_MASTER.md`
  as "[ ] Run your first `/ingest-brain-dump` — the brain hasn't run its loop yet," so the very first
  "what should I work on?" sends them back here.

## Finishing
- **Initialize the status docs — no interview, just sensible fresh-brain defaults.** Write today's date
  and a "just started" state into the markers that load on "what should I work on," so the owner's first
  status query never surfaces a raw `__FILL_FROM_USER__`:
  - `CLAUDE.md`: `current_status` → "Phase 1 (Ingestion): just started — finish `/setup`, then `/ingest-brain-dump`."; `active_reminders` → seed ONE real item, the **monthly intent check-in**: `- [ ] **Intent check-in (due <today + 1 month>)** — re-read INTENT_SPEC.md Owner Intent, score the brain against your success criteria, revise what drifted, set the next due date. (Added: <today>; surface until done, then re-seed.)` This is what gives the success criteria a clock — without it the spec is write-only.
  - `STATE_OF_SECOND_BRAIN.md`: `current_phase` → "Phase 1 — Ingestion (fresh brain, no content filed yet)"; `last_updated` → today; `blockers` → "None yet"; `shipped` → "Nothing yet"; `maintenance_schedule` → their pick (default: weekly, Sundays).
  - `TODO_MASTER.md` + `TODO_Second_Brain.md`: `last_updated` → today; top item → "[ ] Bring your first real content in (`/ingest-brain-dump` or `/mine`)" — or, if Phase 10 was skipped, "[ ] Run your first `/ingest-brain-dump` — the brain hasn't run its loop yet"; backlog empty.
  - `last_updated` in `KEYWORD_GUIDE.md`, `CONTENT_TAXONOMY.md`, `ORIENTATION.md`, `SECOND_BRAIN_MASTER_INDEX.md` → today.
  - `COGNITIVE_PROFILE.md` `model` → the model running this setup + today's date; `ROUTER.md` `subprojects_with_claude_md` and `special_role_docs` → empty lists (comment: "add as you create them").
- **Seed `MEMORY.md`** from what you learned this interview: their inviolable rules → the Hard-rules
  section; a couple of about-me pointers; their comms-style answers from Phase 3.5 (already mirrored
  there — verify, don't re-ask) plus any other workflow preferences (runs commands themselves? ask
  before deploying?). One terse line each.
- Regenerate the worksheet so line numbers stay honest (re-scan `__FILL_FROM_USER__` across the tree
  and rewrite `PERSONALIZE.md`), then show the user what's still unfilled — and note that the remaining
  ones are **content-first breadcrumbs** (project rosters, keyword mines), not things they forgot.
- Tell them the routing already works now, and that they can deepen `INTELLECTUAL_LANDSCAPE.md`,
  `VOICE_GUIDE.md`, and the depth calibration any time by re-running `/setup`.
- **Point them at `/golden-evolver`** — the way to tune the agent's *judgment* over time. Explain it in a
  line: when the agent keeps mis-classifying, under-summarizing, or missing keywords on a kind of content,
  they run `/golden-evolver [task]` to hand-pick a few great examples; every later run gets better. It's
  the same "calibrate the AI's judgment" idea as the privacy and mining loops, applied to few-shot examples.
- Hand off by ingestion scope (from the `source_inventory` you just recorded): if any source is
  **`pending`** (a real export ready to import), hand off to `/mine` — it triages, then calibrates on
  small batches, then bulk-mines (see `Orientation_Docs/MINING.md`). If everything is **`future`**
  (capture they'll do later), hand off to `/ingest-brain-dump` and suggest voice/dictation as their first
  capture. When in doubt, prefer `/mine` — the triage + calibration are what keep a bulk import clean.

## Verification (before you call setup "done for now")
Confirm: you used AskUserQuestion (not prose) for every phase you ran; Phase 1 (purpose) and Phase 2
(gaps) were asked and written; Phase 3.5 (comms style) was asked and landed in BOTH `INTENT_SPEC.md`
and `MEMORY.md`; the owner one-liner + landscape-lite have real content; any API keys
they gave went into `.env` (gitignored), not into a tracked file; **the status docs
(`STATE_OF_SECOND_BRAIN`, `TODO_MASTER`, `CLAUDE.md` `current_status`) were initialized**, so a fresh
"what should I work on?" shows no raw markers; **the monthly intent check-in reminder is seeded** in
`CLAUDE.md` ACTIVE REMINDERS with a real due date; **`MEMORY.md` exists** (copied from
`MEMORY.example.md`) and carries at least their hard rules; **Phase 10 ran one real ingestion loop**
(or its skip seeded the first-ingest TODO); and a final `grep -rn "__FILL_FROM_USER__" .` shows every
remaining marker is either filled or inside a breadcrumb comment — no naked Tier-0/Tier-1 placeholders.
