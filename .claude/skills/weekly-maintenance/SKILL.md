---
name: weekly-maintenance
description: >-
  Intelligent weekly maintenance with parallel review agents. Updates counts/dates,
  spawns 3 Explore agents (Doc Coherence, New File Quality, Project Pulse),
  auto-applies mechanical fixes, surfaces only judgment calls.
  Use when user says "weekly maintenance", "maintenance", "weekly sync", or on Sundays.
required_context_files:
  - INTENT_SPEC.md
  - Orientation_Docs/STATE_OF_SECOND_BRAIN.md
  - Orientation_Docs/TODO_MASTER.md
  - Orientation_Docs/TRACKING_LOG.md
  - $HOME/.claude/projects/<your-project-dir-slug>/memory/maintenance-calibration.md
---

# Weekly Maintenance (Intelligent)

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `INTENT_SPEC.md` (repo root — the Owner Intent section is the yardstick the drift check below measures against)
- `Orientation_Docs/STATE_OF_SECOND_BRAIN.md`
- `Orientation_Docs/TODO_MASTER.md`
- `Orientation_Docs/TRACKING_LOG.md`
- `$HOME/.claude/projects/<your-project-dir-slug>/memory/maintenance-calibration.md` (carry-over register + auto-resolve rules)

<!-- silent-context-load:v1 -->

Replaces the old manual checklist with an intelligent review that auto-applies obvious fixes and only asks about edge cases. The sweep runs in two complementary layers: a **deterministic checker** (`checks.py`, Step 1.5) that enumerates structural drift the LLM agents proved unreliable at catching (they sample; it enumerates), and the **three review agents** (Step 2) that catch the semantic/quality/judgment issues a script cannot model. Both always run.

## Trigger Conditions

- User says: "weekly maintenance", "maintenance", "weekly sync", "run maintenance"
- Sunday reminder (manual — no cron)

## Process

### Step 1: GATHER (lead agent)

Run these commands and capture output for agent context:

```bash
# 1. File counts
python3 "$SECOND_BRAIN_ROOT/scripts/update_counts.py"

# 2. Last maintenance date
grep "Last Maintenance:" "$SECOND_BRAIN_ROOT/Orientation_Docs/STATE_OF_SECOND_BRAIN.md"

# 3. New files since last maintenance (repo root IS the brain — no path filter needed)
cd $SECOND_BRAIN_ROOT && git log --since="[LAST_MAINTENANCE_DATE]" --diff-filter=A --name-only --pretty=format:"" | grep -v '^$' | sort -u

# 4. Modified files since last maintenance
cd $SECOND_BRAIN_ROOT && git log --since="[LAST_MAINTENANCE_DATE]" --name-only --pretty=format:"" | grep -v '^$' | sort -u

# 5. Commit messages since last maintenance
cd $SECOND_BRAIN_ROOT && git log --since="[LAST_MAINTENANCE_DATE]" --oneline

# 6. Aged working-tree drift (files modified but uncommitted for 7+ days)
#    Combines `git status` with per-file mtime. Same-day work is active and expected; aged drift is a leak.
cd $SECOND_BRAIN_ROOT && git status --porcelain | awk '{print $2}' | while read f; do
  if [ -f "$f" ]; then
    age_days=$(( ( $(date +%s) - $(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f") ) / 86400 ))
    if [ "$age_days" -ge 7 ]; then
      echo "$age_days days: $f"
    fi
  fi
done | sort -rn
```

**Carry-over read (mandatory):** also load `maintenance-calibration.md` (listed in `required_context_files`) and extract the `## Carry-Over Register` section. Each entry has a `first_flagged` date and `runs_surfaced` count — these feed the escalation ladder in Step 4. If the file does not exist, or exists but has no Carry-Over Register section, treat the register as empty and proceed; do not block on it.

Store all output as `gather_context` — passed to all 3 agents. Include `aged_drift` and `carry_over` as named sub-sections so agents can reason about them separately from fresh activity.

