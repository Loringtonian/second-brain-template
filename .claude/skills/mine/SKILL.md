---
name: mine
description: >-
  Seed a brain from a LARGE existing source by TRIAGING it, then calibrating the
  agent's judgment on small batches, then bulk-mining. Use when the owner says
  "mine my [source]", "mine this export", "calibrate the mining", "idea mining",
  "process my archive", or "seed my brain from this export" — pointing at a sizable
  export (notes-app dump, chat history, voice-note archive, bookmarks, podcast snips).
  Phase 0 TRIAGE: categorize the source into keep/skip bins, sample the skip-bins,
  get owner approval per bin, build the target list. Phase 1 CALIBRATE: small batches
  → present COMPACT numbered proposals (verbatim quote + the agent's call + one-line
  reason, no tables) → owner corrects → write every correction back into the rules
  (CONTENT_TAXONOMY / KEYWORD_GUIDE / INTELLECTUAL_LANDSCAPE) → draft the full Template
  only after the calls are approved → repeat until a batch is clean. Phase 2 SET LOOSE:
  process the remainder autonomously, spot-check, re-calibrate on drift. Implements
  "invest in structure and calibrate the AI judgement early"; full procedure in
  Orientation_Docs/MINING.md.
  NOT for in-session pasted/dictated thoughts (use /ingest-brain-dump).
  Preserves the owner's exact language — no paraphrasing.
required_context_files:
  - Orientation_Docs/MINING.md
  - Orientation_Docs/CONTENT_TAXONOMY.md
  - Orientation_Docs/KEYWORD_GUIDE.md
  - Orientation_Docs/INTELLECTUAL_LANDSCAPE.md
---

# Mine (Triage → Calibrate → Set Loose)

Turn a large existing source into clean Template A/B files. **Triage it first so you only mine what's
worth mining; calibrate the agent's judgment on small batches; then set it loose on the bulk.** Full
rationale: `Orientation_Docs/MINING.md`.

## Quick Start

1. **Triage:** categorize the source into keep/skip bins → sample each skip-bin (~10) → owner approves
   per bin → build the target list.
2. **Calibrate:** small batch → present compact numbered proposals → owner corrects → write corrections
   back into the rules → draft full Templates only after the calls are approved → repeat until clean.
3. **Set loose:** process the remainder autonomously with the converged rules; spot-check; re-calibrate
   on drift.

## Workflow Checklist

Copy and track:

```
- [ ] PHASE 0 — TRIAGE
      - [ ] Budget it: estimate the source's token size (`scripts/estimate_tokens.py <path> --budget <plan>`) vs the owner's plan; if reading it all blows the session, stage it across quota resets
      - [ ] Categorize the whole source into coarse keep/skip bins by kind
      - [ ] Sample each skip-bin (~10 items) with a one-line observation
      - [ ] STOP — owner approves each bin (propose, don't decide)
      - [ ] Produce the target list, in an agreed order
- [ ] Load rules: CONTENT_TAXONOMY.md, KEYWORD_GUIDE.md, routing-rules.md, classification-rules.md, INTELLECTUAL_LANDSCAPE.md
- [ ] PHASE 1 — CALIBRATE (repeat):
      - [ ] Take a small batch (~5–10 targets)
      - [ ] Per item: semantic segment → /verify-idea dedup → classify + route
      - [ ] Present COMPACT numbered proposals (verbatim quote + call + one-line reason; NO tables, NOT full files)
      - [ ] Collect the owner's corrections to the calls
      - [ ] Write EACH correction back: CONTENT_TAXONOMY.md / KEYWORD_GUIDE.md / INTELLECTUAL_LANDSCAPE.md (project boundaries)
      - [ ] After the calls are approved, draft the FULL Template A/B and present before saving (Create? Y/N)
      - [ ] Log corrections-this-batch; loop until a batch is clean (~0 corrections)
- [ ] PHASE 2 — SET LOOSE:
      - [ ] Process remaining targets autonomously in larger batches with the converged rules
      - [ ] Dedup each; log progress (processed, created, duplicates skipped)
      - [ ] validate_template.py + verify-second-brain as you go (recommended)
      - [ ] Spot-check periodically; on drift, drop to one calibration batch, fold the fix, resume
- [ ] Report: bins skipped (approved), items mined, files created, dedups skipped, rules updated
```

## Critical Principles

1. **Triage before you calibrate.** A raw export is mostly noise; sample the skip-bins and get the
   owner's approval before processing anything in bulk. Agents propose, the owner decides.
2. **Calibrate before the bulk pass.** A cold classifier mis-files at scale and you find out one wrong
   file at a time. A few correction rounds up front save thousands of silent errors.
3. **Present compact proposals, not full files.** During calibration show one numbered item per idea —
   verbatim quote + the call + a one-line reason, **no tables**. Draft the full Template only once the
   owner has approved the call (then present it before saving, per "Template A IS the artifact").
