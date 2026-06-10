---
name: process-content
description: >-
  Low-level mechanic that turns raw text into Template A/B files.
  Segments semantically (never algorithmic chunking), classifies each segment,
  creates files, runs validate_template.py. Does NOT sync from external sources —
  text must already be in context.
  Called by the ingestion skills (e.g. /ingest-example) as their file-creation stage;
  can also be invoked directly when user pastes content and says
  "make files from this", "turn this into Template A", "parse this into ideas".
  NOT for voice/phone inbox work (use an inbox-ingest skill),
  NOT for searching the brain (use explore-second-brain or semantic-search).
  If input has multiple distinct ideas, all are processed in one invocation.
required_context_files:
  - Orientation_Docs/INTELLECTUAL_LANDSCAPE.md
  - Orientation_Docs/KEYWORD_GUIDE.md
  - Orientation_Docs/CONTENT_TAXONOMY.md
  - Orientation_Docs/ORIENTATION.md
---

# Process Content

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`
- `Orientation_Docs/KEYWORD_GUIDE.md`
- `Orientation_Docs/CONTENT_TAXONOMY.md`
- `Orientation_Docs/ORIENTATION.md`

<!-- silent-context-load:v1 -->

Converts raw input → classified segments → Template A/B files.

## Quick Start

1. Explore Second Brain for related content
2. Identify distinct ideas (semantic, not algorithmic)
3. Classify each: NEW_IDEA, TODO, PREDICTION, READING_LIST, etc.
4. Create Template A for each idea
5. **Verify** before saving
6. Present for approval

## Workflow Checklist

```
- [ ] Step 1: Invoke explore-second-brain to find related files
- [ ] Step 2: Read ORIENTATION.md, CONTENT_TAXONOMY.md, KEYWORD_GUIDE.md
- [ ] Step 3: Identify distinct ideas by conceptual boundaries
- [ ] Step 4: Classify each segment (see references/classification-rules.md)
- [ ] Step 5: Create Template A for each (see references/template-format.md)
- [ ] Step 6: **Verify** - run validate_template.py on each
- [ ] Step 7: Present for approval, wait for Y/N
- [ ] Step 8: Save approved files
```

## Critical Rules

1. **SEMANTIC, NOT ALGORITHMIC** - Never chunk by paragraph or word count. One paragraph may have 3 ideas; 5 paragraphs may be 1 idea.
2. **PRESERVE EXACT LANGUAGE** - User's keywords are sacred. Never paraphrase.
3. **WATCH FOR NESTED IDEAS** - A single sentence can hold more than one idea — e.g. a philosophical stance AND a prediction, or an invention AND a TODO. Split them.
4. **VERIFY BEFORE SAVE** - No files created until validation passes.

## Segment Types (Quick Reference)

| Type | Destination |
|------|-------------|
| NEW_IDEA | [Category]/ |
| TODO | Project TODO files |
| PREDICTION | Predictions/ |
| READING_LIST | AA_Lists/ |
| AUGMENT | Add to existing file |

See [references/classification-rules.md](references/classification-rules.md) for full decision tree.

## Source → Template

| Source | Template |
|--------|----------|
| Claude Code / ChatGPT / Gmail voice | Template A (original thinking) |
| Podcast clips / Bookmarks | Template B (external, attribute) |

## Verification

After creating each Template A:

```bash
python3 .claude/scripts/validate_template.py [filepath]
```

Required sections: Metadata, Summary, Classification, Keywords, Source, Status, Original Text

If validation fails, fix issues before presenting for approval.

## References

- [Classification Rules](references/classification-rules.md) - Segment types, decision tree, boundaries
- [Template Format](references/template-format.md) - Template A structure, output format