### Step 1.5: DETERMINISTIC CHECKS (always runs, read-only)

Before spawning the review agents, run the deterministic checker. It exhaustively enumerates the structural-drift classes a sampling LLM agent slips past: skills-table parity (`.claude/skills/` vs the CLAUDE.md table), dead internal links + malformed `.../` paths across the high-traffic docs, intent-spec count drift, memory frontmatter/wikilink/index integrity, MEMORY.md budget, and known doc-pair contradictions (e.g. PHASE_2_VISION vs STATE).

```bash
python3 $SECOND_BRAIN_ROOT/.claude/skills/weekly-maintenance/checks.py
```

Every finding it prints is MECHANICAL and pre-grounded against the filesystem — feed them into the Step 3 aggregate alongside the agents' reports. `[HIGH]`/`[MEDIUM]` items are AUTO-APPLY candidates (factual corrections — stale counts, broken links, missing frontmatter `name:`); `[LOW]` items (e.g. forward-reference `[[wikilinks]]` that are sanctioned by the memory design, or a few-bytes-over budget) are informational unless they recur. The checker only reads — it never edits. Pass `--json` to parse it programmatically. Born from the 2026-05-31 self-audit, where these exact classes had drifted unnoticed because the review agents sampled rather than enumerated.

### Step 2: SPAWN 3 EXPLORE AGENTS (parallel, Sonnet)

Launch all 3 simultaneously using `Agent` tool with `subagent_type: "Explore"` and `model: "sonnet"`.

Each agent receives `gather_context` plus its specific instructions below.

---

#### Agent A: "Doc Coherence"

Doc Coherence owns the full orientation surface — not just the STATE/MASTER_INDEX pair. It also measures the week's accretion against the Owner Intent in `INTENT_SPEC.md` (the drift check that keeps growth pointed where the owner said it should point), and — if the brain maintains an optional `Wiki/` synthesis layer — bridges it back into the intellectual spine (`INTELLECTUAL_LANDSCAPE.md`), so new projects, people, and concepts don't stall unregistered.

**Prompt template:**

