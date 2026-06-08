---
name: viz
description: Tufte-style visualization critique/design skill. Use when user says "/viz", asks to design or improve charts, dashboards, data tables, comparison views, scorecards, cockpit UIs, analytical HTML artifacts, trading/analytics dashboards, idea-ranking cockpits, feed-curation tasklists, or review-queue views. Applies data-ink ratio, chartjunk removal, graphical integrity, small multiples, sparklines, layering, provenance, and high-density/low-slop defaults.
allowed-tools: Read, Edit, Write, Bash
---

# Viz — Tufte-Style Analytical Visualization

## Overview

Use this skill to design or critique visual displays where the point is to understand evidence, compare alternatives, reveal signal, or make a cockpit/dashboard easier to reason with. It adapts Edward Tufte's visualization principles — graphical integrity, data-ink ratio, chartjunk removal, small multiples, sparklines, layering/separation, and high-density analytical design — to Second Brain artifacts and vibe-coded tools.

The stance: pretty is subordinate to truthful, dense, useful, comparison-rich. A chart or dashboard should help the owner decide what is good, what changed, what matters, and what to do next.

## When to Invoke

Invoke when:

- User says `/viz`.
- User asks to design, improve, critique, or clean up a visualization.
- User asks for a dashboard/cockpit/table/scorecard/HTML artifact that carries data or comparisons.
- User asks why a chart feels misleading, noisy, thin, hard to scan, or “startup-dashboard bullshit.”

Use for:

- Trading / analytics dashboards: alpha/returns, replay comparisons, source weights, sectors, model-classification changes, portfolio/risk views.
- Signal / bookmark / feed dashboards: tasklists, trend scans, source quality, recurring topic clusters.
- Idea-ranking / curation cockpits: taste-based comparison views, ranked candidates, review queues, decision surfaces.
- Story or content review tools: A/B comparisons, human-review queues, scorecards, benchmark views.
- HTML artifacts, reports, charts, data tables, diagrams, sparklines, or any visual analytical display.
- Critiquing existing visuals for misleading scales, decorative slop, insufficient comparison, or poor information density.

Do not use for pure brand/aesthetic pages with no analytical content; use design/style skills instead.

## Core Principles

1. **Show comparisons.** Every display should answer: compared to what?
2. **Show causality, mechanism, or structure where possible.** Move beyond “number went up.” Show why, drivers, dependencies, or uncertainty.
3. **Respect graphical integrity.** No fake magnitude. Baselines, intervals, area/volume encodings, and axes must match the data.
4. **Maximize data-ink within reason.** Remove ornament, heavy grids, redundant labels, and startup-dashboard decoration that does not carry information.
5. **Prefer dense, readable displays over sparse bullshit.** High information density is good when hierarchy/layering is clear.
6. **Integrate words, numbers, and images.** Put labels and explanations near the data they explain.
7. **Expose provenance.** Analytical displays should state data source, time window, filters, and caveats.
8. **Preserve decision context.** Show enough surrounding data to prevent overreacting to a single metric.

## Workflow for New Visualizations

### 1. Clarify the data story

Ask or infer:

- What decision does this support?
- What comparisons matter?
- Who is the viewer?
- What is the time window?
- What is the failure mode if the display misleads?

### 2. Choose the display form

- Time-series → line chart, sparkline stack, or annotated timeline.
- Many comparable entities → sorted table with sparklines / compact bars.
- Before/after or A/B → paired columns, slopegraph, small multiples, or delta table.
- Distribution → histogram, beeswarm, box/violin only if the audience benefits.
- Part-to-whole → usually avoid pie charts; prefer sorted bars or table with percentages.
- Multivariate signals → small multiples, faceting, layered table, or compact scorecard.
- Ranked review queue → sortable table with the few highest-signal fields, plus reason/evidence column.

### 3. Design with data-ink discipline

