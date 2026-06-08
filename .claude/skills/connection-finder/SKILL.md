---
name: connection-finder
description: >-
  Proactively surfaces related ideas from the Second Brain while the owner is
  thinking out loud. Uses semantic search + grep (via scripts/sb_embed.py) to
  connect new thinking to existing ideas without being asked.
  Activates when the owner discusses concepts (AI, singularity, coordination),
  mentions people, explores themes, or brainstorms.
  Does NOT activate for file operations, debugging, explicit-instruction
  execution, or logistics — this is for ideation, not task-completion.
  **Sensitivity modes** (SETTINGS.md): AGGRESSIVE (current default — fire
  proactively), MODERATE (fire only on strong semantic matches), CONSERVATIVE
  (fire only on exact-keyword overlaps).
  Caps at 3 connections per activation. Watches for rejection signals
  ("not relevant", "stretch", owner ignores) — after 3+ rejections in a
  session, proactively offers to dial down sensitivity.
  Goal: surface USEFUL connections that advance thinking, not overwhelm.
allowed-tools: Read, Grep, Glob, Bash
required_context_files:
  - Orientation_Docs/INTELLECTUAL_LANDSCAPE.md
  - Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md
  - Orientation_Docs/CONTENT_TAXONOMY.md
---

# Connection Finder

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`
- `Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md`
- `Orientation_Docs/CONTENT_TAXONOMY.md`

<!-- silent-context-load:v1 -->

This skill proactively surfaces related ideas from the owner's Second Brain using semantic search. The goal is to connect new thinking to existing ideas without being asked.

## Trigger Conditions

Activate (AGGRESSIVE mode) when the conversation involves:
- Discussing concepts or ideas (AI, singularity, coordination, etc.)
- Mentioning people or thinkers
- Exploring themes (vibe coding, live player analysis, longevity, etc.)
- Thinking through problems or possibilities
- Brainstorming or ideating

Do NOT activate when:
- Just executing file operations
- Following explicit instructions
- Debugging or troubleshooting
- Discussing logistics

## Required Context (Tier 2 Dependencies)

Before searching for connections, use these docs:

1. **KEYWORD_GUIDE.md** — Vocabulary reference for matching concepts
2. **SECOND_BRAIN_MASTER_INDEX.md** — Folder structure documentation (Tier 1, likely already loaded)
3. **INTELLECTUAL_LANDSCAPE.md** — Project/theme context (Tier 1, likely already loaded)

## When Activated

### 1. Identify Key Concepts

Extract the core concepts being discussed. Reference:
- `Orientation_Docs/KEYWORD_GUIDE.md`

Map to existing vocabulary where possible.

### 2. Search for Related Content

**Primary: Semantic search** (finds conceptual connections; see note below):

```bash
python3 $SECOND_BRAIN_ROOT/scripts/sb_embed.py search "concept being discussed" --top-k 10 --json
```

> `scripts/sb_embed.py` is a semantic-search stub in this repo — it must be wired to
> a local embedding backend before it returns real results. See `SETUP.md` for
> instructions. If `sb_embed.py` is not yet configured, the skill falls back
> automatically to grep (Step 2b).

**Fallback (2b): Grep for precision** (exact keyword matches):

```bash
# Search for keywords
grep -ri "[keyword]" "$SECOND_BRAIN_ROOT" --include="*.md" -l

# Search for project connections
grep -r "**Projects:**.*[ProjectName]" "$SECOND_BRAIN_ROOT" --include="*.md"

# Search for people
grep -ri "[PersonName]" "$SECOND_BRAIN_ROOT" --include="*.md" -l
```

Set `$SECOND_BRAIN_ROOT` to the absolute path of your brain's root directory (e.g. `export SECOND_BRAIN_ROOT=/path/to/Second_Brain`).

Subfolders include: `Inventions/`, `Journal_Intellectual/`, `Journal_Personal/`, `Writing_SciFi/`, `Writing_AllElse/`, `Predictions/`, `External_Sources/`, `Reference/`, `Health/`, etc.

### 3. Surface Connections

Report findings briefly:
- "This connects to [idea title] — [1 sentence summary]"
- "You've explored this before in [source]"
- "Related to your [project] work"

Maximum 3 connections per activation unless asked for more.

### 4. Identify Patterns (Optional)

If recurring themes emerge:
- "This is the 3rd time [concept] has come up recently"
- "This builds on your earlier thinking about [theme]"

## Output Format

Keep it brief. Example:

```
**Connections found:**
- Your "Coordination Theory" idea in Journal_Intellectual/ explores similar game-theory concepts
- "[__FILL_FROM_USER__:active_project]" connects via governance themes
- "[__FILL_FROM_USER__:key_thinker]" mentioned in 4 existing files

Want me to expand on any of these?
```

## Sensitivity Management

Current setting: **AGGRESSIVE** (see [SETTINGS.md](SETTINGS.md))

### Feedback Tracking

Watch for rejection signals:
- "That's not relevant"
- "Not a good connection"
- "That's a stretch"
- Owner ignores the connection entirely

After 3+ rejections in a session, proactively ask:
> "I've noticed a few of my connection suggestions weren't hitting the mark. Would you like me to dial back the sensitivity?"

### Adjusting Sensitivity

If the owner requests lower sensitivity:
1. Update [SETTINGS.md](SETTINGS.md)
2. Switch to MODERATE or CONSERVATIVE mode
3. Confirm the change

## Connection Quality Criteria

A good connection:
- Directly relates to the concept being discussed
- Adds context or builds on the idea
- Comes from a meaningful source (not just keyword coincidence)

A weak connection (avoid):
- Only shares one common word
- From a completely different context
- Would require extensive explanation to justify

## Philosophy

A mature Second Brain holds years of thinking. New ideas don't exist in isolation — they connect to existing patterns. This skill surfaces those connections proactively, enabling synthesis and avoiding reinvented wheels.

The goal isn't to overwhelm with connections — it's to surface the *useful* ones that advance thinking.