```
<purpose>
You are Agent A in a three-agent weekly maintenance sweep (Doc Coherence, alongside New File Quality and Project Pulse). The lead agent aggregates all three reports and auto-applies every item you put under AUTO-APPLY without further review, then asks the owner about every item under JUDGMENT CALLS. Miscalibration in either direction corrupts the sweep — an AUTO-APPLY item the lead shouldn't have applied silently drifts the orientation docs; a JUDGMENT CALL that was actually mechanical wastes the owner's attention on a decision they don't need to make.
</purpose>

<role>
Orientation-doc coherence auditor covering counts, dates, tiers, TODO routing, intent drift (accretion vs INTENT_SPEC.md Owner Intent), CLAUDE.md ACTIVE REMINDERS routing, dead references, quality remediation, carry-over escalation, and (if present) the Wiki↔INTELLECTUAL_LANDSCAPE bridge.
</role>

<return>
Close your turn with a report in this exact structure (the lead agent's aggregator keys off these headings):

## Agent A: Doc Coherence Report

### ACTION REQUIRED (carry-over aged ≥ 3 runs)
Per item:
- **Item:** [description]
- **First flagged:** [date]
- **Runs surfaced:** [N]
- **Why it's blocking:** [1 sentence]
- **Proposed resolution:** [concrete next step]

### AUTO-APPLY (clear/obvious mechanical fixes)
Per item:
- **File:** [absolute path]
- **Line ref:** [line number or section heading]
- **Current:** [exact current text]
- **Proposed:** [exact replacement text]
- **Reason:** [1 sentence]

### JUDGMENT CALLS (uncertain or edge-case, includes carry-over aged < 3 runs)
Per item:
- **File:** [absolute path, if applicable]
- **Issue:** [description with full context]
- **Carry-over?** [yes/no; if yes, age + runs_surfaced]
- **Suggested action:** [what you'd recommend]
- **Why uncertain:** [why this needs human input]

### CARRY-OVER RESOLVED (remove from register)
[Any prior carry-over items that are now resolved, with evidence.]

### NO ISSUES FOUND
[Checks that passed cleanly, one line each.]
</return>

<approach>
Load the context block below (file counts, git activity, aged drift, carry-over register) and every file in the mandatory READ list. Then sweep the coherence surface across these areas; each area you examine lands in exactly one of the report's sections.

- **Counts.** Compare documented file counts in MASTER_INDEX's stats table and CONTENT_TAXONOMY's "Current State" table to the actual numbers from update_counts.py. A drift of >5% is AUTO-APPLY with the corrected number; tighter drift is reported under NO ISSUES FOUND.
- **Dates.** "Last Updated" / "As of" stamps within 14 days are fresh. 14–30 days old with clearly-stale content is AUTO-APPLY (update the stamp). Older than 30 days is a JUDGMENT CALL (may need a content refresh, not just a date bump).
- **Project tiers.** Cross-reference STATE_OF_SECOND_BRAIN's tier tables against the git activity block. Tier alignment with observed activity is NO ISSUES FOUND; genuine mismatches (Tier 1 silent for weeks, Tier 4 shipping daily) are JUDGMENT CALLS.
- **TODO routing.** Glob for `**/TODO*.md` from the repo root. Every result should be referenced in TODO_MASTER.md or be explicitly archived. Orphans are JUDGMENT CALLS unless the routing is unambiguous (in which case AUTO-APPLY the index-line insert).
- **Intent drift (vs INTENT_SPEC.md Owner Intent).** Read the Owner Intent section — purpose, gaps, goals, success criteria, non-goals. Compare it against the week's actual accretion (the git-activity block: where new files landed, what projects moved). Sustained mismatch is a JUDGMENT CALL with evidence — e.g. "stated purpose is X, but 3 weeks of files have landed in Y and nothing has touched X," or activity that matches a stated *non-goal*. Also check the seeded **intent check-in** reminder in CLAUDE.md ACTIVE REMINDERS: if its due date has passed, surface it as ACTION REQUIRED (it is the owner's monthly re-score of the spec). If Owner Intent still holds naked `__FILL_FROM_USER__` markers after setup, that's a JUDGMENT CALL to re-run `/setup`. Alignment is NO ISSUES FOUND ("accretion consistent with stated purpose").
- **Wiki↔INTELLECTUAL_LANDSCAPE bridge** *(only if the brain maintains a `Wiki/` synthesis layer — skip with a NO ISSUES FOUND note if the folder doesn't exist)*. Every Wiki page under `projects/`, `entities/people/`, or `concepts/` that also appears in STATE_OF_SECOND_BRAIN's tier tables should appear in INTELLECTUAL_LANDSCAPE's corresponding section. Missing entries are JUDGMENT CALLS (propose the table-row insert so the owner can one-click approve).
- **ACTIVE REMINDERS routing.** Each bullet under CLAUDE.md's ACTIVE REMINDERS heading should be grep-findable in some TODO file. Unrouted reminders are JUDGMENT CALLS (propose the destination file and section).
- **Dead references.** Each orientation doc references other files by name. For each doc in the mandatory READ list, sample ≥3 referenced file paths, verify each target via Read or Glob, and report the sampled set in your output so the lead agent can audit which references you actually checked. Targets that exist are NO ISSUES FOUND. Unambiguous renames (exactly one match elsewhere) are AUTO-APPLY. Ambiguous cases are JUDGMENT CALLS.
- **Quality remediation.** STATE's known-quality-issues list is the check list. For each listed issue, git activity since last maintenance either resolved it or did not. Resolved items go under CARRY-OVER RESOLVED with the commit reference; open items stay under NO ISSUES FOUND unless this run uncovered new ones.
- **Carry-over register.** The block below lists entries with `first_flagged` and `runs_surfaced`. Each entry lands in one of four places: ACTION REQUIRED (runs_surfaced ≥ 3), JUDGMENT CALLS (< 3, with the age stamped), CARRY-OVER RESOLVED (underlying issue fixed — verify, don't assume), or stays in JUDGMENT CALLS flagged as unchanged.
</approach>

<examples>
<example>
A well-formed AUTO-APPLY item:

- **File:** $SECOND_BRAIN_ROOT/Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md
- **Line ref:** Line 24 (Stats table)
- **Current:** `| ~7757 | 14 | Apr 14, 2026 |`
- **Proposed:** `| ~7828 | 14 | Apr 21, 2026 |`
- **Reason:** update_counts.py reports 7828 today, a 0.9% drift from the documented 7757 — below the 5% threshold for flagging but worth syncing while the lead agent is editing this file anyway.

A well-formed JUDGMENT CALL:

- **File:** $SECOND_BRAIN_ROOT/CLAUDE.md (ACTIVE REMINDERS block)
- **Issue:** "Recover lost notes from phone" (Apr 16) is not grep-findable in any TODO file. It's adjacent to a capture-pipeline project but the failure mode (silent network drop during capture) is phone-UX, not pipeline-code, so it doesn't cleanly belong in the pipeline TODO.
- **Carry-over?** No (first surface in this audit)
- **Suggested action:** Create TODO_Personal_Actions.md (or equivalent) for non-project reminders, or route to the most relevant project TODO under a new reliability section.
- **Why uncertain:** The convention for where cross-cutting reminders live is unsettled — the owner may want a personal-actions file, or may prefer scattering into the most-relevant project.

A well-formed ACTION REQUIRED item:

- **Item:** Major-influence deep dive (e.g. a key intellectual figure with zero Template A files)
- **First flagged:** [date]
- **Runs surfaced:** 3
- **Why it's blocking:** Major intellectual influence with zero Template A files after three maintenance runs. The gap compounds as related material lands in other folders without an anchor file to tie it back.
- **Proposed resolution:** Dedicated session — read primary sources, produce 3–5 Template A files mapping concepts to existing owner frameworks, add to INTELLECTUAL_LANDSCAPE's relevant section, cross-reference from Journal_Intellectual.
</example>
</examples>

<constraints>
- Every item lands under exactly one of: ACTION REQUIRED / AUTO-APPLY / JUDGMENT CALLS / CARRY-OVER RESOLVED / NO ISSUES FOUND. No item appears twice; no item is described in prose outside these sections.
- AUTO-APPLY items must be safe for the lead agent to apply verbatim. If the exact replacement text depends on the owner's judgment, it is a JUDGMENT CALL — move it.
- JUDGMENT CALLS must include a concrete `Suggested action` and `Why uncertain` — a JUDGMENT CALL with no recommendation wastes the owner's attention on the discovery rather than the decision.
- For the carry-over register: verify resolution by checking the file state, not by inference. A carry-over is RESOLVED only when the underlying file / edit actually exists today.
- Cite absolute paths (beginning with `$HOME/`) in every File reference so the lead agent and the owner can click directly.
- NO ISSUES FOUND is a positive reporting section — an empty sweep should land checks here, not omit them. "Checks I ran and everything was fine" is useful signal; silence is not. Name each of the ten check areas explicitly so the lead agent can confirm every area was swept (e.g., "Counts drift — 0.9%, within threshold"; "Intent drift — accretion consistent with stated purpose"; "Dead-reference sweep — sampled 15 refs, all resolve").
- The five structured sections are the aggregator contract. Any prose outside those headings (introduction, summary, commentary) is optional padding — keep it short and after the NO ISSUES FOUND section so it does not interleave with the parsed content.
</constraints>

<verify>
Before ending your turn, confirm:
- Every one of the ten areas in <approach> is accounted for somewhere in the report — AUTO-APPLY / JUDGMENT CALLS / CARRY-OVER RESOLVED / NO ISSUES FOUND.
- Every carry-over register entry lands in ACTION REQUIRED (if runs_surfaced ≥ 3), CARRY-OVER RESOLVED (if actually resolved), or JUDGMENT CALLS (otherwise) — no carry-over entry is missing from the report.
- Every AUTO-APPLY item has all 5 fields (File, Line ref, Current, Proposed, Reason) filled with real content, not placeholders.
- Every JUDGMENT CALL has all 5 fields (File, Issue, Carry-over?, Suggested action, Why uncertain) filled.
- Absolute paths in every File reference.
- The Summary/prose at the end is OPTIONAL; the five structured sections are the contract.
</verify>

<done>
The lead agent can regex-parse your five section headings, apply every AUTO-APPLY item without further inspection, and hand the owner a clean list of ACTION REQUIRED + JUDGMENT CALLS for their weekly decision.
</done>

<return>
Return the report in the structure specified in the top `<return>` block. End the output at the NO ISSUES FOUND section or an optional one-paragraph Summary line, not in the middle of a section.
</return>

<context>
FILE COUNTS (from update_counts.py):
[paste output]

GIT ACTIVITY SINCE [date]:
New files: [paste]
Modified files: [paste]
Commits: [paste]

AGED WORKING-TREE DRIFT (files uncommitted 7+ days):
[paste — may be empty]

CARRY-OVER REGISTER (flagged in prior runs, still unresolved):
[paste entries from maintenance-calibration.md Carry-Over Register with runs_surfaced counts]

READ THESE FILES (mandatory):
1. $SECOND_BRAIN_ROOT/INTENT_SPEC.md — the Owner Intent section (yardstick for the intent-drift check)
2. $SECOND_BRAIN_ROOT/Orientation_Docs/STATE_OF_SECOND_BRAIN.md
3. $SECOND_BRAIN_ROOT/Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md
4. $SECOND_BRAIN_ROOT/Orientation_Docs/TODO_MASTER.md
5. $SECOND_BRAIN_ROOT/Orientation_Docs/CONTENT_TAXONOMY.md
6. $SECOND_BRAIN_ROOT/Orientation_Docs/INTELLECTUAL_LANDSCAPE.md
7. $SECOND_BRAIN_ROOT/Orientation_Docs/ORIENTATION.md
8. $SECOND_BRAIN_ROOT/CLAUDE.md — ONLY the "ACTIVE REMINDERS" block (search for that heading)
9. $SECOND_BRAIN_ROOT/Wiki/index.md + Wiki/TRACKING.md — ONLY if a Wiki/ layer exists (optional pattern; skip otherwise)
</context>
```

