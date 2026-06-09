---
name: ingest-brain-dump
description: >-
  Full orchestrator for stream-of-consciousness input pasted or dictated into the
  Claude Code session. Pipeline: explore-second-brain (find related files) →
  semantic segmentation → verify-idea (dedupe check) → process-content (create
  Template A files) → validate_template.py → user approval → save.
  Use when user pastes unstructured text or dictates a voice note into chat and says
  "brain dump", "process this", "ingest this", "save this", "what should we do with this".
  One paragraph may contain 3 ideas; 5 paragraphs may be 1 idea — always semantic,
  never algorithmic chunking.
  NOT for phone inbox (use a phone-inbox ingest skill if configured).
  NOT for podcast snips (use a snip-processing skill if configured).
  NOT for bookmark exports (use a bookmarks-ingest skill if configured).
  For a LARGE existing source export (notes-app dump, chat history, voice-note archive),
  use /mine — it calibrates the agent's judgment on small batches before the bulk pass.
  Preserves the owner's exact language — no paraphrasing.
required_context_files:
  - Orientation_Docs/INTELLECTUAL_LANDSCAPE.md
  - Orientation_Docs/COGNITIVE_PROFILE.md
  - Orientation_Docs/KEYWORD_GUIDE.md
  - Orientation_Docs/CONTENT_TAXONOMY.md
  - Orientation_Docs/ORIENTATION.md
---

# Ingest Brain Dump

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`
- `Orientation_Docs/COGNITIVE_PROFILE.md`
- `Orientation_Docs/KEYWORD_GUIDE.md`
- `Orientation_Docs/CONTENT_TAXONOMY.md`
- `Orientation_Docs/ORIENTATION.md`

<!-- silent-context-load:v1 -->

Orchestrates brain dump ingestion: explore → classify → verify → create → validate.

## Quick Start

1. User provides unstructured content
2. Search Second Brain for related files
3. Separate into distinct ideas (semantic, not algorithmic)
4. For each idea: verify not duplicate → create file → validate template
5. Present approval proposal → execute approved actions

## Workflow Checklist

Copy and track:

```
- [ ] Step 1: Load context (ORIENTATION.md, KEYWORD_GUIDE.md, CONTENT_TAXONOMY.md)
- [ ] Step 2: Invoke explore-second-brain - find related files
- [ ] Step 3: Classify content semantically - identify distinct ideas
- [ ] Step 4: For each NEW_IDEA:
      - [ ] Invoke verify-idea - check duplicates
      - [ ] If NOT_FOUND: create Template A
      - [ ] Run validate_template.py - confirm compliance
- [ ] Step 5: Present approval proposal (see references/output-templates.md)
- [ ] Step 6: Execute approved actions
- [ ] Step 7: Report summary
```

## Critical Principles

1. **SEMANTIC SEPARATION** - Never algorithmic chunking. Identify ideas by conceptual boundaries.
2. **PRESERVE EXACT LANGUAGE** - The owner's keywords are sacred. No paraphrasing.
3. **VERIFY BEFORE CREATE** - Always check for duplicates first.
4. **VALIDATE AFTER CREATE** - Run template validation on every new file.

## Content Classification

Identify type for each segment:

| Type         | Action                                       |
|--------------|----------------------------------------------|
| NEW_IDEA     | Create Template A in Second_Brain/[Category]/ |
| TODO         | Add to project TODO file                     |
| AUGMENT      | Propose addition to existing file            |
| PREDICTION   | Create in Predictions/                       |
| READING_LIST | Add to AA_Lists/READING_LIST.md              |
| QUESTION     | Log only, don't create file                  |

See [references/routing-rules.md](references/routing-rules.md) for full routing table.

## Source Detection

| Source                          | Template |
|---------------------------------|----------|
| Claude Code conversation        | A (owner's words THIS conversation) |
| Voice dictation / voice notes   | A (owner's words only) |
| External podcast / bookmark     | B (external content, attribute)     |

## Verification Step

After creating any file, validate:

```bash
python3 .claude/scripts/validate_template.py "[filepath]"
```

If invalid: fix issues immediately. Only proceed when all files pass.

## Approval Proposal

See [references/output-templates.md](references/output-templates.md) for format.

Present each idea with:
- Proposed path
- Keywords
- Project connections
- Y/N prompt

Wait for explicit approval before creating files.

## Integration

| Skill                  | When                                 |
|------------------------|--------------------------------------|
| `explore-second-brain` | Step 2 - find related files          |
| `verify-idea`          | Step 4 - check duplicates            |
| `process-content`      | Create Template A (if needed)        |
| `extract-todo`         | Route TODOs to project files         |

## Tier 2 Dependencies

Load before processing:
- `ORIENTATION.md` - Templates, golden rules
- `KEYWORD_GUIDE.md` - Vocabulary reference
- `CONTENT_TAXONOMY.md` - Categories, folder mappings
