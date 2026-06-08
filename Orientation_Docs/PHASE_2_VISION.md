<!-- __FILL_FROM_USER__:phase_2_vision
     FOR THE AGENT READING THIS: this is GENERIC context-engineering guidance for
     evolving a second brain from "ingest mode" (mining old sources) to "partnership
     mode" (engaging with live thinking). The principles below are reusable; adapt the
     specifics (phase names, doc/skill counts, current model) to the owner's actual
     setup, and keep live status in STATE_OF_SECOND_BRAIN.md. -->

# FUTURE EVOLUTION: INTELLECTUAL PARTNER MODE
*Plan for Post-Ingest Phase Transition*
*Status: FORWARD-LOOKING VISION — current execution status is tracked in STATE_OF_SECOND_BRAIN.md. This doc is the aspiration, not the live state.*

---

## CONTEXT

This plan draws on public writing about context engineering for coding agents, and on thinking through what comes after the data-ingest phases are complete.

**Key insight from the blog:** "Context engineering is problem-solving - what configuration of context is most likely to generate the model's desired behavior?"

---

## TECHNICAL INSIGHTS FROM BLOG

### Context Window Management

| Metric | Value | Implication |
|--------|-------|-------------|
| Modern Opus context | ~200K tokens | ~150K words theoretical |
| **Effective utilization** | **50-60%** | ~100-120K usable before degradation |
| Compaction threshold | **60%** | Start fresh or compact at this point |
| Single complex task | 6K+ tokens | Searches + reads + edits add up fast |

**Tactics:**
- Use `/context` to monitor current usage
- Avoid complex tasks mid-conversation - start fresh for involved work
- Tool calls + tool outputs BOTH occupy context
- MCP server tool definitions load upfront = context bloat

### Sub-Agent Architecture Details

**Five agent types with different context inheritance:**

| Agent Type | Context | Tools | Use Case |
|------------|---------|-------|----------|
| `Explore` | **FRESH** (no inheritance) | Read-only: Glob, Grep, Read | Independent searches |
| `general-purpose` | **FULL** inheritance | All tools | Related reasoning tasks |
| `Plan` | **FULL** inheritance | All tools | Architecture planning |
| `claude-code-guide` | Fresh | Docs lookup | Documentation queries |
| `statusline-setup` | Fresh | Config tools | Settings changes |

**Key spawning parameters:**
- `run_in_background: true` - prevents UI flickering from parallel agents
- `resume: [agent_id]` - continue from previous execution with full context
- `model: "opus"/"sonnet"/"haiku"` - override default model

**Implication for Second Brain:** Explore agents are ideal for searching across synthesis docs because they start fresh (no context bloat from conversation history).

### Token Consumption Patterns

**What eats tokens:**
- Every tool call (the request itself)
- Every tool result (can be large for file reads)
- MCP server definitions (loaded upfront)
- Auto-loaded orientation docs (currently 11 files)

**Mitigation:**
- Load skills **on-demand**, not all upfront
- Keep each skill file **<500 lines**
- Use synthesis docs instead of raw files (pre-computed context)
- Background agents compartmentalize work

### Context Engineering Tactics

**Recitation pattern:**
- Objectives drift to "middle" of context as new tokens accumulate
- Repeatedly inject goals via todo lists to keep in recent attention
- `<system-reminder>` tags push priorities into recent attention span

**This is why our current TODO system helps** - it's not just task tracking, it's objective recitation.

### Hook Patterns

| Hook | Trigger | Use Cases |
|------|---------|-----------|
| `UserPromptSubmit` | Before Claude processes input | Inject reminders, validate context |
| `Stop` | After Claude completes response | Notifications, auto-continue, logging |

**Potential applications for Second Brain:**
- Auto-remind about active project when related keywords detected
- Inject synthesis doc pointers based on topic
- Log intellectual queries for pattern analysis

### Debugging & Monitoring Commands

| Command | Purpose |
|---------|---------|
| `/context` | Monitor current context usage |
| `/usage` | Token consumption details |
| `/stats` | Session statistics |
| `Esc+Esc` or `/rewind` | Rollback to previous checkpoint |
| `Ctrl+R` | Backward search across project conversations |
| `/compact` | Fast compaction (loses nuance) |