---

#### Agent B: "New File Quality"

**Prompt template:**

```
You are reviewing new files added to Second Brain this week for quality.

NEW FILES ADDED SINCE [date]:
[paste list]

YOUR TASK: Check template compliance and quality of new files.

FOR EACH NEW FILE (up to 30 files — if more, sample evenly):
1. Read the first 30 lines using the Read tool
2. Check against these criteria:

CHECKS:
1. Template compliance: Does it have ## Metadata, ## Summary, ## Keywords, ## Original Text (Template A) or ## Content (Template B)?
2. Folder placement: Is the file in the correct folder per its Primary category? Cross-reference with FOLDER_ORIENTATION.md at $SECOND_BRAIN_ROOT/FOLDER_ORIENTATION.md
3. Keyword quality: Does it have >= 8 keywords? List files with fewer.
4. Stale references: Contains "This Database" instead of "This Second Brain"?
5. Missing metadata fields: Any required fields empty or missing?

OUTPUT FORMAT (mandatory):

## Agent B: New File Quality Report

### FILES CHECKED
| # | File | Template | Keywords | Placement | Issues |
|---|------|----------|----------|-----------|--------|
| 1 | [relative path] | OK/FAIL | [count] | OK/WRONG | [brief] |

### AUTO-APPLY (clear fixes)
For each item:
- **File:** [absolute path]
- **Line ref:** [line number]
- **Current:** [exact text]
- **Proposed:** [exact replacement]
- **Reason:** [1 sentence]

### JUDGMENT CALLS
For each item:
- **File:** [absolute path]
- **Issue:** [description]
- **Suggested action:** [recommendation]

### SUMMARY
- N files checked, N pass template compliance
- N files have thin keywords (<8)
- N files have stale references
- N files misplaced
```

