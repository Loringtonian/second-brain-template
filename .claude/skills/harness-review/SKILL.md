---
name: harness-review
description: >-
  Weekly self-improvement of the HARNESS itself — not project QA. Reviews the last N days
  of this brain's Claude Code session traces for harness-level friction (where the owner
  corrected the agent, repeated permission prompts, skills that misfired or weren't used,
  rules/memories the agent ignored, weak sub-agent prompts), drafts a proposal of findings,
  and the owner reviews + applies it finding-by-finding (gated — nothing auto-applies).
  Uses the in-session Workflow tool to fan out over trace chunks; no external services, no
  API keys. Use when the owner says "/harness-review", "review the harness", "self-review",
  "what's the agent getting wrong", or accepts the optional offer at the end of /weekly-maintenance.
allowed-tools: Read, Edit, Write, Bash, Glob, Grep, Agent, AskUserQuestion
---

# Harness Review (lean self-improvement loop)

This improves **how the agent behaves** — the rules, skills, memories, and prompts — by reading what
actually happened in recent sessions and proposing fixes. It is recursive self-improvement of the
harness, distinct from `/weekly-maintenance` (which keeps your *content* tidy).

## Hard boundary — propose, never auto-apply

This skill **produces a proposal and nothing else**, then walks the owner through it. No memory,
`CLAUDE.md`, skill, or hook is edited without the owner's explicit per-finding "yes." The improvement
signal is the owner saying "apply that" — not a number going up. Show the diff before every edit.

## Process

### 1 — Window + find the traces
- Default window: last **7 days** (ask if the owner wants a different lookback).
- Claude Code stores per-session traces as JSONL at `~/.claude/projects/<project-slug>/*.jsonl`, where
  `<project-slug>` is this repo's absolute path with `/` and `.` replaced by `-`. Find them:
  ```bash
  SLUG=$(pwd | sed 's#[/.]#-#g'); ls -t ~/.claude/projects/$SLUG/*.jsonl 2>/dev/null
  ```
- **Exclude the live session** (the newest file, which is this run) so the corpus isn't self-contaminated.
- If the traces are large, chunk them by file or by byte budget so each observer reads a coherent slice.

### 2 — Observe (fan out with the Workflow tool)
Dispatch parallel observers over the trace chunks via the **Workflow** tool's `agent()` (in-session,
subscription-authed — no API key). Each observer is descriptive: surface concrete *moments* of
harness friction with evidence, not judgments. Brief each with the 10-slot skeleton
(`Orientation_Docs/SUBAGENT_DELEGATION_PRIOR_ART.md`); have each return findings as structured data:
- the **pattern** (e.g. "the owner re-corrected the agent's folder choice 3×", "permission prompt for
  the same command 5×", "a skill that should have fired didn't", "a memory rule that was ignored"),
- the **evidence** (which session + a short quote/line ref),
- the **intent it conflicts with** (a specific `CLAUDE.md` line / `MEMORY.md` rule / skill / an
  `INTENT_SPEC.md` Owner Intent item — purpose, gaps, success criteria, non-goals, comms style).
  Hand each observer the Owner Intent section in its prompt so "what the owner wants" is checkable,
  not guessed.

### 3 — Synthesize the proposal
Before synthesizing, read `INTENT_SPEC.md` (the Owner Intent section) and check each candidate
finding against it: a proposal that optimizes the agent's behavior *away* from the owner's stated
purpose, comms style, or non-goals is itself harness friction — drop or invert it.
Aggregate the observers' findings, dedup, and write one proposal:
`Orientation_Docs/harness_review/PROPOSAL_<date>.md`. Each finding carries: pattern · evidence ·
conflicting intent · a concrete proposed change (file + the edit). Order by how often the friction recurred.

### 4 — Review + apply (gated)
Walk the findings one at a time. For each: render it, show the proposed change as a concrete diff
sketch (read the current block first; verify the target path exists), and ask **apply / reject /
modify / skip**. Execute only on "apply" (or "modify" → re-present → apply). Show the resulting diff.
This is the only step that mutates anything.

### 5 — Close out
Move the proposal to `Orientation_Docs/harness_review/reviewed/`, append a one-line summary to a
`REVIEW_HISTORY.md` there (applied / rejected / modified / skipped counts), and report what changed.

## Hard rules
- **Produce a proposal; apply nothing without a per-finding yes.** No "approve all."
- **Show the diff before every edit.** No silent Writes.
- **Absolute paths** when handing trace slices to observers (sub-agents confuse cwd).
- **Subscription only** — fan out via the Workflow tool's `agent()`, never a raw API key.
- **Stay lean** — this skill needs no bespoke pipeline; the Workflow tool does the fan-out. (A heavier
  version could add condensing/validation scripts, but that's optional, not required to run.)

## When to run
- On demand (`/harness-review`), or
- As the **optional final step of `/weekly-maintenance`** — after the content sweep, the owner is asked
  whether to also run a harness self-review.
