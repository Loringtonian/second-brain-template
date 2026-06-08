---
name: extract-todo
description: Extracts action items from content and routes to project-specific TODO files. Used by ingest-brain-dump when TODOs are identified in brain dumps.
---

# Extract TODO

Identifies and extracts action items from content, formats them properly, and routes to the appropriate project TODO file.

## Trigger Conditions

Called by `ingest-brain-dump` when content contains action items. Can also be invoked directly with `/extract-todo`.

## Required Context (Tier 2 Dependencies)

Before extracting TODOs, ensure access to:

1. **INTELLECTUAL_LANDSCAPE.md** - Project list for routing TODOs (Tier 1, likely already loaded)
2. **TODO_MASTER.md** - Routing hub for project TODO files

## Input

Content containing one or more action items (explicit or implicit).

## Process

### Step 1: Identify Action Items

Look for:
- Explicit: "I need to...", "TODO:", "Remember to...", "Don't forget..."
- Imperative: "Build X", "Create Y", "Research Z"
- Future intent: "I should...", "I want to...", "I will..."
- Questions that imply action: "How do I...?" → Research task

### Step 2: Determine Project TODO File

Route each TODO to the appropriate project's folder (TODOs are now distributed).

<!-- __FILL_FROM_USER__:todo_routing_table
     Add a row for each active project area in your Second Brain.
     Pattern: | Content Type | `Projects/[Name]/TODO_[Name].md` |
     Keep the catch-all rows at the bottom. Example shape below. -->

| Content Type | Location |
|--------------|----------|
| __FILL_FROM_USER__:project_1 related | `Projects/__FILL_FROM_USER__:project_1/TODO___FILL_FROM_USER__:project_1.md` |
| __FILL_FROM_USER__:project_2 related | `Projects/__FILL_FROM_USER__:project_2/TODO___FILL_FROM_USER__:project_2.md` |
| Database/Second Brain work | `Orientation_Docs/TODO_Second_Brain.md` |
| Inventions (Bits/Atoms) | `Inventions/TODO_Inventions.md` |
| Personal tasks/Habits/Learning | `Journal_Personal/TODO_Personal_Effectiveness.md` |
| Other writing | `Writing_AllElse/TODO_Writing_Other.md` |
| General/unclear | `Orientation_Docs/TODO_Miscellaneous.md` |

### Step 3: Format Entry

```markdown
- [ ] [Action item text] (Source: [date or brain dump ref])
```

### Step 4: Add to Project TODO File

Add directly to the appropriate file in the project's folder (see Step 2 for locations).

Find the appropriate section within that file and add the item.

### Step 5: Return Summary

```markdown
## TODO Extracted

**Action:** [brief description]
**Project:** [project name]
**Added to:** Project_TODOs/TODO_[Project].md
```

## Key Rules

1. **Preserve exact language** - Don't paraphrase the user's intent
2. **One TODO per line** - Split compound tasks if needed
3. **Include source reference** - For traceability
4. **Route to correct project file** - Based on project/category

## Example

**Input:** "I need to research a researcher's work on a topic and reach out to them about a project idea"

**Output:**
```markdown
- [ ] Research [researcher]'s work on [topic] (Source: Dec 25 brain dump)
- [ ] Draft outreach message to [researcher] about [project concept] (Source: Dec 25 brain dump)
```

Added to: `Projects/__FILL_FROM_USER__:project_name/TODO___FILL_FROM_USER__:project_name.md` → Outreach section

## Project TODO Files (Distributed)

TODOs now live in their project folders. Populate this list to match your routing table above:

<!-- __FILL_FROM_USER__:project_todo_list
     One bullet per active project area. Pattern: `Projects/[Name]/TODO_[Name].md` - description -->
- `__FILL_FROM_USER__:project_1_todo_path` - __FILL_FROM_USER__:project_1_description
- `__FILL_FROM_USER__:project_2_todo_path` - __FILL_FROM_USER__:project_2_description
- `Orientation_Docs/TODO_Second_Brain.md` - Database work (meta)
- `Inventions/TODO_Inventions.md` - Bits + Atoms ideas
- `Journal_Personal/TODO_Personal_Effectiveness.md` - Habits, learning, skills
- `Writing_AllElse/TODO_Writing_Other.md` - Other creative writing
- `Orientation_Docs/TODO_Miscellaneous.md` - Uncategorized

## Integration

Called by: `ingest-brain-dump` (Step 3 - Route TODOs)
