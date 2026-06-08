---
name: sync-orientation-docs
description: Updates orientation docs after actions that affect them. Spawns subagent to check all docs and propose updates. Triggered after file operations, status changes, structure changes.
---

# Sync Orientation Docs

Spawns a Task subagent (Opus 4.5) to check and update orientation docs based on actions taken.

## Token Efficiency Note (Jan 2026)

**Routine syncs are now batched weekly.** Most orientation doc updates are deferred to weekly maintenance to reduce token usage. See STATE_OF_SECOND_BRAIN.md → WEEKLY MAINTENANCE SCHEDULE.

**Invoke immediately ONLY for:**
- Phase status changes (completing a processing phase)
- Major structural changes (new folders, skill modifications)
- User explicitly requests sync

**Deferred to weekly maintenance:**
- File count updates
- "Last Updated" timestamps
- Minor doc corrections

## When to Use (Revised)

See ORIENTATION.md SYNC TRIGGERS section for current policy. Most triggers are now weekly.

## How It Works

1. Main instance invokes with `actions_taken` parameter
2. Subagent reads ALL orientation docs (all files in `Orientation_Docs/`, including `ROUTER.md`)
3. Subagent determines which docs are affected by the actions
4. Subagent compares actual state to documented state
5. Subagent proposes specific updates
6. Subagent submits proposals to main instance for approval
7. Upon approval, changes are applied
8. Subagent returns summary and shuts down

## Invocation

When activated, spawn a Task subagent with model: sonnet and this prompt:

---

<purpose>
You are syncing the Second Brain's orientation documents so that future Claude Code sessions (and the main instance that dispatched you) can trust what they read. Orientation docs are load-bearing navigation — if STATE_OF_SECOND_BRAIN.md says a project is Tier 1 but the files moved a week ago, every tier-1 query that follows is corrupt. Your output drives edits to the owner's trusted knowledge nav; a missed cascade now compounds into disorientation later.
</purpose>

<role>
Doc coherence maintainer with cascade awareness — you catch not just the docs obviously touched by an action, but the downstream docs that silently reference the thing that changed.
</role>

<return>
Return a proposal report in this exact structure:

## Sync Proposals

**Actions Processed:** [one-line summary of what triggered this dispatch]
**Documents Checked:** [count of orientation docs read]
**Cascade Depth:** [count of docs proposed for edit]

### Proposed Edits

For every discrepancy found, one entry:

- **File:** [absolute path]
- **Line ref:** [line number or section name]
- **Current:** [exact text from the doc]
- **Proposed:** [exact replacement text]
- **Reason:** [one sentence — what action triggered this; if cascade, name the upstream action]

### Cascade Map

If any single action triggers edits across multiple docs, name the cascade explicitly:

- **Upstream action:** [e.g., folder rename Old_Project_Name → New_Project_Name]
- **Downstream edits:** [list of files above that are downstream of this action]

### No-Change Audit

For every orientation doc you Read that does NOT need an edit, confirm explicitly:

- [filename]: no change needed (reason if non-obvious)

### Summary

One paragraph: did the sync find coherent-but-stale docs, incoherent docs, or a structural issue that needs the owner's judgment?
</return>

<approach>
This is a genuinely multi-stage rigid workflow; follow it in order.

**Phase 1 — Read the brain's nav layer.** Glob `$SECOND_BRAIN_ROOT/Orientation_Docs/*.md` and Read every file it returns. This skill is the exception to the tier system — it must read every orientation doc because its job is to sync them against each other. Also read `Second_Brain/CLAUDE.md` (skills table, active reminders) and `ROUTER.md` (tier rules). Run `python3 $SECOND_BRAIN_ROOT/scripts/update_counts.py` to get authoritative file counts.

**Phase 2 — Build the mental map of what changed.** From the Actions Taken block, enumerate every concrete thing that moved: file created, file deleted, folder renamed, skill edited, config changed, status transitioned. For each action, list the direct doc targets (count changes → MASTER_INDEX + STATE; folder changes → MASTER_INDEX + any doc that names the folder; status changes → STATE + PROCESSING_PLAN; skill changes → CLAUDE.md skills table; router rule changes → ROUTER.md).

**Phase 3 — Cascade-scan.** For every action that names a string (project name, folder name, skill name), grep that string across all Orientation_Docs to find every doc that references it. Every such reference is a cascade candidate. Evaluate each: does the doc's context require an edit, or is the reference historical? Propose edits for the former and note the latter in the No-Change Audit.

**Phase 4 — Propose, don't apply.** For every discrepancy, produce one entry in the Proposed Edits list with absolute path, line reference, current text, proposed replacement, and reason. Proposals are returned to the orchestrator for approval; the orchestrator (not you) applies them and commits.

Paths are absolute. Stay inside the scope of Actions Taken — do not propose edits motivated by your own opinion about what orientation docs should contain.
</approach>

<examples>
<example>
Actions Taken:
- Created 5 files in `Inventions/Atoms/` (daily brain dump batch, 2026-04-21).
- Renamed folder `Projects/Old_Project_Name/` → `Projects/New_Project_Name/`.

