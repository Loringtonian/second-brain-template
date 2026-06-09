---
name: golden-evolver
description: >-
  Evolve the golden few-shot examples your brain's processes use. The owner names a
  task + a recipe; the skill runs the evolution cycle (present outputs, collect the
  owner's scores, track versions, propose mutations) and saves a versioned golden set
  the other skills read at prompt-build time.
  Tasks: classification (taxonomy routing, used by /ingest-brain-dump + /mine),
  summarization (Template A/B summaries, used by /process-content), keyword_extraction
  (used by /process-content), template_creation (full Template A from raw input),
  segmentation (idea-boundary detection in long text), and delegation (orchestrator →
  sub-agent prompts; see Orientation_Docs/SUBAGENT_DELEGATION_PRIOR_ART.md).
  Recipes: Quick Curation (hand-pick 5), Bootstrap (generate 20, filter to top 5),
  Deep Evolution (meta-prompt iteration), Escape Local Maximum (aggressive mutation +
  wildcards), Hybrid (bootstrap then evolve).
  Invoke: "/golden-evolver", "/golden-evolver classification", "evolve examples for
  keyword extraction", "quick curation for summarization", "escape local max on segmentation".
required_context_files:
  - Orientation_Docs/CONTENT_TAXONOMY.md
user_invocable: true
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
---

# Golden Few-Shot Evolver

Evolve the golden few-shot examples your brain's processes use. Better examples make every downstream
run better — and they're cheap to improve once you have a loop. The owner names a task and a recipe; you
manage the cycle: present outputs, collect scores, track versions, propose mutations.

## Storage (self-contained — no external project needed)

```
.claude/golden_sets/[task]/active.json          # current golden set (the one skills read)
.claude/golden_sets/[task]/v001_[hash].json     # versioned sets
.claude/golden_sets/[task]/score_history.jsonl  # one line per scored generation
```

Create `.claude/golden_sets/` on first use. It's local working state — add it to `.gitignore` if you
don't want golden sets in version control.

## Invocation
- `/golden-evolver` — interactive (ask which task)
- `/golden-evolver classification` — target a task
- `/golden-evolver bootstrap summarization` — recipe + task
- "evolve examples for keyword extraction" / "quick curation for classification" / "escape local max on segmentation"

## Step 1 — Identify the task

| Task | What it does | Where the examples are used |
|---|---|---|
| **classification** | Categorize content by taxonomy | `/ingest-brain-dump`, `/mine` |
| **summarization** | Generate Template A/B summaries | `/process-content` |
| **keyword_extraction** | Pull keywords from content | `/process-content` |
| **template_creation** | Build a full Template A from raw input | `/process-content` |
| **segmentation** | Detect idea boundaries in long text | any long-text split |
| **delegation** | Write orchestrator → sub-agent prompts | every Task/Agent dispatch (see `Orientation_Docs/SUBAGENT_DELEGATION_PRIOR_ART.md`) |

If the owner doesn't specify, list the tasks and ask.

## Step 2 — Load current state

`ls .claude/golden_sets/[task]/`. If `active.json` exists, read it + `score_history.jsonl`. If not, this
is first-time setup — default to **Quick Curation**.

## Step 3 — Pick a recipe

- "quick curation" / "let me pick" → **Quick Curation**
- "bootstrap" / "generate and filter" → **Bootstrap**
- "deep evolution" / "evolve" / "iterate" → **Deep Evolution** (meta-prompt)
- "escape local max" / "shake it up" → **Escape Local Maximum**
- "hybrid" → **Hybrid** (bootstrap then evolve)

No recipe given? Recommend by state: no set → Quick Curation; <5 scored generations → Bootstrap; 5+ → Deep Evolution.

## Step 4 — Execute

**Quick Curation** — find 5 real inputs (grep your brain for relevant content) → run the task on each →
present all 5 outputs → owner approves/rejects each → save the approved ones as `v001_[hash].json` +
point `active.json` at it.

**Bootstrap** — find 20 real inputs → run the task on all (parallel cheap-model agents are fine) →
present in batches of 5 → owner scores approve/reject → keep the top ~5 → save versioned + log all scores.

**Deep Evolution** — read `active.json` + `score_history.jsonl` → build a meta-prompt ("here are past sets
and their scores; the current best scored X; propose 3 candidates that might score higher; include one
wildcard to escape local maxima") → run the task on a test input with each candidate → present all 3 +
the current best → owner ranks/scores → log scores, update `active.json` if a candidate wins → repeat
until "good enough."

**Escape Local Maximum** — Deep Evolution with aggressive mutation, ~50% wildcard injection, crossover
between top sets enabled.

**Hybrid** — Bootstrap to seed, then Deep Evolution to refine.

## Step 5 — Save & report

```
Golden Evolver — [Task]
  Recipe: [...]   Version: v[N]_[hash]   Examples: [count]   Generations scored: [count]
  Best score this session: [score]
  Active set: .claude/golden_sets/[task]/active.json
  Iterate: "deep evolve [task]"
```

## Step 6 — Integration

Other skills read `.claude/golden_sets/[task]/active.json` at prompt-build time and include those
examples in the prompt; if it doesn't exist, they fall back to zero-shot. (The shipped skills work
zero-shot today — golden sets are a quality upgrade you grow, not a dependency.)

## Schemas

`score_history.jsonl` line: `{"task","version","input_hash","score","score_type":"1-5","timestamp","notes"}`

`v[N]_[hash].json`: `{"task","version","hash","created","parent_version","strategy","examples":[{"input","output","source"}],"avg_score","generations_tested"}`
