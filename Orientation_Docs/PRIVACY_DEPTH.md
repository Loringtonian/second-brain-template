<!-- __FILL_FROM_USER__:privacy_depth
     FOR THE AGENT READING THIS — this is INFRASTRUCTURE (a mechanism), not blank scaffold.
     The rubric below is a GENERIC default. Your job when a human adopts this repo: run the
     calibration loop in the "Define your levels" section — interview them against their own
     real files until the D1–D5 boundaries match THEIR sense of private, then record their
     rulings at __FILL_FROM_USER__:depth_calibration. The /setup skill drives this. Until
     calibrated, treat the generic rubric as a safe-conservative default (when unsure, round UP). -->

# Privacy Depth — Progressive Context Exposure

> A per-file **privacy/disclosure depth** (1–5) on every file. `1 = least private, 5 = most private`.
> It is the safety foundation for sharing a brain with agents — and the basis for *which* parts of
> this brain you publish. It's the same idea behind publishing a shareable template of a brain:
> ship the low-depth architecture, keep the high-depth interiority private.

## The model — depth is *resolution of disclosure*

Depth is **not** a flat sensitivity label. It is **how high-resolution a disclosure is.** The *same*
underlying thing can be disclosed at every level — e.g. a past work trip:
`"was in country X in 2017"` (D2) → `"doing fieldwork on a project there"` (D3) → `"what they concluded"`
(D4) → `"their private grief about how it ended"` (D5).

**Two drivers, both push depth UP:** (1) **privacy / intimacy** — personal life, health, relationships;
(2) **strategic value** — a "winner" idea is *more* protected, not less.

**Register decides, not topic.** The same topic lands at different depths by *how it's held*: "debt as
proud planning" is shareable-with-an-intimate (D4); "debt as shame" is sealed interiority (D5).

## The rubric (generic default — calibrate to yourself)

| `depth` | Name | What it is | Exposure rule |
|---------|------|-----------|---------------|
| **1** | Public footprint | Already-public facts about you (things you've shared publicly). | Always shareable. |
| **2** | Interests & existence | *Generalized*: that you're interested in X, that a project exists. | Shareable on autonomous agent passes. |
| **3** | Your work | Your actual content/thinking; credentials you'd share with a teammate. | **You-in-the-loop** to share. |
| **4** | Valuable & confidential | Spicy conclusions; "winner" IP; health, finance, family. | **Never without your express, explicit authorization.** |
| **5** | Sealed | Rawest interiority + top secrets; named intimates; NDA material. | **Never without explicit auth; quarantined.** |

## Unit of classification — section-aware, floor rounds UP

A file's `depth:` frontmatter is the **floor** = the depth of the **deepest content in it**, and it
**rounds UP**. The floor is the hard guarantee: a file is never exposed below it. Templated files
(A/B/C) can be reasoned about per-section (e.g. a quote is D2 but your relevance note is D4 → file = D4).

## How depth gates three things

1. **Context loading (progressive exposure)** — `ROUTER.md` loads deep/private docs only when the task
   warrants and you're in the loop; routine passes see only low-depth material. Attention isn't free.
2. **Publishing / sharing** — the rule of thumb for any public or shared copy: **publish depth ≤ 2,
   review depth 3 case-by-case, exclude depth 4–5.** (This is exactly how you produce a shareable,
   publishable copy of a brain.)
3. **Agent-to-agent (the end goal)** — when two people's brain-agents meet (e.g. cofounder/collaborator
   matching), they can disclose progressively: trade D2 interests first, go deeper only with consent.

`.gitignore` should keep the depth manifest and any D4–D5 content out of git until you choose otherwise.

## Stamping the depth

Stamp lives in **YAML frontmatter, one key**: `depth: N` at the top of the file (merged into an existing
frontmatter block if there is one). Keep only the floor in the file; richer per-section detail belongs in
a manifest you keep locally. `scripts/stamp_depth.py <file> <N>` sets it idempotently.

```yaml
---
depth: 3
---
# My note title
…
```

## Deterministic seed rules (safe, no-LLM, conservative round-UP)

Use these to seed before a judgment pass; everything else goes to a careful read.
- Raw external content (others' clips, transcripts) → **D2**.
- Your enriched commentary on external content → **D3** floor.
- Unpublished creative work → **D3**.
- NDA / sealed folders → **D5**.
- **D1 is never rule-assigned** (a false-low is the dangerous error) — only via an explicit public marker.

## Define your levels (the calibration loop — what `/setup` runs)

The rubric **is the product** — calibrate it to *you*:
1. State your one-line **register test** (what makes something feel "too private to share").
2. Hand-rule ~6 of your own real files across D1–D5 — these become your **gold set** (ground truth).
3. Run an **AI-interview loop**: the agent proposes a depth for a file + its reasoning; you correct it;
   the boundary sharpens. Repeat until the agent matches you on fresh files.
4. Record your rulings + boundary notes here:

`__FILL_FROM_USER__:depth_calibration`
<!-- Your register test, your gold-set rulings (file → depth → why), and the D4↔D5 boundary in YOUR
     words. This is what makes auto-classification trustworthy. The /setup skill walks you through it. -->

---

*When unsure, round UP. A file over-classified is merely less convenient; a file under-classified can be
exposed when it never should have been.*
