---
name: code-cleanup
description: >-
  Eight-axis codebase cleanup sweep. Spawns 8 parallel general-purpose subagents,
  each owning one cleanup dimension (dedupe/DRY, type consolidation, unused code,
  circular deps, weak types, defensive try/catch, legacy/fallback code, AI slop).
  Each subagent researches, writes a critical assessment, and implements all
  high-confidence recommendations in its lane. A final verify+repair gate then
  re-runs the target's tests/typecheck against a pre-cleanup baseline and repairs
  or reverts any regression. Accepts an optional target path
  argument (defaults to current working directory).
  Use when user says "/code-cleanup", "code cleanup", "clean up the codebase",
  "run code cleanup", or names a specific repo and asks for the 8-agent sweep.
  Do NOT auto-fire on generic words like "cleanup" alone — this skill edits code
  across 8 dimensions in parallel and should be invoked deliberately.
  Prompt origin: shaw makes magic (public community share).
---

# Code Cleanup

Eight parallel subagents, each auditing and fixing one dimension of code hygiene. Prompt origin: **shaw makes magic** (public community share).

## Invocation

```
/code-cleanup                         # target = current working directory
/code-cleanup <absolute-path>         # target = given path
```

The resolved target path is passed verbatim to every subagent so all 8 scope their work to the same codebase.

## Meta-instruction (verbatim, from Shaw)

> I want each to do detailed research on their task, write a critical assessment of the current code and recommendations, and then implement all high confidence recommendations

Every subagent follows this structure:

1. **Research** — survey the target path, grep for patterns, read key files.
2. **Critical assessment** — write a short report of what's wrong and what to do.
3. **Implement** — apply only high-confidence recommendations; leave uncertain calls in the report for the user.

## Process

### Step 1 — Resolve target

- If an argument was passed, use it as the absolute target path.
- Otherwise, use the current working directory.
- Validate the path exists. Abort if not.

### Step 1.5 — Capture the verify baseline (the regression gate's reference)

Before any edits, capture how the target builds/tests TODAY, so post-cleanup regressions are distinguishable from pre-existing breakage:

1. Detect the target's verify command(s) in priority order: a `Makefile` test target, `package.json` scripts (`test`, `typecheck`, `lint`, `build`), `pytest` / `pyproject.toml` / `pytest.ini`, `cargo test`, `go test`, `tsc --noEmit`, etc. Prefer the cheapest sound check that actually exercises the code (typecheck/compile + unit tests).
2. Run it once on the untouched tree and record the BASELINE result verbatim (pass/fail counts, collection errors, compile errors). A repo can have pre-existing failures — those are the baseline, NOT regressions.
3. If the target has no runnable verify command at all, fall back to a compile/parse check of every source file (`python3 -m py_compile`, `tsc --noEmit`, `node --check`, etc.) and record that as the baseline.

Store the command(s) + baseline result for Step 4.5.

### Step 2 — Spawn 8 subagents in parallel

Launch all 8 in a **single message** using the `Task` tool with `subagent_type: "general-purpose"` — not Explore (read-only). Each subagent needs Edit/Write to implement its recommendations.

