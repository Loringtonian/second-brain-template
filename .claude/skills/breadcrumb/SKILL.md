---
name: breadcrumb
description: Register a discovered capability, tool, pattern, or gotcha in the right discovery layer for future Claude instances
user_invocable: true
allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Breadcrumb

Registers a newly discovered capability, tool, pattern, or gotcha so future Claude instances can find it. Places compact breadcrumbs in the right discovery layer.

## Trigger Conditions

- User says "breadcrumb", "remember this tool", "register this", "add to toolkit", "make future instances aware"
- Another skill discovers something useful and wants to persist it

## Discovery Layers

Place breadcrumbs in the layer that matches visibility needs. Higher layers = more token cost but guaranteed discovery.

| Layer               | Loaded        | Budget   | Use For                                    |
|---------------------|---------------|----------|--------------------------------------------|
| **CLAUDE.md**       | Always        | 1-5 lines | Capabilities ANY instance might need        |
| **MEMORY.md**       | Always        | 2-5 lines | Gotchas, patterns, architectural decisions  |
| **Skill SKILL.md**  | On activation | 1-3 lines | Capabilities specific to one workflow       |
| **Reference doc**   | On demand     | Unlimited | Full syntax, examples, deep reference       |

## Workflow

### Step 1: Understand the Discovery

Ask if not obvious:
- What was discovered? (tool, flag, pattern, gotcha, workaround)
- What context is it useful in? (always, specific workflow, debugging)

### Step 2: Classify Layer

Decision tree:

1. **Is it a CLI tool with JSON output?** → CLAUDE.md `CLI JSON MODES` table
2. **Is it useful across most workflows?** → CLAUDE.md (new section or existing table)
3. **Is it a gotcha/pattern from a specific system?** → MEMORY.md under the relevant section
4. **Is it specific to one skill's workflow?** → That skill's SKILL.md
5. **Does it need full examples/syntax?** → Reference doc (Tech_Tips.md, etc.)

Multiple layers are fine. Common pattern: compact breadcrumb in CLAUDE.md or MEMORY.md pointing to full reference in Tech_Tips.md.

### Step 3: Format the Breadcrumb

**CLAUDE.md**: Table row or 1-line bullet. Match existing format.
```
| tool | `--flag` | What it does |
```

**MEMORY.md**: Bullet with enough context to be useful standalone.
```
- **Pattern name**: Brief explanation. Context for when this matters.
```

**Skill SKILL.md**: Inline note near the relevant workflow step.

**Reference doc**: Full entry with install, syntax, examples.

### Step 4: Place It

- Read the target file
- Find the right insertion point (after related content, before the next section)
- Edit to add the breadcrumb
- Preserve existing formatting (table alignment, heading hierarchy)

### Step 5: Confirm

Show the user:
```
## Breadcrumb Placed

**Layer:** CLAUDE.md > CLI JSON MODES
**Added:** | tool | `--flag` | Description |
**Tokens:** ~10

[+ any additional layers]
```

## Anti-Patterns

- **Don't dump full docs into CLAUDE.md** — it's always-loaded, every line costs tokens
- **Don't duplicate existing entries** — grep first to check if it's already there
- **Don't add session-specific context** — breadcrumbs are for persistent, reusable knowledge
- **Don't breadcrumb obvious things** — `ls` lists files. We know.
- **Don't breadcrumb unverified info** — only register things confirmed to work

## Examples

### Good Breadcrumbs

**CLI tool**: "fd supports `--json` for structured file finding"
→ CLAUDE.md `CLI JSON MODES` table: `| fd | \`--json\` | Fast file finder with structured output |`

**Gotcha**: "Fly.io volumes can't be shared across machines"
→ MEMORY.md under a relevant project: `- **Fly.io only supports 1 volume per machine** — data shares the tailscale_state volume`

**Workflow-specific**: "yt-dlp `--write-info-json` saves metadata alongside downloads"
→ the relevant download-skill's SKILL.md: note near the download step

### Bad Breadcrumbs

- Entire man page dumped into MEMORY.md
- "Python is a programming language" in CLAUDE.md
- A fix for a one-time bug that won't recur
- Temporary workaround that should be properly fixed instead