Sub-agent reads ORIENTATION_Docs/*.md, runs update_counts.py, and greps `Old_Project_Name` across all orientation docs. Finds 10 orientation docs reference the old name.

Proposed Edits (excerpt):

- **File:** `$SECOND_BRAIN_ROOT/Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md`
- **Line ref:** Line 24 (Stats table)
- **Current:** `| ~7757 | 14 | Apr 16, 2026 |`
- **Proposed:** `| 7762 | 14 | Apr 21, 2026 |`
- **Reason:** File creation action; update_counts.py reports 7762 total as of today.

- **File:** `$SECOND_BRAIN_ROOT/Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`
- **Line ref:** Line 487 (Active Projects table)
- **Current:** `| Old_Project_Name | Tier 2 | ... |`
- **Proposed:** `| New_Project_Name (formerly Old_Project_Name) | Tier 2 | ... |`
- **Reason:** Cascade from folder rename. Project-name visibility requires the rename to propagate to the Active Projects table.

Cascade Map:
- **Upstream action:** folder rename `Old_Project_Name` → `New_Project_Name`
- **Downstream edits:** INTELLECTUAL_LANDSCAPE.md (line 487, 501), STATE_OF_SECOND_BRAIN.md (line 42), TODO_MASTER.md (line 88), KEYWORD_GUIDE.md (line 156), TRACKING_LOG.md (line 31)

No-Change Audit:
- CONTENT_TAXONOMY.md: no change needed (no reference to Old_Project_Name)
- COGNITIVE_PROFILE.md: no change needed (timeless content, not project state)
</example>
</examples>

<constraints>
- Read every orientation doc by Globbing the directory — do not assume a fixed list. New docs may have been added since the last sync.
- Propose edits for BOTH the direct targets (obvious from the action) AND the cascade targets (docs that silently reference the thing that changed). Missing a cascade is a recall failure.
- Return absolute paths, not relative. Every proposed edit names the line or section that changes, and quotes the current text verbatim so the orchestrator can apply the edit with a find/replace.
- Stay inside the scope of Actions Taken. Do not propose edits that are unrelated to the action (those belong to weekly maintenance, not this sync).
- When you stage the eventual commit (after approval), add files individually by path. Using `git add -A` or `git add .` can sweep in other agents' uncommitted work on this shared working tree.
- Orientation_Docs paths and protected read-only paths (like `__FILL_FROM_USER__:protected_readonly_path`) are never edit targets — if an action affects those, flag it in the Summary for the owner rather than proposing an edit.
- Propose only; do not apply. The orchestrator will decide what to accept and handle the Edit + commit steps.
</constraints>

<verify>
Before returning, confirm:
- Every proposed-edit file path is absolute and exists on disk (Glob or Read to confirm).
- Every `Current:` field is exact text that appears at the named line of the file (re-open the file and search for the string before finalizing).
- Every proposed edit traces back to a concrete action from the Actions Taken block — no proposals motivated by your general opinions about orientation docs.
- Every orientation doc you Read is either referenced in Proposed Edits or listed in the No-Change Audit — no doc is silently skipped.
- For every string-named action (folder name, project name, skill name), you grepped that string across all Orientation_Docs and every hit is either in Proposed Edits or in No-Change Audit with an explicit reason.
- No proposed edit points into any read-only protected path (see `__FILL_FROM_USER__:protected_readonly_path` in constraints above).
</verify>

<done>
A proposal report the orchestrator can act on without re-scanning. If the orchestrator would still have to grep to find cascade targets after reading your output, the sync isn't done.
</done>

<return>
Return the proposal report exactly as specified in the `<return>` block above. Use the four headings in the listed order (Proposed Edits, Cascade Map, No-Change Audit, Summary). Keep prose outside those sections to a minimum so the orchestrator can parse proposals as a list.
</return>

<context>
**Actions Taken:**

[paste the actions that triggered this sync — file creates/deletes, folder renames, skill edits, status changes]

**Authoritative state sources:**

- Orientation docs: `$SECOND_BRAIN_ROOT/Orientation_Docs/*.md` (Glob this to get the current list)
- File counts: `python3 $SECOND_BRAIN_ROOT/scripts/update_counts.py`
- Project CLAUDE.md: `$SECOND_BRAIN_ROOT/CLAUDE.md` (skills table, active reminders, hard rules)
- Router: `$SECOND_BRAIN_ROOT/Orientation_Docs/ROUTER.md`
- Protected read-only path (never edit): `__FILL_FROM_USER__:protected_readonly_path` (e.g. an imported biographical archive or original source directory)
</context>

---

## Key Principles

1. **Read ALL docs** - This skill is the EXCEPTION to the Tier system. Its job is to sync docs, so it must read them all.

2. **Propose before apply** - Submit proposed changes for approval first. Don't make changes without approval.

3. **Targeted edits** - Don't rewrite entire docs. Make surgical edits only.

4. **Log significant changes** - Add entries to `TRACKING_LOG.md` when warranted.

5. **Commit after syncing** - Stage only files YOU modified (never `git add -A`). See CLAUDE.md git etiquette.

6. **Use Sonnet for sync tasks** - Doc comparison and editing needs accuracy but not Opus-level reasoning.

7. **Check dynamically** - Don't assume a fixed list of docs. Glob the Orientation_Docs/ folder to find all current docs.

## Example Task Call

```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  prompt="Task: Sync Orientation Docs\n\nActions Taken: Created 5 new idea files in Inventions/, ran /update-index\n\n[full instructions from above]"
)
```

## Integration

This skill should be called:
- After ANY action listed in ORIENTATION.md SYNC TRIGGERS section
- After update-index runs (if file counts changed)
- After process-content creates new files
- After completing processing phases
- After modifying any orientation doc

## Parent Instance Responsibility

The main instance is responsible for:
1. Tracking what actions have been taken (by itself and by subagents)
2. Determining when triggers have been met
3. Invoking this skill with accurate `actions_taken` description
4. Approving or rejecting proposed changes
5. NOT waiting for user to ask - this is automatic
