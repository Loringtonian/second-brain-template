---
name: load-brain
description: >-
  Load the essential Second Brain (large) into context.
  Your core original thinking: journals, inventions, predictions, writing, health, lists.
  Light trim removes redundant metadata; keeps Summary, Keywords, Connections, Original Text.
  Excludes external sources, bulk fiction, transcripts, code/builds, and docs already loaded via rules.
  Use when user says "load brain", "load everything", "full context", "deep context".
allowed-tools:
  - Bash
  - Read
---

# Load Brain

Reads your core intellectual output into context via a pre-built snapshot file.

> **Stub notice:** `scripts/build_brain_snapshot.py` is not yet implemented. Fill it in
> (see SETUP.md) before `/load-brain` will work end-to-end. Once implemented, this skill
> runs exactly as described below.

## Context Budget (1M model)

| Component          | Approximate size |
|--------------------|-----------------|
| Snapshot content   | large           |
| Read tool overhead | ~55K tokens     |
| System context     | ~75K tokens     |
| **Conversation**   | remaining headroom |
| **Total**          | **~1,000K**     |

The exact snapshot size depends on your content. Run `python3 scripts/build_brain_snapshot.py`
to see a breakdown after implementing the script.

## What Gets Loaded

Light trim: `## Metadata`, `## Classification`, `## Source`, `## Status` removed during build.
Kept: Title, Summary, Project Connections, Connections, Keywords, Original Text.

| Category               | Description                           |
|------------------------|---------------------------------------|
| Inventions             | Original invention and idea notes     |
| Journal Intellectual   | Intellectual / philosophical entries  |
| Journal Personal       | Personal reflective entries           |
| Writing SciFi          | Original science fiction writing      |
| Predictions            | Forward-looking notes and forecasts   |
| Writing AllElse        | Essays, posts, miscellaneous writing  |
| Health                 | Health observations and tracking      |

Configure `ESSENTIAL_DIRS` in the script to match your own content folders (see SETUP.md).

## What's Excluded (and why)

| Category                         | Reason                                                  |
|----------------------------------|---------------------------------------------------------|
| Orientation Docs (key files)     | Already loaded via `.claude/rules/` symlinks            |
| Projects/ docs                   | STATE_OF_SECOND_BRAIN (via rules) covers project status |
| External sources / third-party   | Not your original thinking                              |
| AI-generated drafts              | Unreviewed; noise in a synthesis context                |
| Bulk fiction (large sub-folder)  | Token-heavy; load separately when needed                |
| Raw transcripts / vault          | Massive token footprint; rarely needed whole            |
| Reference / To_Study             | External references, learning queue                     |
| Code, builds, media, binary      | Not prose content                                       |

## Process

### Step 1: Regenerate Snapshot

```bash
python3 scripts/build_brain_snapshot.py
```

This builds two files (paths relative to repo root):
- `.claude/brain_snapshot.md` — the concatenated content (gitignored)
- `.claude/brain_load_instructions.md` — exact Read parameters per batch

### Step 2: Read the Instruction File

```
Read(file_path="<repo-root>/.claude/brain_load_instructions.md")
```

The instruction file is short (~75 lines). It contains the exact Read calls grouped into batches,
generated from the actual line count of the snapshot.

### Step 3: Execute Batch 1

Fire ALL Read calls listed under `## Batch 1` as parallel Read calls.
Use the EXACT `file_path`, `offset`, and `limit` values from the instruction file.

### Step 4: Execute Batch 2

Fire ALL Read calls listed under `## Batch 2` as parallel Read calls.

### Step 5: Execute Batch 3

Fire ALL Read calls listed under `## Batch 3` as parallel Read calls.

### Step 6: Execute Additional Batches (if any)

If the instruction file has more than 3 batches (the brain grew), execute each additional
batch the same way.

### Step 7: Confirm

Report to user with the snapshot stats printed by the build script:
- Total files and tokens loaded
- Remaining conversation headroom
- Any orientation docs already in context via rules (skip re-reading those)

## CRITICAL RULES

These exist because the Read tool has a **hard 10,000 token per call limit**.
650 lines = ~8,125 tokens. This is safe. 1,000 lines = ~12,500 tokens. This FAILS.

- **NEVER use limit > 650.** Every Read call MUST use `limit=650` or less.
- **NEVER combine batches.** Execute Batch 1, wait for ALL reads to complete, then Batch 2, etc.
- **NEVER modify offsets or limits.** Use the EXACT values from `brain_load_instructions.md`.
- **NEVER improvise a different chunking strategy.** The instruction file is generated from
  the actual file size and is always correct.
- **NEVER stop between batches to ask the user.** Load everything, then report.
- **NEVER recalculate chunk sizes.** The instruction file already did the math.
- If a single Read call fails, retry that specific call once. If it fails again, skip it and continue.
- The instruction file is the source of truth. If this SKILL.md text conflicts with the
  instruction file, the instruction file wins.

## Freshness

- Snapshot + instructions are regenerated each time `/load-brain` runs (Step 1).
- Also regenerate after significant content additions (e.g., during maintenance runs).
- `FILE:` markers inside the snapshot show the exact source path for traceability.

## When to Use

- Starting a deep analysis session ("tell me about my patterns")
- Cross-referencing ideas across the entire brain
- Finding connections between distant topics
- Preparing for a writing or synthesis session that needs full context
