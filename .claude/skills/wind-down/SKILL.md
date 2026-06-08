---
name: wind-down
description: >-
  Persist session progress before context compaction or session end.
  Use when user says "wind down", "checkpoint", "save progress", "done", or "finished".
  Auto-triggered via PreCompact hook. PostCompact hook verifies execution.
required_context_files:
  - Orientation_Docs/STATE_OF_SECOND_BRAIN.md
  - Orientation_Docs/TODO_MASTER.md
  - Orientation_Docs/TRACKING_LOG.md
---

# Wind-Down

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/STATE_OF_SECOND_BRAIN.md`
- `Orientation_Docs/TODO_MASTER.md`
- `Orientation_Docs/TRACKING_LOG.md`

<!-- silent-context-load:v1 -->

Persist session progress before context compaction or session end. Designed for AUTONOMOUS operation via PreCompact hook, with manual fallback for early session exits.

## Trigger Conditions

**Automatic (PreCompact hook):**
- Fires before context compaction
- Uses `checkpoint` mode
- No human intervention needed

**Manual - Checkpoint mode:**
- "wind down", "checkpoint", "save progress"
- Preserves in-progress state

**Manual - Complete mode:**
- "done", "finished", "task complete", "I'm stopping"
- Clears in-progress state, marks task complete

## Required Context (Tier 2 Dependencies)

Before winding down, read:

1. **STATE_OF_SECOND_BRAIN.md** - For phase status updates
2. **TRACKING_LOG.md** - For session log entries
3. **TODO_MASTER.md** - For task routing
4. **TODO_Second_Brain.md** - Check HIGHEST PRIORITY section for blocking items

Note: the current phase is tracked in STATE_OF_SECOND_BRAIN.md.

## Process

### Step 1: Determine Mode

Parse the trigger:
- PreCompact hook → `checkpoint` mode
- "wind down", "checkpoint", "save progress" → `checkpoint` mode
- "done", "finished", "complete", "stopping" → `complete` mode
- Default if unclear → `checkpoint` mode

### Step 2: Gather Session State

Identify what was done this session:
- Files created in Second_Brain/
- Files modified (including ORIENTATION.md files in any folder)
- Orientation tracking docs updated
- Tasks completed
- Remaining work count

### Step 3: Update Docs

If phase status changed:
- Update the CURRENT STATUS table in STATE_OF_SECOND_BRAIN.md

Add session entry to TRACKING_LOG.md (always).

Stage and commit only session-touched files:

**Checkpoint:**
```bash
git add [touched files]
git commit -m "Wind-down checkpoint: [brief description of work]"
```

**Complete:**
```bash
git add [touched files]
git commit -m "Wind-down: [task description] complete"
```

### Step 5: Output Summary

**Checkpoint mode:**
```markdown
## Session Checkpoint Saved

**Mode:** Checkpoint (mid-task)
**State persisted:**
- [list files created/modified]

**Git commit:** [hash]

**To continue:**
- Start new instance (auto-reads orientation docs)
- Pick up from: [specific next action]

**Note:** Compaction will now proceed. New instance will have fresh context.
```

**Complete mode:**
```markdown
## Task Complete - Session Closed

**Mode:** Complete (task finished)
**Final state:**
- [list files created/modified]

**Git commit:** [hash]

**Next instance will start fresh** - no stale in-progress state.
**Next task:** [Check TODO_Second_Brain.md HIGHEST PRIORITY section first, then TODO_MASTER.md]
```

## Key Principles

1. **Autonomous first** - Designed to run automatically via PreCompact hook
2. **Updates existing docs** - No new state files, uses established tracking docs
3. **Git commit is the checkpoint** - Provides rollback safety
4. **Explicit continuation prompt** - Next instance knows exactly where to pick up
5. **Two modes** - Checkpoint preserves in-progress; Complete clears it

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `sync-orientation-docs` | Wind-down handles the subset of docs that need updating |

## Files Touched

| File | When Updated |
|------|--------------|
| `STATE_OF_SECOND_BRAIN.md` | If phase status changed |
| `TRACKING_LOG.md` | Always (session log entry) |
| `TODO_MASTER.md` | If tasks completed |
| Project TODO files | If project work done |
| _(orientation-review log)_ | If orientation docs reviewed |

## Error Handling

If git commit fails:
- Log the error
- Still output the summary
- Note that commit failed, manual commit needed

## Example Invocations

**PreCompact hook fires:**
→ Wind-down runs in checkpoint mode automatically
→ Updates docs, commits, outputs summary
→ Compaction proceeds with state safely persisted

**User says "done for today":**
→ Wind-down runs in complete mode
→ Clears in-progress state
→ Commits with "complete" message
→ Next instance starts fresh

**User says "save progress, I'll continue later":**
→ Wind-down runs in checkpoint mode
→ Preserves in-progress state
→ Commits with "checkpoint" message
→ Next instance can resume mid-task
