# ROUTER — Silent Context Loading

> Instructions TO the agent. This is the only orientation doc auto-imported.
> Decide which additional docs to Read based on the user's request. Load silently — do not announce, do not ask permission. Reading is cheap; reading the wrong files is only wasted tokens.

**Orientation path:** `Orientation_Docs/`

---

## What you have loaded (TIER 0)

- `CLAUDE.md` — critical rules, skills table, project callouts
- This `ROUTER.md` — decision guide
- `INTELLECTUAL_LANDSCAPE_LITE.md` — distilled "who the owner is in ~200 lines" — ensures
  no agent ever operates on their data without knowing who they are
- `MEMORY.md` — your portable cross-session memory, `@`-imported by `CLAUDE.md` (copy from
  `MEMORY.example.md` on first run). Travels with the repo; distinct from Claude Code's
  machine-local native `~/.claude/.../memory/` store.

For anything beyond pure coding you may need a deeper tier below. **Bias toward
loading more, not less** — see Behavioural notes at the bottom.

---

## Decision Rules (apply in order)

### Rule 1 — Pure code / repo work → stay at TIER 0
Triggers: file paths, bug fixes, feature work, scripts, dev servers, tests, git, build errors, refactors, tool-building inside `.claude/`, any code-only subproject.

Action: **load nothing extra.** Read only the specific source files the task requires.

### Rule 2 — Brain navigation / status / what's-next → TIER 1
Triggers: "what's on deck", "what's next", project status queries, "where does X live", "show me the brain", "what should I work on", priorities, near-term direction, any reference to a top-level brain folder, any "navigate me through the projects" prompt.

Action: silently `Read` all of:
- `Orientation_Docs/ORIENTATION.md`
- `Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md`
- `Orientation_Docs/STATE_OF_SECOND_BRAIN.md`
- `Orientation_Docs/PHASE_2_VISION.md`
- `Orientation_Docs/TODO_MASTER.md`

(Why this is here, not in Rule 3: when the owner asks "what's next" they want project state
*and* near-term direction, not just status. `INTELLECTUAL_LANDSCAPE_LITE.md` is already
in Tier 0 so you also have their life context. The vision doc + TODOs together are the
"where am I going" half — they belong with status.)

### Rule 3 — Deep intellectual / strategic / biographical / personal-data analysis → TIER 2
Triggers (any of these):
- Thinkers, influences, ideas in depth, project meaning, deep trade-offs, "should I…", life planning, cross-project synthesis, any deep reference to the owner's intellectual world or major projects (`__FILL_FROM_USER__:major_projects`).
- **Any analytical or exploratory task performed *on the owner's own data* that asks for evaluation, ranking, or qualitative judgment** — e.g. "what's most interesting/striking/best/favorite/the spirit of/the essence of" applied to their photos, notes, writings, ideas, archive, history. These queries imply *connect this to who I am*, not just *do the analysis*.
- Any prompt where giving a *correct* answer without their life-context would be a *misframed* answer.

Action: silently `Read` all of:
- `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md` (full version; the LITE is already loaded)
- `Orientation_Docs/COGNITIVE_PROFILE.md` (Template C draft, treat as hypothesis not law)
- `Orientation_Docs/KEYWORD_GUIDE.md`
- `Orientation_Docs/CONTENT_TAXONOMY.md`

Plus TIER 1 if not already loaded.

### Rule 4 — Writing in the owner's voice → TIER 2-Voice
Triggers: drafting tweets, posts, essays, story prose, first-person writing, rewrites, or any output meant to sound like the owner.

Action: silently `Read`:
- `Orientation_Docs/VOICE_GUIDE.md`

Combine with TIER 2 if the writing is substantive (essay/post) rather than a quick tweet.

### Rule 5 — Brain dump / ingestion / enrichment → TIER 2 + pipeline spec
Triggers: user pastes raw dictation, says "process this", invokes any `ingest-*`, `process-*`, `triage-*`, or `enrich-*` skill.

