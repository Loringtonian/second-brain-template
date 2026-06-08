---
name: project-tracker
description: >-
  Helps you finish projects. Auto-activates when the conversation mentions any
  project registered in Orientation_Docs/INTELLECTUAL_LANDSCAPE.md — that is the
  authoritative active-project roster; pull live status from STATE_OF_SECOND_BRAIN.md.
  High-signal triggers include whatever active projects you have listed there.
  Also activates on common variations and shorthand names for those projects.
  Surfaces current state + last-touched + blockers + single next action, using
  FINISHING_FRAMEWORK.md.
  Archived projects — only activate when user asks by name.
  Philosophy: ship things, not perfect things — one concrete next action at a time.
allowed-tools: Read, Grep, Glob
required_context_files:
  - Orientation_Docs/STATE_OF_SECOND_BRAIN.md
  - Orientation_Docs/INTELLECTUAL_LANDSCAPE.md
  - Orientation_Docs/TODO_Second_Brain.md
---

# Project Tracker

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/STATE_OF_SECOND_BRAIN.md`
- `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`
- `Orientation_Docs/TODO_Second_Brain.md`

<!-- silent-context-load:v1 -->

This skill helps you finish projects. Many builders are good at starting; the hard part is delivery.

## Trigger Conditions

Activate when the conversation mentions any ACTIVE project listed in `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`.

Populate your active project list from that file. Common categories include:
- **Knowledge management** — this Second Brain itself
- **Writing / creative** — anthologies, essays, fiction, posts
- **Software tools** — productivity apps, personal servers, pipelines
- **Research / frameworks** — governance, networks, databases
- **Online presence** — website, social personas
- **Hardware / physical** — anything built with hands

Also activate on shorthand or variations of those project names.

**Archived projects** — only activate if user explicitly asks by name.

## Required Context (Tier 2 Dependencies)

Before tracking projects, read:

1. **TODO_MASTER.md** - Task routing hub, links to project TODOs
2. **INTELLECTUAL_LANDSCAPE.md** - Project details (likely already loaded)

Load the relevant project's TODO file from its folder if one exists (e.g., `<ProjectFolder>/<ProjectName>/TODO_<ProjectName>.md`).

## When Activated

### 1. Surface Context

Read the relevant section from:
- `$SECOND_BRAIN_ROOT/Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`

Check for related action items in:
- `$SECOND_BRAIN_ROOT/Orientation_Docs/TODO_MASTER.md`

> `$SECOND_BRAIN_ROOT` = the root of this repository. Use repo-relative paths when calling Read/Grep.

Search for related ideas using grep:
- Consult SECOND_BRAIN_MASTER_INDEX.md for folder structure
- Use grep to search the brain root

### 2. Identify Status

Report briefly:
- What's the current state of this project?
- What was last worked on?
- What's blocking progress (if anything)?

### 3. Suggest Next Steps

Using the [FINISHING_FRAMEWORK.md](FINISHING_FRAMEWORK.md):
- Identify the smallest shippable piece
- Suggest the single next action
- Flag if something needs external input or is blocked

### 4. Accountability Check

If the project seems stuck:
- When was this last touched?
- Why is it stuck?
- Should it be archived, deprioritized, or pushed forward?

## Output Format

Keep it brief (2-3 sentences per section). Expand only if asked.

Example output:
```
**<Project Name> Status:** <N> stories drafted, <N> need revision. Last touched: <description>.

**Blockers:** None identified - ready for next story or revision pass.

**Next step:** Pick one: revise "<item>" OR draft <next item> from the list.
```

## Philosophy

The goal is to help you **ship things**. Not perfect things - shipped things. Break big projects into small pieces. One concrete next action at a time.

See [FINISHING_FRAMEWORK.md](FINISHING_FRAMEWORK.md) for the full approach.