---

#### Agent C: "Project Pulse"

**Prompt template:**

```
You are reviewing project activity in Second Brain to check if stated priorities match reality.

GIT COMMITS SINCE [date]:
[paste commit messages]

MODIFIED FILES SINCE [date]:
[paste list]

YOUR TASK: Compare actual project activity against stated project tiers.

READ THESE FILES:
1. $SECOND_BRAIN_ROOT/Orientation_Docs/STATE_OF_SECOND_BRAIN.md (project status tables)
2. The 3-4 most active project TODO files based on git activity (use Glob for Projects/*/TODO*.md)
3. Tail of $SECOND_BRAIN_ROOT/Orientation_Docs/TRACKING_LOG.md (last 50 lines)

CHECK FOR:
1. Tier mismatches: Tier 1 projects with zero commits? Tier 3/4 projects with heavy activity?
2. TODO completions: Any TODO items that appear done based on git activity?
3. Stale blockers: Blockers listed in STATE that may be resolved
4. New keyword candidates: Interesting terms from new file names or commit messages
5. **Intent Spec Existence Check** (see section below — run for each active project).

### Intent Spec Existence Check

For each active project, check for an OFFICIAL intent spec file. Files named `INTENT_SPEC.md`, `INTENT.md`, or `SPEC.md` count if they are owner-authored (no `status: UNOFFICIAL - PENDING OWNER REVIEW` frontmatter, no "DRAFT" markers in the first 20 lines).

If missing OR only an unofficial draft exists, surface in the weekly maintenance output:

> **Intent spec missing:** `[project name]` — the owner should author `INTENT_SPEC.md` when idle. Agents may draft an UNOFFICIAL backfill on request, but the owner must approve before it becomes ground truth for agentic workflows.

Rationale: intent spec is ground truth for gap-report / gap-closer agentic workflows. An agent-authored "intent" is actually a description of current state, not intent — so backfill drafts stay UNOFFICIAL until the owner reviews.

OUTPUT FORMAT (mandatory):

## Agent C: Project Pulse Report

### ACTIVITY BY PROJECT
| Project | Tier | Commits | Files Changed | Assessment |
|---------|------|---------|---------------|------------|
| [name]  | [1-5]| [N]     | [N]           | [on track / surprisingly active / dormant] |

### AUTO-APPLY (clear fixes)
For each item:
- **File:** [absolute path]
- **Line ref:** [section heading]
- **Current:** [exact text]
- **Proposed:** [exact replacement]
- **Reason:** [1 sentence]

### JUDGMENT CALLS
For each item:
- **Issue:** [description]
- **Suggested action:** [recommendation]

### KEYWORD CANDIDATES
[New terms worth adding to KEYWORD_GUIDE.md]

### TODO ITEMS POSSIBLY COMPLETE
[List with evidence from git]
```

