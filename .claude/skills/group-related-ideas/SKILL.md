---
name: group-related-ideas
description: Handles connections between related ideas. Options include creating folders, adding shared keywords, merging content, or rejecting false positives. Used when ingest-brain-dump identifies related content.
required_context_files:
  - Orientation_Docs/INTELLECTUAL_LANDSCAPE.md
  - Orientation_Docs/CONTENT_TAXONOMY.md
  - Orientation_Docs/KEYWORD_GUIDE.md
---

# Group Related Ideas

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md`
- `Orientation_Docs/CONTENT_TAXONOMY.md`
- `Orientation_Docs/KEYWORD_GUIDE.md`

<!-- silent-context-load:v1 -->

Manages connections between ideas that share concepts, themes, or keywords. Provides multiple strategies for linking related content.

## Trigger Conditions

Called by `ingest-brain-dump` when:
- New idea overlaps with existing Second Brain content
- Multiple ideas in same brain dump are related
- User explicitly asks to connect ideas

Can also be invoked directly with `/group-related-ideas`.

## Required Context (Tier 2 Dependencies)

Before grouping ideas, ensure access to:

1. **SECOND_BRAIN_MASTER_INDEX.md** - Folder structure documentation (Tier 1, likely already loaded)
2. **KEYWORD_GUIDE.md** - For shared keyword identification

## Strategies

### [F] Folder - Create Shared Folder

When ideas form a coherent cluster that deserves its own namespace:

```
1. Create new folder in [Category]/[Topic]/
2. Move both files into folder
3. Add folder-level README if warranted
```

**Use when:** 3+ related ideas, clear shared theme, likely to grow

### [K] Keywords - Add Shared Keywords

When ideas are related but should remain separate files:

```
1. Identify shared keywords
2. Add keywords to both files' Keywords section
3. Update KEYWORD_GUIDE.md if new keywords
4. Connection is now searchable
```

**Use when:** Conceptual overlap, different enough to stay separate

### [M] Merge - Combine Into One File

When new content belongs in existing file:

```
1. Read existing file
2. Identify where new content fits
3. Add new content with date marker
4. Preserve all existing keywords, add new ones
5. Update file
```

**Use when:** New content is clearly part of existing idea

### [R] Reject - No Connection

When apparent relationship is superficial:

```
1. Do not create connection
2. Proceed with separate handling
```

**Use when:** False positive from keyword matching

## Process

### Step 1: Analyze Relationship

```
- What keywords do they share?
- Are they the same idea expressed differently? (→ Merge or Reject as duplicate)
- Are they distinct ideas in same domain? (→ Keywords or Folder)
- Is one an extension of the other? (→ Merge)
- Are they only tangentially related? (→ Reject)
```

### Step 2: Present Options

```markdown
## Related Ideas Detected

**Idea 1:** [title/summary]
**Idea 2:** [title/summary or existing file path]

**Relationship:** [keyword overlap / conceptual similarity / same project]
**Shared Keywords:** [list]

**Options:**
- [F] Create folder: `[Category]/[Proposed Name]/`
- [K] Add shared keywords: `[keyword1]`, `[keyword2]`
- [M] Merge into: `[existing file path]`
- [R] Reject (no meaningful connection)

**Recommendation:** [F/K/M/R] because [reason]
```

### Step 3: Execute Chosen Strategy

Based on user selection, execute the appropriate strategy from above.

### Step 4: Sync (if needed)

If folder structure changed significantly:
- Run `/sync-orientation-docs` to update documentation

## Key Rules

1. **Keywords are the primary connection mechanism** - Ideas don't need to be in same file/folder to be connected
2. **Don't over-merge** - Separate ideas that happen to be related should stay separate
3. **Folder creation is significant** - Only when cluster is clear and will grow
4. **Preserve both ideas' integrity** - Merging should enhance, not erase

## Integration

Called by: `ingest-brain-dump` (Step 3 - Handle RELATED_GROUP)
Works with: `verify-idea` (duplicate detection)
