---
name: semantic-search
description: >-
  Fast semantic search over Second Brain using local embeddings (BAAI/bge-large-en-v1.5,
  via `sb_embed.py`). Finds ideas by MEANING, not just keyword overlap.
  **Commands:** `search "query"` (top-k ranked matches, ~50ms cached),
  `verify "idea"` (duplicate check with DUPLICATE/OVERLAP/NOT_FOUND verdict),
  `similar path/to/file.md` (find files semantically close to an existing one),
  `stats` (index health).
  **Filters:** `--project "Project Name"`, `--category "Journal"`, `--top-k N`, `--json`.
  **Use semantic search for:** broad concept recall ("what do I have about coordination?"),
  rephrased-duplicate detection, unexpected-connection discovery, pre-ingestion dedupe.
  **Use grep instead when:** you know the exact term/phrase, doing project/category
  lookups by exact string, or confirming a specific filename. Grep is precise;
  semantic is recall-wide.
  Best practice: combine — semantic for broad recall, grep for precision matching.
  Invoked via "find ideas about X", "what do I have on X", "related to X", "similar to this idea".
allowed-tools: Bash, Read
---

> **Setup note:** this skill calls `scripts/sb_embed.py` + a local embedding model, which is **not bundled** in this template — see `SETUP.md` at the repo root. Until you add it, fall back to keyword/`grep` search.

# Semantic Search

Find ideas by meaning, not just keywords. Uses local embeddings (BAAI/bge-large-en-v1.5).

**Performance notes:**
- First query: ~7s (model loading)
- `similar` command: ~50ms (uses cached vectors)
- Search/verify: ~6s per query (requires embedding)

## Quick Start

1. User provides concept/query
2. Run semantic search via CLI
3. Review results (similarity scores indicate relevance)
4. Optionally filter by project or category

## Commands

```bash
# Semantic search (fast, <50ms)
python3 scripts/sb_embed.py search "AI governance coordination" --top-k 10

# With JSON output for parsing
python3 scripts/sb_embed.py search "query" --top-k 10 --json

# Filter by project
python3 scripts/sb_embed.py search "query" --project "Project Name" --top-k 10

# Filter by category
python3 scripts/sb_embed.py search "query" --category "Journal" --top-k 10

# Check for duplicates (before creating new files)
python3 scripts/sb_embed.py verify "idea text here" --threshold 0.85

# Find similar to existing file
python3 scripts/sb_embed.py similar path/to/file.md --top-k 5

# Index stats
python3 scripts/sb_embed.py stats
```

## Verify Command Output

| Status | Meaning | Action |
|--------|---------|--------|
| **DUPLICATE** | >0.85 similarity | Skip, point to existing file |
| **OVERLAP** | 0.70-0.85 similarity | Consider merge or link |
| **NOT_FOUND** | <0.70 similarity | Safe to create new file |

## When to Use

**Use semantic search for:**
- Broad concept recall ("what do I have about coordination?")
- Finding rephrased duplicates
- Discovering unexpected connections
- Pre-ingestion duplicate check

**Use grep for:**
- Exact keyword matches
- Finding specific phrases
- Project/category lookups
- When you know the exact term

## Best Practice: Combine Both

```bash
# 1. Semantic search for broad recall
python3 scripts/sb_embed.py search "AI governance" --top-k 20 --json

# 2. Grep for exact keyword matches
grep -ri "governance" . --include="*.md" -l

# 3. Compare and deduplicate results
```

## Index Management

The index auto-updates when files are created/edited in Second_Brain/.

```bash
# Rebuild index manually (if needed)
python3 scripts/sb_embed.py index

# Force full rebuild
python3 scripts/sb_embed.py index --rebuild

# Check index health
python3 scripts/sb_embed.py stats
```

## References

- [Query Examples](references/query-examples.md) - Common search patterns
