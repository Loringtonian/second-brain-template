---
name: remove-watermark
description: Remove a visible watermark from an image with local OpenCV inpainting (no Docker, no hosted model, sub-second), self-calibrating across aspect ratios via a Sonnet vision locate + before/after QA loop. Built for the Gemini bottom-right sparkle but works on any visible mark. Use when the user says "remove watermark", "dewatermark", "remove the gemini watermark", "clean watermark", or points at a watermarked image / folder. Does NOT touch invisible SynthID provenance marks.
user_invocable: true
allowed_tools:
  - Bash
  - Read
  - Agent
---

# remove-watermark

Erase a **visible** watermark (the Gemini "✦" sparkle, or any logo on an image the user
owns) using a fast local pipeline. The pixel work is deterministic OpenCV inpainting; a
Sonnet subagent does the parts that need eyes — finding the mark (which moves around in
normalized space as aspect ratio changes) and confirming it's gone.

**Scope:** only the visible brand mark on the user's own image. Never the invisible SynthID
provenance watermark — different purpose, out of scope.

## Engine

`scripts/remove_watermark.py` — local, no API keys. Deps: `pip install opencv-python pillow numpy`
(optional `simple-lama-inpainting` for the `--lama` tier). Key flags (full list in the file header):

```
python3 scripts/remove_watermark.py <image | dir | glob> \
    --region-frac CX,CY,W,H   # watermark center+size as fractions (from vision-locate)
    --min-frac 0.11           # floor on box edge (fraction of min(W,H)); GROW this on a miss
    --inflate 1.5             # scales the located box around its center
    --shape box               # box (robust coverage) | diamond (tighter, less edge-bleed)
    --method telea            # telea | ns  (cv2);  or  --lama  for the high-quality tier
    --json                    # machine-readable summary (clean path, crops, region used)
```

It writes `<stem>_clean.png` next to the source (**never overwrites the original**) and emits
`wm_before.png` / `wm_after.png` crops to `/tmp/dewatermark/<stem>/` for the QA view. It always
inpaints from the pristine original, so retries never stack smears.

## Per-image loop (max 3 attempts)

Run this for each image. Each attempt re-runs the engine **on the original**.

### 1. Locate — Sonnet subagent (`Agent`, `model: sonnet` — subscription, no API key)

```
<purpose>You are locating a watermark in ONE image so a tool can inpaint the box you return. A wrong box smears clean art and leaves the mark.</purpose>
<return>Return ONLY JSON: {"found": true, "bbox_frac": [cx, cy, w, h], "on_edge": true|false, "notes": "<short>"}
cx,cy = CENTER as fractions of image width/height (0–1, origin top-left); w,h = size fractions.
on_edge = true if the mark sits on / straddles a HIGH-CONTRAST boundary (a dark object meeting a light wall/tile, two very different colours/textures), where simple inpainting would smear one side over the other.
If absent: {"found": false, "bbox_frac": null, "on_edge": false, "notes": "..."}.</return>
<approach>Read the image at <PATH>. Find the small, faint, SEMI-TRANSPARENT watermark on top of the art — usually a diamond / 4-pointed-star sparkle near a corner (Gemini's is bottom-right), but it can be a small logo anywhere along an edge. Return a box snug around it plus a little margin; prefer slightly generous over clipping. Then judge on_edge: does the box span a sharp dark↔light or object↔background boundary?</approach>
<constraints>Coordinates normalized 0–1, origin top-left. Order [cx,cy,w,h]. A sparkle is ~3–9% of the image. Output JSON only.</constraints>
<verify>cx,cy is the CENTER; all four in 0–1; box covers the whole mark; on_edge reflects whether the box straddles a high-contrast boundary.</verify>
<context>image path = <PATH> ; dimensions = <W>x<H> (<aspect note>).</context>
```

Note: this locate is **approximate** — a faint mark on a downscaled read can bias the estimate
toward the corner by ~0.05–0.08. That's expected; the box floor + growth (below) absorbs it.

> **Edge case (this is the #1 failure mode).** If the locate returns `on_edge: true`, run step 2
> **with `--lama --shape diamond` from the first attempt** — do NOT use the cv2 default. cv2's
> telea/ns inpaint fills by diffusing neighbouring pixels, so across a sharp dark↔light boundary it
> bleeds one side's colour into the other and leaves a visible smear (e.g. the dark door colour
> smudged onto white tile). LaMa reconstructs the boundary instead; a diamond mask also covers less
> area than a box, so it smears less.