4. **Corrections are written back into the rules.** A correction not folded into `CONTENT_TAXONOMY.md` /
   `KEYWORD_GUIDE.md` / `INTELLECTUAL_LANDSCAPE.md` will be made again. The rules are the memory of the
   calibration — this is what makes the loop converge.
5. **Find a home for everything.** Default to filing; skipping is rare and reserved for the obviously
   content-free. When unsure, file it.
6. **An external reference is not an auto-skip.** A note about someone else's work still earns a
   reading-list / concept / tool note (Template B, attributed).
7. **Split multi-idea items, and verify the split.** Note the expected number of ideas before splitting
   and the extracted number after; if extracted < expected, review before approving.
8. **Semantic segmentation, never algorithmic chunking.** A paragraph may hold several ideas; several
   paragraphs may be one.
9. **Preserve exact language; mine the owner's words.** Original Text is verbatim; keywords are the
   owner's actual terms. In a multi-speaker source (chat export, interview), mine only the owner's side.
10. **Convergence is the stop signal — and it's not permanent.** Stop calibrating when a batch comes
    back clean; resume calibrating when a new source shape makes the bulk pass drift.

## Phase 0 — Triage

- **Budget it first.** Estimate how much reading the source in full would cost —
  `python3 scripts/estimate_tokens.py <path> --budget <plan-tokens>` — and weigh it against the owner's
  plan (Claude Pro vs Max, or an API budget). If reading everything would blow one session window, plan
  to **stage** the mine across quota resets (a Pro ~5-hour window, overnight, week's end) and use a
  cheap/fast model for the bulk reading. Sizing up front is what stops a single import from burning the
  whole plan.
- Categorize the whole source into coarse bins by kind (keep kinds vs skip kinds).
- For each skip-bin, pull ~10 items, state a one-line observation, and present the sample.
- **Stop for the owner's approval per bin** — "skip it" / "sample more" / "keep these." No bin is
  skipped on the agent's judgment alone.
- Produce the mining target list in an order the owner agrees. For a mixed keep-bin, sample a few and
  agree an approach first; don't auto-pilot.

## Phase 1 — Calibrate (small batches)

For each batch:
- Pull a small batch (~5–10) of targets in the agreed order.
- Per item: segment → `/verify-idea` (skip true duplicates, surface near-duplicates) → classify per
  `CONTENT_TAXONOMY.md` + the classification rules → decide routing per the routing rules.
- **Present compact numbered proposals:** verbatim quote · the call (category / template / project) ·
  one-line reason. No tables, no full files yet.
- The owner corrects the calls. **Write back** for every correction — a new boundary in
  `CONTENT_TAXONOMY.md`, a term in `KEYWORD_GUIDE.md`, a project-boundary call in
  `INTELLECTUAL_LANDSCAPE.md`. Note what changed.
- Once the calls are approved, draft the **full Template A** (original thinking) or **Template B**
  (external, attributed) and present before saving.
- Track corrections per batch. When a batch comes back clean, calibration has converged.

## Phase 2 — Set loose (bulk mine)

- Process the remaining targets autonomously in larger batches, applying the converged rules.
- Dedup-check each item; log progress (processed, created, duplicates skipped). Validating each created
  file (`validate_template.py`) and running `verify-second-brain` is recommended.
- Spot-check a batch periodically. On drift, drop to one calibration batch, fold the fix into the rules,
  resume.

## Integration

| Skill / script | When | Status |
|---|---|---|
| `scripts/estimate_tokens.py` | Phase 0 — size the source vs the plan before reading | core |
| `/verify-idea` | Per item — duplicate detection before creating a file | core |
| `/process-content` | The per-item segment → classify → Template-create mechanic | core |
| `.claude/scripts/validate_template.py` | Validate created files in the bulk pass | recommended |
| `verify-second-brain` agent | Template/placement/keyword/language check | recommended |
| `/ingest-brain-dump` | The in-session counterpart (pasted/dictated thoughts, not a bulk export) | sibling |

## Verification Checklist

Before calling a mine run done, confirm:
- Every skip-bin was sampled and **approved by the owner** — none skipped on the agent's say-so.
- Every correction the owner made during calibration was written back into a rule file
  (`CONTENT_TAXONOMY.md` / `KEYWORD_GUIDE.md` / `INTELLECTUAL_LANDSCAPE.md`).
- Multi-idea items were split, and each split's extracted count met or exceeded the expected count.
- The bulk pass used the converged rules (not the shipped defaults).
- Original Text is verbatim; external content is Template B with attribution; in multi-speaker sources
  only the owner's words were mined.
- You reported bins skipped, items mined, files created, duplicates skipped, and which rules were updated.