### Known Workarounds

| Issue | Workaround |
|-------|------------|
| Parallel sub-agents cause UI flickering | Use `run_in_background: true` |
| `/compact` loses nuance | Manual handoff for complex tasks |
| Alt+Tab thinking toggle Mac bug | Use settings.json toggle instead |
| Context degradation on long tasks | Start fresh session at 60% |

### File Structure Best Practices

```
.claude/
  commands/           # Custom slash commands
  agents/             # Custom sub-agent definitions
  skills/
    {skill-name}/
      SKILL.md        # <500 lines recommended
      [supporting files]

~/.claude/
  commands/           # System-wide custom commands
  settings.json       # CLI preferences
```

**Current Second Brain structure:**
- a handful of orientation docs auto-loaded each session
- a set of skills in `.claude/skills/`
- This may be too much upfront context - consider tiering

---

## THE PHASE TRANSITION

Two distinct operational modes:

| **Ingest Mode** (Phases 1-10) | **Partnership Mode** (Future) |
|------------------------------|----------------------------|
| Mining old sources | Engaging with current thinking |
| Structuring data | Surfacing connections |
| Procedural (templates, workflows) | Intellectual (challenge, synthesize) |
| Skills: ingestion + dedupe-check | Skills: connection-finding, project-tracking + new |
| CLAUDE.md: "how to process files" | CLAUDE.md: "how to engage intellectually" |

---

## KEY INSIGHTS FROM BLOG POST

### 1. Modularize, Don't Bloat
Keep CLAUDE.md lean (~500 lines per skill domain). Use hooks + skills to load expertise on-demand. Current 9 auto-loaded orientation docs is substantial context.

### 2. Context Rot is Real
Performance degrades as context grows. Aim for 50-60% utilization. Matters for synthesis work pulling from many files.

### 3. Recite Objectives
Keep goals in recent attention. For intellectual partnership, surface *intellectual priorities* not just task lists.

### 4. Progressive Disclosure
Sub-agents inherit context selectively. Design choice: some agents need fresh starts, others need full context.

### 5. Taste Refinement Over Implementation
"Implementation is fast now - spend time on taste." Claude handles retrieval/synthesis, user steers judgment.

---

## THE SUBFOLDER PROBLEM

### Current State
~250 files in `Journal_Intellectual/` is a dump. Keywords enable cross-folder retrieval, so subfolders can be aggressive about thematic grouping without breaking discovery.

### Proposed Structure

```
Second_Brain/
├── Journal_Intellectual/
│   ├── Technology/               # ~50 files
│   │   ├── _SYNTHESIS.md         # Entry point, connects dots
│   │   └── [individual files]
│   ├── Philosophy/               # ~30 files
│   ├── Governance/               # ~25 files
│   ├── Economics_Business/       # ~40 files
│   ├── Habits_Identity/          # ~20 files
│   ├── Coordination_Game_Theory/ # ~15 files
│   └── Observations_Misc/        # Catch-all
├── Inventions/
│   ├── Bits_AI_Tools/
│   ├── Bits_Platforms/
│   ├── Bits_Consumer/
│   ├── Atoms_Hardware/
│   └── Atoms_Physical/
[etc. for other major categories]
```

### Synthesis Documents

Each subfolder gets a `_SYNTHESIS.md`:
- Key themes and how thinking evolved
- Contradictions and unresolved tensions
- Connections to active projects
- Open questions still cooking
- Pointers to related files in OTHER categories

The synthesis doc becomes the *entry point*. Claude loads `_SYNTHESIS.md` first, only drilling into individual files when needed. Massive context savings.

---

## CLAUDE.MD EVOLUTION

### Current State
Procedural - "how to process files, templates, golden rules"

### Proposed Addition