### 2. Inpaint

`python3 scripts/remove_watermark.py "<PATH>" --region-frac CX,CY,W,H --min-frac <floor> --json`
First attempt: `--min-frac 0.11` — **add `--lama --shape diamond` if the locate flagged `on_edge`.**
Parse the JSON for `clean`, `before_crop`, `after_crop`.

### 3. QA — Sonnet subagent, **two views for two jobs**

Give it BOTH the full cleaned image (catches a mark the tight crop would miss) and the
before/after crop pair (judges smear):

```
<purpose>Confirm an automated watermark removal actually worked, so a retry can fire if not.</purpose>
<return>Return ONLY JSON: {"still_present": bool, "relocate_frac": [cx,cy,w,h] | null, "artifact": "none|mild|bad"}
relocate_frac = where the mark still is (normalized center+size on the FULL image) if still_present, else null.</return>
<approach>Read the full cleaned image at <CLEAN> and decide: is ANY visible watermark/sparkle still present anywhere? Compare the before crop <BEFORE> and after crop <AFTER>: in BEFORE the mark is visible — is it absent in AFTER, and is the patched area clean or an obvious smudge/smear? Judge removal from the full image (a mark can survive just outside the crop); judge smear from the crops.</approach>
<constraints>still_present reflects the FULL image. artifact: none = invisible, mild = faint smudge, bad = obvious blur/smear **OR one region's colour bled across an edge into another (e.g. dark door colour smeared onto white tile, a dark halo on a light wall)**. When the patch sits on a boundary and you're unsure, call it bad. Output JSON only.</constraints>
<verify>You checked the whole image for a surviving mark, not only the crop; relocate_frac is the mark's real position if it survived; artifact==bad if any colour bled across an edge.</verify>
<context>clean = <CLEAN> ; before = <BEFORE> ; after = <AFTER> ; dims = <W>x<H>.</context>
```

### 4. Decide
- `still_present == false` and `artifact` in {none, mild} → **done**. Report the `_clean` path.
- `still_present == true` → retry, **growing the box**: min-frac ladder `0.11 → 0.18 → 0.26`.
  If `relocate_frac` looks confident, recenter on it; otherwise keep the locate center and just grow.
  (Growth monotonically guarantees coverage even when the locate stays biased.)
- `still_present == false` but `artifact == bad` (**this includes any cross-edge colour bleed**) →
  the mark sat on a busy or high-contrast-edge background. Re-run that image with `--lama`
  (one-time `pip install simple-lama-inpainting`, local, ~2–5s, no Docker) for a clean
  reconstruction, **then re-QA**. (Best avoided up front: when the locate flags `on_edge` you've
  already gone straight to `--lama`, so this branch is the safety net.)
- After 3 attempts still present → report the best result and offer `--lama` or a manual
  `--region X,Y,W,H` from the user.

## Batch (folder / glob)

The engine accepts a directory or glob and skips its own `_clean` outputs. Before a batch run,
**state the image count and that it will fire ~N locate + ~N QA Sonnet calls (plus retries) and
confirm** — Sonnet vision is subscription spend, fine for a small priority batch, not an unbounded
folder. Then fan out the per-image loops in parallel and print a summary table:
`file → removed? → artifact → final path`.

## Validated behavior

Tested across aspect ratios (1024² through tall 1536×2728). Vision-locate self-calibrates the
corner sparkle across all of them; most images clear at `--min-frac 0.11`. When a mark sits
unusually inward, attempt 1 can survive — the QA subagent catches it on the full image and returns
an accurate `relocate_frac`, and attempt 2 (`--min-frac 0.18`, recentered) clears it. **Marks on a
high-contrast edge (a logo straddling a dark object and a light wall) smear under cv2 and must use
`--lama`** — the locate's `on_edge` flag routes them there from the start. Originals untouched,
RGBA preserved.

## Hard rules
- Original is read-only; output is always a new `_clean` file.
- Vision goes through `Agent` subagents (`model: sonnet`), never an Anthropic API key.
- Visible mark only — never target invisible SynthID.
- A watermark on a high-contrast boundary → `--lama`, never the cv2 default (it bleeds across the edge).