Each prompt follows the template (Shaw's brief text is inserted verbatim; the wrapper around it uses the 10-slot sub-agent delegation skeleton from `CLAUDE.md` > SUB-AGENT DELEGATION):

```
<purpose>
You are one of 8 parallel code-cleanup sub-agents. Each of the other 7 owns a different cleanup dimension and is running on the same target at the same time. Your report is merged with theirs into a single Code Cleanup Report the orchestrator hands to the user. The orchestrator trusts every HIGH-CONFIDENCE edit to be applied without further review, and every UNCERTAIN item to be genuinely ambiguous — miscalibration on either side corrupts the merge.
</purpose>

<role>
Focused code-hygiene auditor for one lane, working in parallel with seven peers.
</role>

<return>
Close your turn with a report in this structure:

## Lane: <brief name>

### Critical assessment
[One short paragraph: what is the state of this lane in the target? Which patterns recur? What is the overall health?]

### HIGH-CONFIDENCE (applied)
- [Absolute path]:[line or range] — [one-line change description]
- [...]

### UNCERTAIN (surfaced for review)
- [Absolute path]:[line or range] — [issue] — [why you did not apply it]
- [...]

### Tools run
- [knip | madge | tsc | mypy | ruff | ...] — [one-line output summary]
- [...]

### Files edited
- [Absolute path]
- [...]
</return>

<approach>
Shaw's lane brief, verbatim:

<INSERT ONE OF SHAW'S 8 BRIEFS VERBATIM>

Meta-instruction from Shaw (verbatim):
"I want each to do detailed research on their task, write a critical assessment of the current code and recommendations, and then implement all high confidence recommendations"

Work the lane in three stages: research first (grep, Read, run any language-appropriate tools), then write the critical assessment splitting every finding into HIGH-CONFIDENCE or UNCERTAIN, then apply only the HIGH-CONFIDENCE items via Edit/Write and leave UNCERTAIN for the orchestrator's aggregation.
</approach>

<examples>
<example>
Lane: Dedupe / DRY on a small tools directory.

### Critical assessment
Three utility functions (`cosineSim`, `phraseWindows`, `parseJsonResponse`) appear verbatim in 3–5 files each; one file also duplicates ~100 lines of prompt-building logic inline. Consolidating into a shared `lib/util.js` is low-risk and substantially reduces future edit surface.

### HIGH-CONFIDENCE (applied)
- /abs/tools/lib/util.js:1 — Created; exports `cosineSim`, `phraseWindows`, `parseJsonResponse`, `pmap`.
- /abs/tools/generate-tree.js:79-139 — Removed local `cosineSim` and `phraseWindows`; imported from `./lib/util.js`.
- /abs/tools/add-phrase-maps.js:23-76 — Same two removals; imported from util.
- /abs/tools/extract-concepts.js:143-166 — Removed local `parseJsonResponse`; imported. Call sites unchanged (same signature).

### UNCERTAIN (surfaced for review)
- /abs/tools/classify-genre.js:81 — `parseJson` has simpler error recovery than the util version. Consolidating would pick the more robust path — behavior-equivalent on success, strictly better on malformed inputs, but technically a behavior change on failure paths. Author judgment.
- /abs/tools/regenerate-summaries.js — may be obsoleted entirely by rebuild-levels.js (newer file, different strategy). Candidate for removal, but that is a product decision, not dedupe.

### Tools run
- knip — not run (plain JS, no package.json knip config).
- madge — not run; deferred to circular-deps lane.

### Files edited
- /abs/tools/lib/util.js (new)
- /abs/tools/generate-tree.js
- /abs/tools/add-phrase-maps.js
- /abs/tools/extract-concepts.js
</example>
</examples>

<constraints>
- Preserve behavior on every HIGH-CONFIDENCE edit. When a call site has a custom timeout, buffer size, or error-handling path, keep it as an argument to the shared helper rather than silently normalizing.
- Keep changes scoped to your lane. When another lane (unused imports, circular deps, weak types) has a cleaner claim on a finding, surface it as UNCERTAIN with a note like "defer to the unused-code lane" rather than handling it yourself.
- Mirror the file's existing style (indentation, quote style, import ordering). Your edits should read as if the original author wrote them.
- When a language-appropriate tool exists (knip/madge for JS/TS, vulture/deadcode for Python, unused-imports for Rust, etc.), run it as part of research when in scope for your lane. Note any substitutions in the Tools run section.
- An UNCERTAIN item should be one where a domain-aware reviewer could legitimately go either way. If you are only uncertain because you are lazy about a simple check, do the check.
- When you find two places that compute the "same" thing, diff them for algorithmic or constant divergence before proposing consolidation. Different algorithms, ratios, thresholds, fence-stripping rules, or error-recovery paths mean that "deduplicating" silently changes behavior at one call site. Any such divergence is UNCERTAIN by default — surface it with a named description (which constants differ, which outputs would change).
</constraints>

<verify>
Before ending your turn, confirm:
- Every HIGH-CONFIDENCE edit you listed is present in the working tree at the cited path and line.
- Every file you edited appears in both the HIGH-CONFIDENCE list and the Files edited list.
- Every UNCERTAIN item explains why it is genuinely ambiguous, not merely unfinished.
- Every edit stays within your lane's claim — e.g., unused-import deletions belong to the unused-code lane, not the dedupe lane.
- Public exports the file had before are still exported after, unless removal was the goal and is flagged.
- Before removing any symbol, function, method, or export, grep for callers in BOTH source AND test directories (e.g. `tests/`, `*_test.*`, `*.test.*`, `*.spec.*`). A symbol with zero source callers but a live TEST caller is NOT dead — flag it UNCERTAIN, do not delete.
</verify>

<done>
An orchestrator could merge your report with seven peer reports, apply zero additional review to the HIGH-CONFIDENCE list, and hand the UNCERTAIN list to the owner knowing every item in it is a real judgment call.
</done>

<return>
Return the report in the structure specified in the top `<return>` block. End the output at the Files edited list.
</return>

<context>
Target path: <resolved target>
</context>
```

### Step 3 — Shaw's 8 subagent briefs (verbatim — DO NOT paraphrase)

Each brief below is the exact text to drop into the `<INSERT ONE OF SHAW'S 8 BRIEFS VERBATIM>` slot above. Preserve punctuation, casing, and phrasing.

**Subagent 1 — Dedupe / DRY:**
> Deduplicate and consolidate all code, and implement DRY where it reduces complexity

**Subagent 2 — Type consolidation:**
> Find all type definitions and consolidate any that should be shared

**Subagent 3 — Unused code (knip):**
> Use tools like knip to find all unused code and remove, ensuring that it's actually not referenced anywhere

**Subagent 4 — Circular deps (madge):**
> Untangle any circular dependencies, using tools like madge

**Subagent 5 — Weak types:**
> Remove any weak types, for example 'unknown' and 'any' (and the equivalent in other languages), research what the types should be, research in the codebase and related packages to make sure that the replacements are strong types and there are no type issues

**Subagent 6 — Defensive try/catch:**
> Remove all try catch and equivalent defensive programming if it doesn't serve a specific role of handling unknown or unsanitized input or otherwise has a reason to be there, with clear error handling and no error hiding or fallback patterns

**Subagent 7 — Legacy / fallback:**
> Find any deprecated, legacy or fallback code, remove, and make sure all code paths are clean, concise and as singular as possible

**Subagent 8 — AI slop / stub comments:**
> Find any AI slop, stubs, larp, unnecessary comments and remove. Any comments that describe in-motion work, replacements of previous work with new work, or otherwise are not helpful should be either removed or replaced with helpful comments for a new user trying to understand the codebase-- but if you do edit, be concise

### Step 4 — Aggregate

Once all 8 agents return:

1. Collect each agent's critical assessment + list of edits.
2. Deduplicate across agents (e.g., agent 1 and agent 7 both touching the same legacy helper — keep one).
3. Collect all UNCERTAIN items into a single "Needs Review" section.

### Step 4.5 — Verify + Repair (the regression gate)

> This stage is the one high-value thing the parallel sweep historically lacked. Added 2026-06-01 after an A/B test (this parallel design vs a propose→central-apply→verify redesign — see Design notes).

Once the edits are applied and aggregated:

1. **Re-run the Step 1.5 verify command(s)** on the cleaned tree.
2. **Diff against the baseline.** Only NEW failures — tests/compile/typecheck that passed at baseline and now fail, or NEW collection/import errors — count as regressions. Pre-existing baseline failures are NOT regressions; do not chase them.
3. **If there are regressions**, dispatch ONE repair subagent (`general-purpose`) with: the failing output, the baseline, and the aggregated list of applied edits. Its job: fix the regression with the MINIMAL change — or revert the specific offending edit — without touching unrelated code. Then re-run the verify command to confirm green vs baseline.
4. **Surface the result** in the final report: baseline → post-cleanup → post-repair, with any edit that was reverted called out.

Repair is bounded to ONE pass. If a regression survives one repair attempt, REVERT the edits implicated and surface the item under "Needs Review" rather than iterating — an un-repairable regression means the cleanup was wrong, not that it needs more agents.

### Step 5 — Report

Present to user:

```markdown
## Code Cleanup Report — <target path>

### Summary
- Agents run: 8
- Files edited: N
- Total high-confidence fixes applied: N
- Uncertain items surfaced: N
- Regression gate: baseline [pass/fail] → post-cleanup [pass/fail] → post-repair [pass/fail] (N edits reverted)

### Per-agent results

#### Agent 1 — Dedupe / DRY
- Assessment: [one paragraph]
- Edits: [file list]
- Uncertain: [items, if any]

(... repeat for all 8 ...)

### Needs Review (aggregated uncertain items)
- [file:line] — [issue] — [agent N's suggestion]

### Suggested next step
- The verify+repair gate (Step 4.5) already re-ran the test suite / typechecker against the baseline — see the Regression gate line above. If it is not green vs baseline, do NOT commit; review the surfaced regression first.
- Commit the sweep as a single atomic commit per-agent or as one unified commit.
```

## Design notes

- **Parallel, not sequential.** All 8 dispatch in one message. The whole point is parallel subagent work — serializing defeats it.
- **`general-purpose` subagent type.** These agents write code; `Explore` is read-only and will fail to implement.
- **Verbatim Shaw briefs.** The briefs above are copied from Shaw's original. Do not "improve" them — the prompt works as-is and has been trusted by the dev community.
- **One lane per agent.** Don't merge lanes. Overlap is fine (the dedupe step in Step 4 handles that); what you can't recover is a lane being skipped.
- **Target path, not project name.** Subagents take an absolute path so the skill works on any repo, not just Second Brain projects.
- **Verify+repair gate over central-apply (A/B finding, 2026-06-01).** An A/B test ran this parallel design against a redesign that funneled all 8 lanes' proposals through ONE central apply stage (propose → dedup → apply → verify). The central-apply stage timed out and applied **zero** edits — it fails closed to nothing, strictly worse than this design's "partial but real" failure mode. Meanwhile the parallel design's concurrent edits did NOT corrupt the tree (post-hoc dedup absorbed cross-lane overlap on a shared file cleanly). The one thing the redesign got right — a verify+repair regression gate — was borrowed back as Step 4.5 without touching the parallel-apply core. Lesson: keep the parallel sweep; add the gate; do not serialize the apply. (The test-caller check in the wrapper `<verify>` slot was added the same day, after OLD deleted a method a test still called.)

## Known caveats

- Tools like `knip` (Subagent 3) and `madge` (Subagent 4) are JS/TS specific. Python/Rust/Go targets: those agents should use language-appropriate equivalents (vulture, deadcode, unused-imports; pydeps, go-callvis) and note the substitution in their report.
- Running 8 agents in parallel is token-heavy. For very large monorepos, the user may want to narrow scope by passing a subdirectory as the target.
- This is a sweep, not a rewrite. The skill does not refactor architecture, rename files, or change public APIs — only the 8 hygiene lanes above.

## Attribution

Prompt origin: **shaw makes magic** (public community share). The 8 briefs and the meta-instruction are preserved verbatim from the original public share.
