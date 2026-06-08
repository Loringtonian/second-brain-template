---
name: delegate-check
description: >-
  Lint a draft sub-agent prompt against the 10-slot skeleton before dispatching
  via Task/Agent tool. Catches the high-frequency failure modes: negative framing,
  numbered algorithms, pre-warned failure modes, step budgets, character-sheet
  roles, missing schema pin, relative paths, negative examples. Returns a scored
  audit (PASS / FLAGS) and a revised draft that addresses every flag.
  Full rationale: your delegation prior-art doc.
  Invocation: `/delegate-check`, "lint this sub-agent prompt", "audit this Task
  prompt", "check this delegation", or automatic pre-flight before any Agent()
  dispatch when the orchestrator has time to iterate.
user_invocable: true
allowed_tools:
  - Read
  - Write
  - Edit
  - Grep
required_context_files:
  - __FILL_FROM_USER__:delegation_rationale_doc
---

# Delegate-Check — Sub-Agent Prompt Linter

Lints a draft sub-agent prompt against the 10-slot skeleton + positive-framing rules before the orchestrator dispatches it. This is the pre-flight check between "I'm about to call Agent()" and the actual call.

## Step 0 — Silent Context Load

Silently `Read` your delegation prior-art doc (`__FILL_FROM_USER__:delegation_rationale_doc`) if not already in context. Do not announce.

## Input

The orchestrator hands you a draft prompt. That's it. No extra ceremony — the whole point is to be fast enough that running it every dispatch is cheap.

## The 10 Slots (reference)

```
 1. <purpose>      PURPOSE & CONTEXT
 2. <role>         ROLE (optional, one sentence)
 3. <return>       RETURN FORMAT (top)
 4. <approach>     GENERAL APPROACH
 5. <examples>     WORKED EXAMPLES (positive only)
 6. <constraints>  CONSTRAINTS (positive framing)
 7. <verify>       VERIFICATION CHECKLIST
 8. <done>         DEFINITION OF DONE
 9. <return>       OUTPUT CONTRACT (bottom)
10. <context>      LIVE CONTEXT (absolute paths)
```

## Lint Checks

Run every check below against the draft. Report any that trigger as `FLAG`; the rest as `OK`.

### Framing (highest priority — priming-sensitive)

- **F1: Negative without reason.** Grep for `don't`, `do not`, `never`, `avoid`, `must not`, `cannot`. For each hit, verify a *reason* is attached (e.g., *"because X", "so that Y", "to prevent Z"*). If reason is missing → FLAG. Fix: either remove the prohibition or reframe positively, or add the reason.
- **F2: Pre-warned failure modes.** Grep for conditional failure patterns: `if you hit`, `if you encounter`, `if X fails`, `in case of error`. These prime the failure. FLAG. Fix: convert to forward-facing verification checklist entries (*"Before returning, confirm the output parses as JSON"*).
- **F3: Negative example demonstrations.** Check for "bad example" / "wrong output" / "do not produce" blocks. FLAG. Fix: remove, keep only positive examples.

### Structure (skeleton compliance)

- **S1: Purpose slot missing.** No `<purpose>` or equivalent opening context paragraph. FLAG. Fix: add why-this-matters + what-feeds-downstream.
- **S2: Output schema not pinned at top.** No concrete return-format spec in the first third of the prompt. FLAG. Fix: add `<return>` block near the top.
- **S3: Output schema not pinned at bottom.** No re-pin at the end. FLAG. Fix: add `<return>` block at the end (format-drift insurance).
- **S4: Numbered algorithm for a non-rigid task.** Count numbered steps. If >3 and the task is reasoning-heavy (not a rigid procedure), FLAG. Fix: collapse to a general-approach paragraph. Keep numbered steps only when the procedure is genuinely stage-gated and rigid.
- **S5: Missing verification checklist.** No forward-looking *"before returning, confirm X"* block. FLAG. Fix: add `<verify>` with 2–5 checklist items.
- **S6: Missing definition of done.** No clear statement of what a complete answer looks like. FLAG. Fix: add `<done>` block.

### Hygiene

- **H1: Role longer than one sentence.** Multi-sentence persona / character sheet. FLAG. Fix: collapse to one sentence or remove.
- **H2: Step/token budget clause.** Grep for `you have N steps`, `budget`, `up to N`, `maximum of`, `N attempts`. FLAG. Fix: remove. Budget is not a constraint; scope is.
- **H3: Explicit termination clause.** Phrases like `stop when`, `terminate if`, `quit after`. FLAG. Fix: remove. Use definition-of-done instead.
- **H4: Relative paths.** Grep for paths not starting with `/` and not absolute. FLAG. Fix: convert to absolute.
- **H5: Missing XML tag wrapping.** Each of the 10 slots should be wrapped in a semantic tag. Un-tagged prose slots → soft-FLAG (style-only, not blocking).

### Content quality

- **C1: Example count.** Zero examples on a non-trivial task → FLAG. 4+ examples → soft-FLAG (Anthropic suggests 3–5 max; 1–3 usually enough).
- **C2: Purpose-degradation risk.** Check if the sub-agent would understand the broader goal from the prompt alone, not just the immediate action. If not → FLAG. Fix: expand `<purpose>`.

## Output

Return a compact audit followed by the revised draft:

```
## Delegate-Check Audit

**Score:** X/Y checks passed (Z FLAGS)

### Flags

- **F1 (negative without reason):** "...don't truncate..." — no reason attached.
  Fix: remove OR reframe as "Return the full content." OR add reason.
- **S3 (schema not re-pinned):** Output format declared at top but not at bottom.
  Fix: add closing <return> block.
  [...]

### Revised Draft

<purpose>
...
</purpose>

<role>
...
</role>

[... full revised 10-slot prompt ...]
```

If the draft passes all blocking checks, return:

```
## Delegate-Check Audit

**Score:** PASS

Draft is skeleton-compliant. Dispatching.
```

## Anti-Patterns (do not do these when linting)

- **Don't rewrite for style.** Lint against skeleton + framing rules only. If the orchestrator's voice is terse or warm, leave it. You're a linter, not a stylist.
- **Don't add content the orchestrator didn't provide.** If `<examples>` is missing but no source examples are available, FLAG but don't fabricate.
- **Don't block trivial dispatches.** If the sub-agent task is a one-line factual lookup ("fetch file X, report line count"), most slots are overkill. Use judgment: soft-FLAG the missing slots, note "trivial task," PASS.
- **Don't lint post-hoc.** This is a *pre*-dispatch check. If the orchestrator has already dispatched, the value is gone — just note the lessons for next time.

## When to invoke automatically

The orchestrator should invoke `/delegate-check` before any Task/Agent dispatch where:

- The sub-agent task is non-trivial (≥1 paragraph of work)
- The sub-agent is fanning out (parallel agents with similar prompts — fix one, fix all)
- The orchestrator is about to spend real tokens on a high-stakes sub-agent call

For trivial one-line sub-agent dispatches (e.g., "fetch file X"), skip the check — the fixed cost exceeds the benefit.
