---
name: verify-idea
description: >-
  Semantic duplicate detection for Second Brain ideas. Distills input to core
  concept, runs `sb_embed.py verify` (embedding-based similarity, ~50ms), reads
  top candidates, and returns one of four verdicts:
  **DUPLICATE** (>0.85 similarity — exact same idea, point to existing file, skip creation),
  **OVERLAP** (0.70–0.85 — related but distinct, consider merging or linking),
  **NOT FOUND** (<0.70 — safe to create new file),
  **UNCERTAIN** (ambiguous matches — surface them to human for judgment).
  Falls back to grep for keyword precision when semantic search is ambiguous.
  Core rule: SEMANTIC match, not keyword match. Two ideas are duplicates when they
  propose the same unique insight, regardless of wording — shared keywords with
  different proposals do NOT count as duplicates.
  Called by the ingestion skills (e.g. /process-content, /ingest-example) before file
  creation. Also invoke directly when user asks "is this captured?",
  "do I have this?", "check for duplicates", "have I thought about this before?".
allowed-tools: Read, Grep, Glob, Bash
required_context_files:
  - Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md
  - Orientation_Docs/KEYWORD_GUIDE.md
---

> **Setup note:** the `sb_embed.py verify` step needs a local embedding helper that is **not bundled** — see `SETUP.md` at the repo root. Without it, this falls back to grep keyword matching (described below), so the skill still works.

# Verify Idea

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md`
- `Orientation_Docs/KEYWORD_GUIDE.md`

<!-- silent-context-load:v1 -->

Semantic duplicate detection for Second Brain ideas using embeddings + grep.

## Quick Start

1. Extract core concept from input
2. **Run semantic verify command** (fast, catches rephrased duplicates)
3. If uncertain, grep for specific keywords as backup
4. Read top candidates, compare semantically
5. Return status: DUPLICATE, OVERLAP, NOT FOUND, or UNCERTAIN

## Workflow Checklist

```
- [ ] Step 1: Distill input to core concept (1-3 sentences)
- [ ] Step 2: Run semantic verify command (fast duplicate check)
- [ ] Step 3: If UNCERTAIN, grep for specific keywords as backup
- [ ] Step 4: Read top candidate files (Summary + Original Text)
- [ ] Step 5: Semantic comparison (same insight? not just shared keywords)
- [ ] Step 6: Return status with recommendation
```

## Primary: Semantic Verify (Fast)

```bash
# Check for duplicates using embeddings (~50ms)
python3 $SECOND_BRAIN_ROOT/scripts/sb_embed.py verify "the core concept text" --json

# Output shows:
# - status: DUPLICATE (>0.85) | OVERLAP (0.70-0.85) | NOT_FOUND (<0.70)
# - matches: list of similar files with similarity scores
```

## Backup: Grep for Precision

When semantic search returns UNCERTAIN or you need exact matches:

```bash
# Distinctive terms
grep -ri "[term]" Second_Brain/ --include="*.md" -l

# Project connections
grep -r "**Projects:**.*[ProjectName]" Second_Brain/ --include="*.md"

# Category-specific
grep -ri "[term]" Journal_Intellectual/ --include="*.md" -l
```

Cast wide net - better to read 10 files than miss a match.

## Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| **DUPLICATE** | Exact same idea exists | Skip, point to existing |
| **OVERLAP** | Related but distinct | Consider merge or link |
| **NOT FOUND** | No semantic match | Safe to create |
| **UNCERTAIN** | Possible matches | Human review needed |

## Critical Rule

**SEMANTIC MATCH, NOT KEYWORD MATCH**

Two ideas are the same if they propose the **same unique insight**, regardless of wording.

- Same concept, different words → DUPLICATE
- Shared keywords, different proposals → NOT duplicate
- When uncertain → say UNCERTAIN, let user decide

## References

- [Output Format](references/output-format.md) - Result template, comparison rules
