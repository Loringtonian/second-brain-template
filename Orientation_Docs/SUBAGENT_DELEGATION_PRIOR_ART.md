# Sub-Agent Delegation — Prior Art & Techniques
*How to write better prompts when Claude spawns Claude*
*Synthesized from SPRIG, PROMST, Auto-Enhance, reconciled with Anthropic's current guidance*

> This is the **why** behind the 10-slot delegation skeleton in `CLAUDE.md`. The skeleton without the
> reasoning is cargo-cult; read this once so the framing rules stick. It is general domain knowledge —
> nothing here is specific to one owner. The `/delegate-check` skill lints a draft prompt against it.

---

## Why this doc exists

When the orchestrator Claude spins up a team, the results are often disappointing because **the prompt
given to the sub-agent was thin** — terse, under-specified, missing context. There is no single widely
accepted public benchmark whose central purpose is "measure how good model A is at writing prompts for
model B." The closest three — **SPRIG** (system-prompt evolution), **PROMST** (prompt optimization for
multi-step agentic tasks), and **Auto-Enhance** (a meta-benchmark where one agent modifies another) —
each illuminate part of the problem. This doc distills their empirical findings into techniques you can
apply right now when writing sub-agent prompts.

## The three benchmarks at a glance

| Benchmark | What it measures | Closest to the orchestrator→sub-agent problem? |
|---|---|---|
| **SPRIG** | Evolves a task-agnostic *system* prompt across 47 benchmarks (GA over component categories). | Partial — single-turn, no tool use. |
| **PROMST** | Optimizes prompts for *multi-step, tool-using, agentic* tasks; human-authored failure-detector rules are the feedback channel. | **Closest** — this is the shape of orchestrator → sub-agent → tool-loop. |
| **Auto-Enhance** | Meta-benchmark: can a top-level agent modify a reference agent (prompt/scaffold/model) to improve downstream performance? | Broader superset. |

None isolate "model A's prompt-writing ability for model B" as a scoring axis — that gap is real.