```markdown
## INTELLECTUAL PARTNERSHIP MODE

You are not just a retrieval system. You are an intellectual sparring partner.

### Engagement Principles
1. **Challenge when appropriate** - If an idea contradicts something I've written
   elsewhere, surface the contradiction. Don't just validate.
2. **Connect aggressively** - When I discuss a topic, proactively pull related
   ideas from other categories, even if I didn't ask.
3. **Track evolution** - Note when my thinking has changed on a topic. "You wrote
   X in 2023 but now you're saying Y - is this an evolution or contradiction?"
4. **Surface unfinished work** - When a topic relates to an active project,
   remind me what's blocking progress.

### When NOT to Partner
- During ingest/processing work (stay procedural)
- When I explicitly want just retrieval, not engagement
- When I'm in "brain dump" mode (capture first, analyze later)
```

---

## NEW SKILLS FOR PARTNERSHIP PHASE

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/challenge` | "Challenge this idea" | Find contradicting ideas in Second Brain |
| `/synthesize [topic]` | "Synthesize my thinking on X" | Create or update `_SYNTHESIS.md` for a topic |
| `/accelerate [project]` | "Accelerate [a flagship project]" | Surface ALL related content for shipping |
| `/signals [topic]` | "Surface signals on X" | Pull relevant signals from files |
| `/evolution` | "How has my thinking evolved on X?" | Track idea development over time |

The existing `connection-finder` and `project-tracker` are already designed for this - they just need to work with synthesis docs instead of raw file dumps.

---

## IMPLEMENTATION PHASES

### Phase A: Subfolder Structure (1-2 sessions)
1. Analyze each major category for natural clusters (using keywords, project connections)
2. Propose subfolder structure for approval
3. Migrate files
4. Update indexes

### Phase B: Synthesis Docs (ongoing)
1. Start with highest-value categories (`Journal_Intellectual/Technology/`)
2. Create `_SYNTHESIS.md` for each subfolder
3. This is where the intellectual partnership work happens - Claude reads all files, identifies patterns, writes synthesis

### Phase C: CLAUDE.md + Skills Update
1. Add "Intellectual Partnership Mode" section to CLAUDE.md
2. Create new partnership skills
3. Update existing skills to work with synthesis docs

---

## THE META-INSIGHT

The blog's core point applies to this transition:

> "What configuration of context is most likely to generate the model's desired behavior?"

**For ingest mode:** Load templates, processing specs, approval workflows.
**For partnership mode:** Load synthesis docs, intellectual priorities, current project status.

The subfolder + synthesis doc structure is essentially **pre-computing context** so that when engaging intellectually, Claude has dense, relevant context rather than sprawling raw files.

---

## IMMEDIATE TACTICAL IMPROVEMENTS

These can be applied NOW, even during ingest phases:

### 1. Monitor Context Usage
Start using `/context` regularly during long sessions. Get a feel for how fast we burn through the 60% threshold.

### 2. Use Background Agents More
Current batch processing already uses subagents, but ensure `run_in_background: true` is set to prevent flickering and allow parallel work.

### 3. Consider Tiering Orientation Docs
Current state: several docs auto-loaded. Could tier into:
- **Always loaded:** CLAUDE.md, INTELLECTUAL_LANDSCAPE.md (core identity)
- **On-demand:** Processing specs, operational docs (already done)
- **Potentially demote:** KEYWORD_GUIDE.md (large, could be skill-loaded)

### 4. Skill File Audit
Check if any skills exceed 500 lines. If so, split into focused sub-skills.

### 5. Hook Experiment
Try a simple `UserPromptSubmit` hook that injects active project reminders based on keyword detection. Low-effort test of the pattern.

### 6. Session Hygiene
For complex ingest batches, start fresh sessions rather than continuing degraded context. The blog confirms this is better than compacting.

---

## PREREQUISITES

Before implementing this plan:
- [ ] Complete the remaining ingest phases (mine all source exports)
- [ ] All source data imported and structured
- [ ] Second Brain file count stabilized
- [ ] User ready to shift from ingest to engagement mode

---

## RELATED DOCS

- `CLAUDE.md` - Boundaries and rules (entry point)
- `SKILLS_REFERENCE.md` - Existing skill definitions
- `INTELLECTUAL_LANDSCAPE.md` - Projects and themes context
- `SECOND_BRAIN_MASTER_INDEX.md` - Current file organization

---

*This document will be activated when ingest phases are complete and user is ready to transition.*
