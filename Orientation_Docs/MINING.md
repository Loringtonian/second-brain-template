# MINING — Seeding a Brain From a Large Source (Triage → Calibrate → Set Loose)

> How to turn a big existing export — a notes-app dump, chat history, a voice-note archive,
> bookmarks, podcast snips — into clean, correctly-classified Template A/B files **without** mis-filing
> thousands of items on the agent's cold first guess.
>
> Three moves, in order: **triage** the source so you only mine what's worth mining; **calibrate** the
> agent's judgment on small batches (it proposes, you correct, the corrections are written back into the
> rules); then **set it loose** on the bulk. This is the procedure behind the principle *"invest in
> structure and calibrate the AI judgement early."* Run it with the `/mine` skill.

---

## Why triage AND calibration, not just ingestion

A large source is two problems at once. First, it's **not uniform** — a raw export is mostly noise
(one-off lookups, logistics, image requests, duplicates) around a minority of real ideas; bulk-processing
it files the noise as ideas. Second, a fresh brain's classifier is the shipped `CONTENT_TAXONOMY.md` + an
empty `KEYWORD_GUIDE.md`, so even the real ideas get the agent's *uncalibrated* taste — wrong folder,
untagged terms, missed duplicates, wrong template (A vs B).

Triage solves the first; calibration solves the second. Together they're the difference between a clean
brain and a noisy one. Spend the time early — it pays back across the whole archive.

---

## Phase 0 — Triage (decide what's worth mining)

The agent **proposes; you decide.** Nothing is processed in bulk until you approve.

1. **Categorize the whole source** into a handful of coarse bins by kind — the *keep* kinds (your
   original thinking, ideas, substantive notes) and the *skip* kinds (one-off factual lookups,
   admin/logistics, pure image requests, empty or duplicate items).
2. **Sample each skip-bin** — pull ~10 items, with a one-line observation ("these all look like
   single-turn lookups"), and present the sample.
3. **Get approval per bin** — you confirm "yes, skip that bin" / "no, sample more" / "actually, keep
   these." No bin is skipped on the agent's say-so.
4. **Produce the target list** — the items to mine, in an order you agree on. For a mixed keep-bin,
   sample a few and agree an approach before processing. Don't auto-pilot.

Default to keeping (see the judgment rules below); skipping is the rare exception.

---

## Phase 1 — Calibrate (small batches, compact proposals)

1. **Load the rules as inputs:** `CONTENT_TAXONOMY.md`, `KEYWORD_GUIDE.md`, the routing/classification
   references, and `INTELLECTUAL_LANDSCAPE.md` (who the owner is).
2. **Take a small batch** (~5–10 targets). For each: segment semantically (a paragraph may hold several
   ideas; several paragraphs may be one), dedup-check with `/verify-idea`, classify, and decide routing.
3. **Present compact proposals — not full files, and no tables.** One numbered item per idea: a short
   **verbatim quote**, the agent's **call** (category / template / project), and a **one-line reason**.
   (Full drafts and tables read poorly when reviewed quickly; the full Template comes later, at the save
   gate.)
4. **You correct the calls** — wrong category, wrong template (A vs B), a missed duplicate, a bad
   split/merge, a missing keyword, a wrong project connection.
5. **Write every correction back into the rules** — the category boundary into `CONTENT_TAXONOMY.md`,
   the term into `KEYWORD_GUIDE.md`, and **project-boundary calls into `INTELLECTUAL_LANDSCAPE.md`**
   (which project an idea belongs to; where two projects split). *The rules are the memory of the
   calibration* — a correction not written back will be made again.
6. **Only after you approve the calls, draft the full Template A/B** for those items and present it
   before saving (Create? Y/N) — per "Template A IS the artifact."
7. **Repeat.** Corrections per batch should fall. **Convergence** = a batch you review with ~no
   corrections. That is the signal to stop calibrating.

---

## The judgment rules (the hard-won part)

These are what turn a generic classifier into *your* judgment. State them; follow them.

- **Find a home for everything.** Default to filing; **skipping is rare** — only the obviously
  content-free (a pure image request, a one-off lookup unrelated to your world). When unsure, file it —
  you'll say later if it's useless.
- **An external reference is not an auto-skip.** A note *about* someone else's work is still worth
  keeping — it becomes a reading-list item, a concept note, or a tool note (Template B, attributed).
  Don't discard it just because it isn't original.
- **Split multi-idea items.** When one source item holds several distinct ideas, split it into separate
  artifacts. Note the **expected** number of ideas before splitting and the **extracted** number after;
  if you extracted fewer than expected, review before approving — you may have missed one.
- **Preserve exact language.** The Original Text is verbatim; keywords are the owner's actual terms,
  never paraphrased.
- **In a multi-speaker source** (a chat export, an interview transcript), mine **only the owner's
  words** — the other party's text isn't the owner's thinking, and including it would misattribute ideas.
- **Catch inspiration triggers.** "I was listening to…", "On [show]…", "this reminded me of…" → record
  the inspiration source on the artifact.

---

## Phase 2 — Set loose (bulk mine)

With the converged rules, process the remaining targets **autonomously** in larger batches: segment →
dedup → classify → Template → log progress (items processed, files created, duplicates skipped). Validate
created files (`validate_template.py`) and run the `verify-second-brain` check as you go — recommended.
**Spot-check** a batch periodically; if the agent drifts on a new kind of content, drop back to one
calibration batch, fold the fix into the rules, and resume. Convergence is not permanent — a new source
shape can need a retune.

---

## When to use

- **Seeding a new brain** from a large export — the first big import.
- **Adding a new source type** later — calibrate its quirks on a batch before bulk-running it.
- **When bulk output quality drops** — a short re-calibration retunes the rules.

## Run it

Say **"mine my [source]"**, "calibrate the mining", or "idea mining" → the `/mine` skill runs
Triage → Calibrate → Set loose. For in-session pasted or dictated thoughts (not a bulk export), use
`/ingest-brain-dump`.