### Citations
- **SPRIG:** Zhang et al. — [arXiv 2410.14826](https://arxiv.org/abs/2410.14826) · [TMLR OpenReview](https://openreview.net/forum?id=VdVV24KSWK) · [code](https://github.com/orange0629/prompting)
- **PROMST:** Chen et al., EMNLP 2024 — [arXiv 2402.08702](https://arxiv.org/abs/2402.08702) · [ACL Anthology](https://aclanthology.org/2024.emnlp-main.226/) · [code](https://github.com/yongchao98/PROMST)
- **Auto-Enhance:** NeurIPS 2024 Safe Agents Workshop — [OpenReview](https://openreview.net/forum?id=YAhyaNEoy9) · [code](https://github.com/samizdis/impact-academy/)
- **Anthropic current guidance (supersedes where it conflicts):** [Prompt engineering](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/) · [Claude Code best practices](https://code.claude.com/docs/en/best-practices) · [Custom sub-agents](https://code.claude.com/docs/en/sub-agents)

---

## Anthropic's current guidance (supersedes GPT-era findings where they conflict)

The three benchmarks are GPT-3.5/4o-era. Anthropic's current guidance moves differently on two points —
**negative framing** and **prescriptive algorithm outlines** — and you want Claude-tuned advice, not
model-generic folklore.

**Negative instructions → positive reframes.**
> *"Tell Claude what to do instead of what not to do."* — Anthropic prompt engineering docs

If a prohibition is genuinely necessary, pair it with the *reason* — the reasoning defuses the priming
effect, while a raw prohibition primes the banned behavior. (*"…never use ellipses, because the
text-to-speech engine won't know how to pronounce them."*)

**General instructions → over prescriptive steps.**
> *"Prefer general instructions over prescriptive steps… Claude's reasoning frequently exceeds what a
> human would prescribe."*

This conflicts with Auto-Enhance's "include an explicit numbered algorithm" finding (load-bearing for
GPT-4o). Claude 4.x prefers direction to hand-holding.

**Role/persona — qualified endorsement.** One sentence helps and focuses tone; a character sheet does
not. (SPRIG found personas selected *below chance*; Anthropic's one-sentence guidance wins for Claude.)

**XML-tag wrapping — endorsed.** Wrap each content type in its own tag to reduce misinterpretation.

**Examples — 1–3 positive, never negative.** No "here's a bad response, don't do that" pattern.

**Verification over prediction.**
> *"Claude performs dramatically better when it can verify its own work."*

Favor a **forward-looking verification checklist** over backward-facing "don't do X" warnings.

**Termination — clear scope, not stop-clauses.** A well-scoped task with a definition of done stops
cleanly; no "stop when you see X" needed.

### Net revisions to the GPT-era technique list
- **Numbered algorithm** → prefer a general approach; spell out steps only for genuinely rigid multi-stage procedures.
- **Pre-warned failure modes** ("if you hit X do Y") → forward-facing verification checklist; if a known failure must be named, frame it positively with the reason.
- **Violation-path sentences** → positive scope design instead (they prime the violation).
- **Step/token budgets** → drop by default (they prime conservation and premature termination).
- **Explicit termination clause** → replaced by definition-of-done.
- **Persona** → one sentence if it clarifies perspective; never a résumé.

Everything orthogonal to framing (output-schema pinning, restate-the-task, absolute paths, loop
detection, diagnose-before-rewrite, pass@k, file-write tools over `echo`, rolling state log) still holds.

---

## The distilled techniques (skim before dispatching)

Each is grounded in a cited finding. Apply as a checklist; pick what matches the task.

**Structure**
1. **Separate the layers** — standing rules (who you are / how to think / safety) in one block, task-specific instructions in another. System- and task-level gains are additive. (SPRIG)
2. **Pin the output schema at the top AND the bottom.** Format drift is the #1 multi-step failure mode. (PROMST)
3. **Keep the standing block short** — ~5–10 single-instruction sentences; long prompts did not win. (SPRIG)
4. **Whole-sentence instructions, not comma-joined phrase lists.** (SPRIG)

**Include**
5. **Restate-the-task** ("restate and elaborate on the request before responding"). (SPRIG)
6. **2–3 distinct thinking cues**, not one. (SPRIG)
7. **One short "good property" sentence** — max three adjectives. (SPRIG)
8. **An explicit uncertainty clause** ("if you are unsure, say so") — cheap hallucination insurance. (SPRIG)
9. **At least one concrete worked example of success.** Dropping the one-shot example crashed pass@5. (Auto-Enhance)
10. **Absolute paths, never relative** — sub-agents confuse cwd across tool calls. (Auto-Enhance)

**Execution & verification**
11. **Force a baseline before any change** — successful runs established current state first; failed runs tuned blind. (Auto-Enhance)
12. **Verify after every change, not at the end** — "after editing, RUN the check; don't claim success without the updated result." (Auto-Enhance)
13. **Prefer file-write tools over `echo`/heredoc** — nested-quote errors were the single most reproducible failure. (Auto-Enhance)
14. **Inject a forcing function on repeat** — if you see identical-action cycles, the next turn says "don't repeat your last action — try X." (PROMST)
15. **Discourage cascading error-chasing** — "if a command fails, first check whether your last change is the root cause; don't invent new paths/flags to dodge the symptom." (Auto-Enhance)
16. **Force single-strategy commitment** — "plan, reason, and choose ONE strategy." (Auto-Enhance)

**What NOT to include**
17. **Skip character-sheet roles** and **emotional stimuli** — both selected below chance. (SPRIG)
18. **Don't fold all failures into one blob** — bucket by type. (PROMST)
19. **Don't rely on "figure out what went wrong" meta-prompts** — they lose to structured feedback. (PROMST)

**Orchestration meta**
20. **Asymmetric model split** — a strong model writes the prompt; a cheaper model executes. (PROMST) In Claude terms: **Opus orchestrator writes prompts; Sonnet/Haiku sub-agents execute.**
21. **Plan for pass@k, not pass@1** — variance is large; budget for retries. (Auto-Enhance)
22. **Even frontier sub-agents gain ~28% from a better prompt** — a model upgrade does not substitute for prompt craft. (PROMST)
23. **When iterating a prompt, split "diagnose failure" from "rewrite"** — two calls, not one, with the full prompt lineage in context. (PROMST)

---

## The 10-slot skeleton (Anthropic-reconciled, positive framing throughout)

```
 1. <purpose>     PURPOSE & CONTEXT      — why this matters, what feeds downstream.
 2. <role>        ROLE                   — one sentence, optional. Trust the default otherwise.
 3. <return>      RETURN FORMAT (top)    — concrete output schema, up front.
 4. <approach>    GENERAL APPROACH       — the shape of the work, not a numbered recipe.
                                           Explicit steps only when genuinely multi-stage and rigid.
 5. <examples>    WORKED EXAMPLES        — 1–3 POSITIVE examples in <example> tags. No negatives.
 6. <constraints> CONSTRAINTS            — hard rules in POSITIVE framing; if you must prohibit, give the reason.
 7. <verify>      VERIFICATION CHECKLIST — "before returning, confirm X, Y, Z are true." Forward-looking.
 8. <done>        DEFINITION OF DONE     — what a complete answer looks like. Clear scope = clean stop.
 9. <return>      OUTPUT CONTRACT (bot.) — re-pin the schema at the bottom (format-drift insurance).
10. <context>     LIVE CONTEXT           — state, absolute paths, prior outputs. Absolute paths only.
```

Skip slots that don't apply — but deliberately; each omitted slot is a known failure mode.

> **Sub-agents inherit nothing automatically** — not `CLAUDE.md`, not `ROUTER.md`, not `MEMORY.md`, not
> the output style. The parent is the only channel: load the right context BEFORE delegating and
> hand-inject the relevant priors into the `<context>` slot. For a rule that must hold regardless of
> model compliance, the only deterministic mechanism is a PreToolUse hook, not a prompt instruction.

## Anti-patterns to watch for in your own sub-agent prompts
- **Terse single-paragraph brief** — missing purpose, schema, approach, verify-checklist, definition of done.
- **Negative phrasing as default** — "don't skip the schema, don't be verbose" → reframe positively.
- **Character-sheet roles** — one sentence max, if it clarifies perspective.
- **Numbered algorithm for a task Claude could reason through** — prefer general over prescriptive.
- **Pre-warned failure-mode laundry list** — flip to a verification checklist.
- **Step/token budgets** — prime conservation; drop for quality-critical work.
- **One-shot rewrite of a failed prompt** — diagnose first, then rewrite, with the lineage in context.
- **No schema at the bottom / no absolute paths** — the two cheapest, most common regressions.

---

## Building your own delegation benchmark (optional)

No public benchmark scores "how good is model A at writing prompts for model B." If you want a scoreboard
for your orchestrator prompts, a small opinionated one is worth owning: pick 3–5 multi-step, tool-using
tasks with *programmatic* success metrics; for each task make four variants that differ **only in how
much is in the orchestrator's prompt** (spell-out-everything → drop-commands → drop-example →
drop-algorithm) to isolate prompt-writing skill from task difficulty; score milestones + outcome at
pass@5 with early stop; report bootstrap CIs because variance is large. Feed the results back into your
few-shot examples (see the `/golden-evolver` skill's `delegation` task).

## Keywords
subagent-delegation, prompt-optimization, SPRIG, PROMST, Auto-Enhance, Anthropic-prompt-engineering,
positive-framing, negative-instruction-priming, verification-checklist, definition-of-done,
XML-tag-wrapping, asymmetric-model-split, 10-slot-skeleton, orchestrator-quality