- Start minimal.
- Add only elements that carry data, comparison, hierarchy, provenance, or actionability.
- Use color sparingly for semantic states: positive/negative, selected/highlighted, stale/warning.
- Prefer subdued grids, direct labels, and compact legends.
- Default to tables when exact values and comparison both matter.

### 4. Add context and caveats

Always include when relevant:

- Source
- Date/time window
- Filtering rules
- Missing data caveats
- Whether values are raw, normalized, model-generated, or manually reviewed

## Workflow for Critique

1. **Graphical integrity**
   - Are scales truthful?
   - Are baselines appropriate?
   - Are intervals consistent?
   - Is area/volume encoding lying?
   - If proportions look suspicious, calculate/estimate lie factor.

2. **Comparison quality**
   - Does it answer “compared to what?”
   - Are deltas visible?
   - Are cohorts/time windows comparable?
   - Is ranking meaningful?

3. **Data-ink / chartjunk**
   - What can be erased without losing information?
   - Are decorative gradients, shadows, cards, icons, or 3D effects obscuring the signal?
   - Are labels redundant or too far from the data?

4. **Density and hierarchy**
   - Is the display too sparse for the question?
   - Is it dense but illegible?
   - Can small multiples, sparklines, or grouped tables improve scanability?

5. **Actionability**
   - Does it make the next action obvious?
   - If it is a cockpit, does the top of the page show what changed, what matters, and what needs review?

## Owner-Specific Defaults

<!-- __FILL_FROM_USER__:viz_defaults
     Replace the examples below with your own domain-specific display guidelines.
     E.g. your primary dashboards, messaging platforms, or UI contexts. -->

- **Analytics dashboards:** Prefer deterministic comparisons and replay deltas over vibes. Show before/after prompt/config changes, alpha/returns, source/sector effects, and relevant exclusions.
- **Second Brain / idea-ranking cockpits:** Preserve exact titles/keywords; show why an item surfaced. Provenance beats polish.
- **Messaging / mobile output:** Many messaging platforms have no real table syntax. Use bullets, labeled key/value rows, or compact lists. Do not emit pipe tables unless the target is a markdown file.
- **HTML artifacts:** Dense dark-mode cockpits are fine, but visual hierarchy must be earned. Use subdued chrome; make the data primary.
- **Review queues:** Put “why this matters” and “next action” near the item, not hidden below the fold.

## Quick Checklist

Before finalizing a visualization or critique, verify:

- [ ] The main comparison is obvious.
- [ ] Data source, time window, and caveats are visible.
- [ ] No misleading baseline, scale, area, or interval choices.
- [ ] Non-data decoration has been removed or justified.
- [ ] Labels sit near the data they explain.
- [ ] Color has semantic meaning and is not just decoration.
- [ ] Dense views remain scannable through grouping, sorting, layering, or small multiples.
- [ ] The viewer can tell what changed and what action/review is needed.

## References

- `references/tufte-principles.md` — core principles from *The Visual Display of Quantitative Information*: lie factor, data-ink, chartjunk, small multiples, integrity.
- `references/analytical-design.md` — material from *Envisioning Information*, *Visual Explanations*, and *Beautiful Evidence*: analytical design, sparklines, layering & separation, micro/macro, range-frames, causality, confections.

## Common Pitfalls

1. **Making it pretty instead of useful.** Aesthetic polish is secondary to evidence, comparison, and actionability.
2. **Under-dense dashboards.** Four giant cards can be worse than one compact table when the owner needs to scan many candidates.
3. **No comparison baseline.** A metric without history/cohort/benchmark often becomes decorative numerology.
4. **Hiding provenance.** If the viewer cannot tell where the data came from and when it was captured, trust collapses.
5. **Messaging-platform tables.** Pipe tables degrade in many messaging contexts. Use bullets/key-values unless writing to a file.
6. **Color abuse.** Color should encode meaning, not serve as startup confetti.
7. **Over-reducing multivariate decisions to one score.** Scores can rank, but include the reason/evidence fields that let the owner apply taste.
