<!-- __FILL_FROM_USER__:media_pipeline_example
     FOR THE AGENT READING THIS — THIS IS A GENERIC EXEMPLAR.
     It teaches the shape of a multi-stage media-processing skill with a human
     triage gate in the middle. Adapt it to the owner's real media sources
     (podcasts, videos, photo libraries, audio recordings, etc.).
     Replace every __FILL_FROM_USER__ marker with owner specifics.
     After adapting, rename this directory and update CLAUDE.md's skills table. -->
---
name: media-pipeline-example
description: >-
  Generic exemplar — multi-stage media pipeline with a HUMAN TRIAGE GATE. Teaches:
  detect new media → process/transcribe → enrich → emit a docket the human marks →
  produce final outputs from marked items only. Use as a model for podcast-clip,
  photo-curation, or any two-phase media workflow.
  Triggers: "process new media", "run the pipeline".
model: sonnet
---

# Media Pipeline (Example Pattern)

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

No required_context_files for this exemplar. A real implementation may need
INTELLECTUAL_LANDSCAPE.md and owner-specific classification context — add them to
`required_context_files` in the frontmatter when adapting.

<!-- silent-context-load:v1 -->

Two-phase pipeline split at a **human triage gate**. Phase 1 prepares; Phase 2 produces.
The owner marks a docket between phases, deciding what to act on. Nothing is published
or destructively modified before the gate.

## Overview

```
[Phase 1: Prepare]
  Detect new media items
      ↓
  Process each item (transcode / transcribe / extract metadata)
      ↓
  Enrich each item (classify / generate summary / tag)
      ↓
  Emit TRIAGE DOCKET

[HUMAN TRIAGE GATE — owner marks items: KEEP / SKIP / LATER]

[Phase 2: Produce]
  Read marked docket
      ↓
  Produce final outputs for KEEP items only
      ↓
  Report results
```

## Phase 1 — Prepare

```
- [ ] Step 1: Detect new items in source (compare against state ledger)
              Source: __FILL_FROM_USER__:media_source (e.g. an export folder, an API endpoint)
              State ledger: __FILL_FROM_USER__:state_file (e.g. vault_state.json)
- [ ] Step 2: For each new item — process:
              __FILL_FROM_USER__:processing_step (e.g. extract audio, run transcription, pull EXIF)
- [ ] Step 3: For each item — enrich:
              __FILL_FROM_USER__:enrichment_step (e.g. generate summary, classify topic, detect faces)
- [ ] Step 4: Write TRIAGE DOCKET (see format below)
- [ ] Step 5: Report to owner: "N items ready for triage. Docket: <path>"
- [ ] Step 6: STOP — wait for owner to mark the docket before proceeding
```

## Triage Docket Format

One line per item. Owner marks each line before Phase 2 begins.

```
# Triage Docket — <date>
# Mark each item: KEEP | SKIP | LATER
#
# KEEP   → Phase 2 will produce output for this item
# SKIP   → ignore (no output, no archive)
# LATER  → defer to the next run

KEEP   item_001  | __FILL_FROM_USER__:summary_field
SKIP   item_002  | ...
LATER  item_003  | ...
```

Docket location: `__FILL_FROM_USER__:docket_path` (e.g. `Ingestion_Archive/triage_docket.md`)

## Phase 2 — Produce

Invoked only after the owner marks the docket.

```
- [ ] Step 1: Parse docket — collect all KEEP items
- [ ] Step 2: For each KEEP item — produce final output:
              __FILL_FROM_USER__:output_step (e.g. clip video, write Template B, export image)
- [ ] Step 3: Update state ledger (mark items as processed)
- [ ] Step 4: Report: N outputs produced, paths listed
```

## Critical Rules

1. **GATE IS MANDATORY** — Phase 2 never auto-starts. Always wait for explicit owner approval via the marked docket.
2. **STATE LEDGER IS THE SOURCE OF TRUTH** — Never re-process items already in the ledger without explicit instruction.
3. **NON-DESTRUCTIVE FIRST** — Originals are read-only. Outputs go to a separate destination folder.
4. **REPORT AT THE GATE** — When handing off to the owner, give enough context per item that they can triage without re-reading raw media.

## Adapting This Exemplar

To build a real skill from this pattern:
1. Fill all `__FILL_FROM_USER__` markers with owner-specific paths, APIs, and steps.
2. Define the state ledger schema (what counts as "already processed").
3. Define the enrichment step (what metadata/summaries/tags to generate).
4. Define the output format (Template B, a clip file, a tagged photo, etc.).
5. Rename the directory and add a trigger phrase to CLAUDE.md's skills table.