Action: load TIER 2 (Rule 3) **and** trust the invoked skill to self-load its own spec via its `required_context_files`. If no skill is invoked but the work clearly fits a pipeline (a recognizable ingestion source — podcast clips, chat exports, email, bookmarks, transcripts, a phone inbox), invoke the matching ingestion skill — don't do it by hand. (e.g. user pastes raw dictation → invoke your ingestion skill; not hand-rolled file creation.)

### Rule 6 — Full deep-dive / synthesis → TIER 4
Triggers: "load the brain", requests to cross-reference the entire Second Brain, deep synthesis across folders, or any task that genuinely needs the full-brain snapshot.

Action: invoke `/load-brain`. Never try to ingest the snapshot manually.

### Rule 7 — Entering a subproject → read its local CLAUDE.md
Triggers: the user asks you to work inside a subproject directory (e.g., `Projects/<subproject>/`, `vendor/*`), OR you are about to Edit / Write / Bash inside such a directory for the first time in the session.

Action: before touching files in that subproject, silently `Read` any `CLAUDE.md`, `AGENTS.md`, or `VERIFY.md` that lives in the project's root. Claude Code does not auto-load subproject CLAUDE.md files — they only auto-load when Claude Code is launched from that directory. You must pick them up yourself. Keep a list of known subprojects that carry their own CLAUDE.md here (`__FILL_FROM_USER__:subprojects_with_claude_md`), for example:

- `Projects/<subproject_a>/CLAUDE.md`
- `Projects/<subproject_b>/CLAUDE.md`
- `vendor/<tool>/CLAUDE.md`

If the user names a subproject not on this list, still Glob for a `CLAUDE.md` inside its root before work.

---

## Never auto-load

- The full-brain snapshot (huge — only via `/load-brain`)
- Oversized reference archives and any large visual/index trees

## Special-role docs (not tier-loaded — read only when their job comes up)

These live in `Orientation_Docs/` but are not part of any tier. Name them here so agents know they exist and why they're not auto-loaded (`__FILL_FROM_USER__:special_role_docs`), for example:
- A security-audit matrix — read when doing security work (referenced from CLAUDE.md ACTIVE REMINDERS).
- An append-only maintenance/tracking log — read only when tracing what a past `/weekly-maintenance` run did.
- Completed-cycle approval records or bookkeeping docs — historical reference only.

---

## Behavioural notes

- **Silent** means silent. Don't announce "Reading TIER 2 files." Just do the Reads before your substantive response.
- If a request spans multiple rules (e.g., code fix + strategic planning), load the union.
- **If you're unsure between two tiers, prefer the LARGER one.** A few thousand wasted tokens are cheap; misframed answers, missed connections, and the user having to re-explain who they are are expensive. The bias toward the smaller tier optimizes cost over quality and is wrong — a correct-but-disconnected answer about the owner's archive, given without realizing the central thread of their life, is the failure mode this guards against.
- **Re-evaluate tier on session pivots.** Tiers are loaded once per request, but a long session that drifts from coding into biographical/strategic territory (e.g., "explore my photos and tell me what's interesting") needs a re-evaluation. Don't ride Tier-0 momentum into a Tier-2 question.
- **Respect privacy depth.** Files carry a `depth: N` (1–5) frontmatter — their disclosure level (see `Orientation_Docs/PRIVACY_DEPTH.md`). On routine/autonomous passes prefer low-depth (≤2) material; load depth 3+ only when the task needs it and the owner is in the loop; never surface depth 4–5 in a shareable / agent-to-agent context without explicit authorization. This is the loading half of progressive context exposure.
- Skills that declare `required_context_files` in their frontmatter supersede these rules when invoked — load whatever the skill demands, silently.
- Sub-agents inherit **nothing** automatically — not this ROUTER, not CLAUDE.md, not MEMORY.md or its shards, not topic files. A spawned sub-agent is context-blind by default (verified against Claude Code docs + issue #29423). The parent is the only channel: load the right tier BEFORE delegating and **hand-inject the relevant priors into the sub-agent's prompt** (the 10-slot `<context>` slot). For a rule that must hold regardless of model compliance — especially inside a sub-agent — the only deterministic mechanism is a PreToolUse hook, not memory/rules/CLAUDE.md.
