# MINING — Seeding a Brain From a Large Source (with Calibration)

> How to turn a big existing export — a notes-app dump, chat history, a voice-note archive,
> bookmarks, podcast snips — into clean, correctly-classified Template A/B files **without** the
> agent's first-pass judgment quietly miscategorizing thousands of items.
>
> The load-bearing practice: **calibrate the agent's judgment on small batches first; only then set
> it loose on the bulk.** This is the procedure behind the principle *"invest in structure and
> calibrate the AI judgement early."* Run it with the `/mine` skill.

---

## Why calibration, not just ingestion

A fresh brain's classifier is the shipped `CONTENT_TAXONOMY.md` + the routing/classification rules +
an empty `KEYWORD_GUIDE.md`. Run a 3,000-item export through that cold and you get the agent's
*uncalibrated* taste: borderline ideas filed in the wrong folder, your terms-of-art left untagged,
duplicates created, the wrong template chosen (A vs B). Those errors compound silently across the
whole archive — and you discover them months later, one wrong file at a time.

Calibration fixes this cheaply. You correct the agent on ~10 items at a time, and **every correction
is written back into the rules**, so the same mistake never recurs. After a few rounds the agent is
reproducing *your* calls, and the remaining thousands process correctly on their own.

This is the single practice that separates a noisy brain from a clean one. Spend the hour early.

---

## The loop

### Phase 1 — Calibrate (batches of 10)

1. **Load the rules.** `CONTENT_TAXONOMY.md`, `KEYWORD_GUIDE.md`, the routing rules
   (`.claude/skills/ingest-brain-dump/references/routing-rules.md`) and classification rules
   (`.claude/skills/process-content/references/classification-rules.md`), plus
   `INTELLECTUAL_LANDSCAPE.md` (who the owner is).
2. **Take the next 10 items** from the source. For each: segment semantically → dedup-check with
   `/verify-idea` → classify + route → draft the **full** Template A/B (verbatim Original Text,
   keywords, project connections). Never algorithmic chunking — a paragraph may hold 3 ideas; 5
   paragraphs may be 1.
3. **Present all 10** for review — full drafts, not a summary. You cannot correct what you cannot see.
4. **The owner corrects.** Wrong category, wrong template (A vs B), a missed duplicate, a bad
   split/merge, a missing keyword, a wrong project connection.
5. **Fold every correction back into the rules.** Add the category boundary to `CONTENT_TAXONOMY.md`,
   the routing case to the routing rules, the term to `KEYWORD_GUIDE.md`. *The rules are the memory of
   the calibration* — a correction that isn't written back will be made again.
6. **Repeat** with the next 10. Track corrections per batch — the count should fall.

**Convergence test:** when a batch comes back with ~no corrections — the owner reads all 10 and says
"yes, these are right, you've got it" — the agent has the owner's judgment. That is the signal to stop
calibrating.

### Phase 2 — Set loose (bulk mine)

7. With the converged rules, process the remaining source **autonomously** in batches: segment →
   dedup → classify → full Template → `validate_template.py` → log progress. Spot-check a batch every
   so often. If the agent drifts on a new *kind* of content, drop back to a single calibration batch,
   fold the fix in, and resume. Convergence is not permanent — a new source shape can need a retune.

---

## When to use

- **Seeding a new brain** from any large export — the first big import.
- **Adding a new source type** later (you start importing a new app's data) — calibrate that source's
  quirks on 10 before bulk-running it.
- **When bulk output quality drops** — a short re-calibration retunes the rules.

## Run it

Say **"mine my [source]"**, "calibrate the mining", or "idea mining" → the `/mine` skill runs this
loop. For in-session pasted or dictated thoughts (not a bulk export), use `/ingest-brain-dump` instead.