---

### Step 3: AGGREGATE

After all 3 agents return:

0. Collect the deterministic findings from `checks.py` (Step 1.5) — these are pre-verified MECHANICAL items; route `[HIGH]`/`[MEDIUM]` into AUTO-APPLY and dedup them against anything the agents independently flagged.
1. Collect all ACTION REQUIRED items (Agent A only — the aged carry-over escalations)
2. Collect all AUTO-APPLY items from A, B, C
3. Collect all JUDGMENT CALLS from A, B, C
4. Collect all CARRY-OVER RESOLVED entries from Agent A
5. Deduplicate (same file + same issue = one item)
6. Prioritize: ACTION REQUIRED first, then judgment calls by impact

### Step 3.5: REBUILD EMBEDDINGS INDEX (only if you've implemented the embedding stub)

`scripts/sb_embed.py` ships as a stub — see `SETUP.md`. If you haven't implemented it yet, skip this step with a one-line note in the report. Once implemented: run an incremental embeddings rebuild before applying edits, so semantic-search recall can never drift more than 7 days even if the `mark_embedding_pending.py` PostToolUse hook misses signals. Incremental, not `--rebuild`.

```bash
python3 $SECOND_BRAIN_ROOT/scripts/sb_embed.py index
```

Consumes `.claude/embeddings/pending.txt` if present, then clears it. Takes ~minutes on a 7-day delta. Run in foreground; report runtime in the final summary. If it fails (model load error, FAISS corruption), surface as a JUDGMENT CALL — do NOT block AUTO-APPLY edits below.

