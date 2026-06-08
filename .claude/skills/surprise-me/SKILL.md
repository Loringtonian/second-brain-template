---
name: surprise-me
description: Surfaces random ideas from the Second Brain for serendipitous rediscovery. Combats the "you can't find what you don't know to search for" problem. Invoke with /surprise-me or when user wants to browse ideas without specific keywords.
allowed-tools: Bash, Read, Glob
---

# Surprise Me

Surfaces random ideas from the Second Brain for serendipitous rediscovery.

## Purpose

With grep-based search, you can only find what you know to look for. This skill brings back the browsability and serendipity of the old index system - helping you stumble upon ideas you forgot you had.

## Trigger Conditions

Activate when user says:
- "surprise me"
- "random ideas"
- "what have I forgotten"
- "show me something random"
- "browse ideas"
- "I don't know what to search for"

## Quick Start

1. Get random files from Second_Brain content folders
2. Exclude admin files (ORIENTATION.md, TODO_*.md, etc.)
3. Read each file's Summary, Keywords, and Project Connections
4. Present in digestible format
5. Offer to dive deeper on any that spark interest

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| count | 3 | Number of random ideas to surface |
| category | all | Filter by folder (inventions, journal, writing, predictions, etc.) |
| project | none | Filter by project connection |

## Process

### Step 1: Select Random Files

```bash
# Get random content files (excluding admin/orientation docs)
find "$SECOND_BRAIN_ROOT" -name "*.md" -type f \
  ! -name "ORIENTATION.md" \
  ! -name "TODO_*.md" \
  ! -name "README.md" \
  ! -name "*_INDEX.md" \
  ! -name "*_SPEC.md" \
  ! -name "*_TRACKER.md" \
  ! -path "*/Orientation_Docs/*" \
  ! -path "*/Archive/*" \
  ! -path "*/.obsidian/*" \
  | shuf -n [count]
```

**With category filter:**
```bash
# Example: inventions only
find "$SECOND_BRAIN_ROOT/Inventions" -name "*.md" -type f \
  ! -name "ORIENTATION.md" ! -name "TODO_*.md" ! -name "README.md" \
  | shuf -n [count]
```

### Step 2: Extract Key Info

For each file, read and extract:
- **Title** (from # heading)
- **Summary** (from ## Summary section)
- **Keywords** (from ## Keywords section)
- **Project Connections** (from ## Project Connections section)
- **Status** (Nugget/Plan/Active/Archived)

### Step 3: Present Results

```markdown
## 🎲 Random Ideas from Your Second Brain

### 1. [Title]
**Status:** [status] | **Folder:** [category]
**Summary:** [2-3 sentences]
**Keywords:** [keyword list]
**Projects:** [connections or "None"]

---

### 2. [Title]
...

---

### 3. [Title]
...

---

**Want more?** Say "more" or "another 3"
**Interested in one?** Say "tell me more about #2" to see full content
**Filter?** Say "surprise me with inventions" or "random predictions"
```

## Category Mappings

| User Says | Folder Path |
|-----------|-------------|
| inventions, ideas, startups | Inventions/ |
| journal, intellectual, philosophy | Journal_Intellectual/ |
| personal, diary | Journal_Personal/ |
| writing, scifi, stories | Writing_SciFi/ |
| predictions, forecasts | Predictions/ |
| external, podcast clips, bookmarks | External_Sources/ |
| health | Health/ |

## Follow-up Actions

When user expresses interest in an idea:
- **"tell me more about #N"** → Read and present full file
- **"connect this to..."** → Invoke connection-finder skill
- **"develop this"** → Invoke project-tracker skill
- **"more like this"** → Search for files with similar keywords

## Example Invocations

**Basic:**
> /surprise-me

**With count:**
> /surprise-me 5

**With category:**
> surprise me with some inventions
> random predictions
> show me forgotten journal entries

**Deep dive:**
> tell me more about #2
> expand on the first one

## Philosophy

The goal is rediscovery and serendipity. The Second Brain has 15+ years of thinking - ideas that were exciting once but got buried. This skill helps those ideas resurface at unexpected moments, potentially connecting to current work in ways you wouldn't have searched for.

"The best ideas are often the ones you forgot you had."
