---
name: mine
description: >-
  Seed a brain from a LARGE existing source by calibrating the agent's judgment on
  small batches before the bulk pass. Use when the owner says "mine my [source]",
  "mine this export", "calibrate the mining", "idea mining", "process my archive",
  or "seed my brain from this export" — and points at a sizable export (notes-app
  dump, chat history, voice-note archive, bookmarks, podcast snips).
  Two phases: (1) CALIBRATE — process batches of 10, present full drafts, the owner
  corrects, every correction is written back into the rules, repeat until a batch is
  clean; (2) SET LOOSE — process the remaining source autonomously with the converged
  rules. Implements the principle "invest in structure and calibrate the AI judgement
  early"; full procedure in Orientation_Docs/MINING.md.
  NOT for in-session pasted/dictated thoughts (use /ingest-brain-dump).
  Preserves the owner's exact language — no paraphrasing.
required_context_files:
  - Orientation_Docs/MINING.md
  - Orientation_Docs/CONTENT_TAXONOMY.md
  - Orientation_Docs/KEYWORD_GUIDE.md
  - Orientation_Docs/INTELLECTUAL_LANDSCAPE.md
---

# Mine (with Calibration)

Turn a large existing source into clean Template A/B files. **Calibrate the agent's judgment on
small batches first; only then set it loose on the bulk.** Full rationale: `Orientation_Docs/MINING.md`.

## Quick Start

1. Identify the source and roughly how many items it holds.
2. **Calibrate:** process the next 10 → present full drafts → owner corrects → write corrections back
   into the rules → repeat until a batch is clean.
3. **Set loose:** process the remainder autonomously with the converged rules; spot-check; re-calibrate
   on drift.

## Workflow Checklist

Copy and track:

```
- [ ] Load rules: CONTENT_TAXONOMY.md, KEYWORD_GUIDE.md, routing-rules.md, classification-rules.md, INTELLECTUAL_LANDSCAPE.md
- [ ] Confirm the source + item count with the owner; agree the source order
- [ ] PHASE 1 — CALIBRATE (repeat):
      - [ ] Take the next 10 items
      - [ ] Per item: semantic segment → /verify-idea dedup → classify + route → full Template A/B draft
      - [ ] Present all 10 in full (not summaries) for review
      - [ ] Collect the owner's corrections
      - [ ] Fold EACH correction back into the rules (taxonomy / routing / keyword guide)
      - [ ] Log corrections-this-batch; loop until a batch is clean (~0 corrections)
- [ ] PHASE 2 — SET LOOSE:
      - [ ] Process remaining items in batches with the converged rules
      - [ ] validate_template.py on every file; log progress
      - [ ] Spot-check periodically; on drift, drop to one calibration batch, fold the fix, resume
- [ ] Report: items mined, files created, dedups skipped, rules updated
```

## Critical Principles

1. **Calibrate before bulk.** A cold classifier mis-files at scale and you find out one wrong file at
   a time. Ten minutes of correction up front saves thousands of silent errors.
2. **Corrections are written back into the rules.** A correction that isn't folded into
   `CONTENT_TAXONOMY.md` / the routing rules / `KEYWORD_GUIDE.md` will be made again. The rules are the
   memory of the calibration — this is what makes the loop converge.
3. **Present full drafts, not summaries.** The owner can only correct what they can see. Show complete
   Template A/B for every item in the batch.
4. **Semantic segmentation, never algorithmic chunking.** A paragraph may hold 3 ideas; 5 paragraphs
   may be 1.
5. **Preserve exact language.** The Original Text is verbatim. Keywords are the owner's actual terms.
6. **Convergence is the stop signal — and it's not permanent.** Stop calibrating when a batch comes
   back clean; resume calibrating when a new source shape makes the bulk pass drift.

## Phase 1 — Calibrate (batches of 10)

For each batch:
- Pull the next 10 source items in agreed order.
- For each: segment → `/verify-idea` (skip true duplicates, surface near-duplicates) → classify per
  `CONTENT_TAXONOMY.md` + the classification rules → route per the routing rules → draft the **full**
  Template A (owner's original thinking) or Template B (external content, attributed).
- Present all 10 together. Ask the owner to correct category, template, dedup calls, splits/merges,
  keywords, and project connections.
- **Write back:** for every correction, update the relevant rule file so the next batch reflects it
  (a new category boundary in `CONTENT_TAXONOMY.md`; a routing case in `routing-rules.md`; a term in
  `KEYWORD_GUIDE.md`). Note what changed.
- Track corrections per batch. When a batch is clean (the owner reviews 10 and changes ~nothing),
  calibration has converged.

## Phase 2 — Set loose (bulk mine)

- Process the remaining source autonomously in batches, applying the converged rules.
- Run `validate_template.py` on every created file; dedup-check each item; log progress
  (items processed, files created, duplicates skipped).
- Spot-check a batch periodically. If quality drops on a new kind of content, drop back to one
  calibration batch, fold the fix into the rules, and resume the bulk pass.

## Integration

| Skill / script | When |
|---|---|
| `/verify-idea` | Per item — duplicate detection before creating a file |
| `/process-content` | The per-item segment → classify → Template-create mechanic |
| `.claude/scripts/validate_template.py` | Validate every created file |
| `/ingest-brain-dump` | The in-session counterpart (pasted/dictated thoughts, not a bulk export) |

## Verification Checklist

Before calling a mine run done, confirm:
- Every correction the owner made during calibration was written back into a rule file.
- The bulk pass used the converged rules (not the shipped defaults).
- Every created file passed `validate_template.py` and was dedup-checked.
- Original Text is verbatim everywhere; external content is Template B with attribution.
- You reported items mined, files created, duplicates skipped, and which rules were updated.