### Step 4: AUTO-APPLY MECHANICAL EDITS

Apply all AUTO-APPLY items using Edit tool. These are factual corrections:
- Stale file counts
- Stale dates
- "This Database" -> "This Second Brain"
- Known canonical fixes (see `maintenance-calibration.md` "Auto-Resolve" section)

No user interaction needed. Just do them.

### Step 5: SURFACE ACTION REQUIRED + JUDGMENT CALLS

**If any ACTION REQUIRED items exist, present them FIRST, above judgment calls:**

```markdown
### ACTION REQUIRED (carry-over aged ≥ 3 runs — no longer deferrable)
1. **[Item]**
   First flagged: [date] ([N] runs surfaced)
   Why it's blocking: [1 sentence]
   Proposed resolution: [concrete step]
   -> **Decide now:** resolve, explicitly defer with reason, or retire the item.
```

Then, if any JUDGMENT CALLS exist, present them:

```markdown
### JUDGMENT CALLS (need your input)
1. **[Issue title]** [carry-over tag if applicable: "(carry-over, flagged N days ago)"]
   Context: [full context]
   Suggested: [action]
   -> **Calibration Q:** Should this auto-apply in future weeks?
```

If neither list has items, skip this step entirely.

After the user responds, persist changes to `maintenance-calibration.md`:
- New auto-apply rules → append to "Auto-Resolve"
- New "do not auto-fix" rules → append to "Do NOT Auto-Fix"
- ACTION REQUIRED items the user resolved → remove from Carry-Over Register
- ACTION REQUIRED items the user explicitly defers → increment `runs_surfaced` and note the defer reason
- JUDGMENT CALLS not resolved this run → add to Carry-Over Register (if new) or increment `runs_surfaced` (if repeat)
- CARRY-OVER RESOLVED entries from Agent A → remove from register

### Step 6: COMMIT & REPORT

1. Update "Last Maintenance" and "Next Due" dates in STATE_OF_SECOND_BRAIN.md
2. Add TRACKING_LOG entry — include a line per carry-over item surfaced/resolved so the next run can trace lineage
3. Update `maintenance-calibration.md` with the final carry-over register state (see Step 5 persistence rules). This file lives outside the repo under Claude Code's memory directory (`$HOME/.claude/projects/<your-project-dir-slug>/memory/`) — the Write/Edit tool persists it; it is NOT part of the git commit.
4. Stage ONLY repo files that were edited in this run (never `git add -A`, never the calibration memory file)
5. Commit: `"Weekly maintenance sync - [date]"`

### Step 7 (optional) — offer a harness self-review
This sweep kept the *content* clean. The agent's *behavior* is a separate axis. After the report, ask
(AskUserQuestion) whether the owner also wants to run **`/harness-review`** — it reads the last week of
session traces for harness-level friction (repeated corrections, permission-prompt churn, misfiring or
unused skills, ignored rules) and proposes gated fixes. Default to offering it but not auto-running; if
they decline, note it and finish.

Present final report:

```markdown
## Weekly Maintenance Report - [Date]

**Period:** [last maintenance] to [today]
**New files:** N | **Modified:** N | **Commits:** N | **Aged drift:** N files ≥ 7 days uncommitted

### ACTION REQUIRED (aged carry-over — resolve, defer with reason, or retire)
[only if any — otherwise "None this week"]

### AUTO-APPLIED (already done)
| # | File                  | Edit                              |
|---|-----------------------|-----------------------------------|
| 1 | MASTER_INDEX.md       | Total: ~5167 -> ~5180             |
| 2 | STATE_OF_SECOND_BRAIN | Last Maintenance: [old] -> [new]  |

### JUDGMENT CALLS (need your input)
[only if any — otherwise "None this week"; annotate carry-over items with age]

### CARRY-OVER REGISTER (after this run)
| Item | First flagged | Runs surfaced | Status |
|------|---------------|----------------|--------|
| [description] | [date] | [N] | open / escalated / deferred |

### NEW FILE QUALITY SUMMARY
[from Agent B]

### PROJECT PULSE
[from Agent C]

### KEYWORD CANDIDATES
[from Agent C, if any]
```

## Key Design Decisions

- **Sonnet for all 3 agents** — this is high-value review work, not a Haiku task
- **Explore agents (read-only)** — agents analyze and report. Lead applies edits.
- **Auto-apply by default** — mechanical/factual corrections go through without asking
- **Calibration loop** — when judgment calls arise, ask user "should this auto-apply next time?" and persist to memory
- **Carry-over with age escalation** — items flagged but unresolved across runs aren't rediscovered; they're tracked in the calibration register and escalated to ACTION REQUIRED after 3 runs. Prevents the "same judgment call, surfaced and forgotten, every week" failure mode.
- **Agent A owns the full orientation surface** — including INTELLECTUAL_LANDSCAPE, ORIENTATION, the intent-drift check against INTENT_SPEC.md, CLAUDE.md ACTIVE REMINDERS routing, and (if present) the Wiki↔IL bridge. Adding a 4th agent would be simpler on paper; folding these into Doc Coherence is more honest about what "coherence" means.
- **Intent drift is a weekly check, not a quarterly retrospective** — the Owner Intent in INTENT_SPEC.md is the yardstick; accretion that drifts from it gets surfaced while the drift is one judgment call wide, not a junk drawer deep.
- **Dead-reference grep** — orientation docs reference each other by filename; the skill verifies those targets exist every run. Cheap, catches drift early.
- **Aged drift threshold (7 days)** — same-day uncommitted changes are active work, not drift. The skill only warns about shadow state that's been sitting ≥ 7 days, so running maintenance mid-session doesn't produce noise.
- **Pre-compute git data once** — lead runs git commands, passes output to all 3 agents as context
- **Head -30 for new files** — template compliance detectable in first 30 lines
- **Don't read all 23 folder ORIENTATIONs** — stable routing tables. Only check when misplaced file detected.

## Files Touched

| File                                                             | When Updated                                    |
|------------------------------------------------------------------|-------------------------------------------------|
| `Orientation_Docs/STATE_OF_SECOND_BRAIN.md`         | Always (dates, possibly tiers)                  |
| `Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md`     | If counts changed                               |
| `Orientation_Docs/TRACKING_LOG.md`                  | Always (session entry + carry-over lineage)     |
| `Orientation_Docs/CONTENT_TAXONOMY.md`              | If counts changed (now auto-updated by script)  |
| `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`        | If Wiki↔IL backport or table refresh needed     |
| Any file with stale references or dead cross-refs                | If auto-apply fixes found                       |
| `memory/maintenance-calibration.md`                              | Always (carry-over register update)             |

## Integration

| Skill                    | Relationship                                       |
|--------------------------|----------------------------------------------------|
| `sync-orientation-docs`  | Weekly maintenance SUBSUMES routine syncs           |
| `wind-down`              | Run wind-down after maintenance if ending session   |
| `process-content`        | Agent B may flag quality issues in recently ingested content |

## Error Handling

- If an agent fails or times out: proceed with the other 2 reports. Note the gap.
- If update_counts.py fails: skip count checks, note in report.
- If git commands fail: report what you have, skip git-dependent checks.
- If no new files since last maintenance: Agent B reports "No new files" and skips.
