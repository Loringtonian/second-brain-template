# Search Strategy

How to efficiently search the Second Brain for relevant connections.

## Folder Structure (reference)

```
$SECOND_BRAIN_ROOT/
├── Orientation_Docs/        # Central docs (INTELLECTUAL_LANDSCAPE, KEYWORD_GUIDE, etc.)
├── External_Sources/        # __FILL_FROM_USER__:external_source_subfolders
├── Journal_Intellectual/    # Philosophy, AI analysis, intellectual explorations
├── Inventions/              # Bits/ and Atoms/ subfolders
├── Writing_SciFi/           # Speculative fiction drafts
├── Writing_AllElse/         # Essays, lyrics, other writing
├── Journal_Personal/        # Reflections, habits
├── Predictions/             # Forecasts with timelines
├── Projects/                # Active and archived projects
└── [other categories]
```

Set `$SECOND_BRAIN_ROOT` to the absolute path of your brain's root directory.

## Search Method: Grep-Based

All searching uses grep directly on the brain root. No stale indexes; 100% accuracy.

**Why grep:**
- Token-efficient (~100 tokens per search)
- Always up to date
- Zero maintenance overhead

### Basic Search Patterns

**Search for keywords:**
```bash
grep -ri "[keyword]" "$SECOND_BRAIN_ROOT" --include="*.md" -l
```

**Search for project connections:**
```bash
grep -r "**Projects:**.*[ProjectName]" "$SECOND_BRAIN_ROOT" --include="*.md"
```

**Search for people:**
```bash
grep -ri "[PersonName]" "$SECOND_BRAIN_ROOT" --include="*.md" -l
```

**Search by category:**
```bash
grep -r "**Primary:** Journal - Intellectual" "$SECOND_BRAIN_ROOT" --include="*.md"
```

## Keyword Matching

Reference `Orientation_Docs/KEYWORD_GUIDE.md` for vocabulary.

### High-Value Keywords (search these first)

Fill these with your own brain's priority terms:
- Project names: `__FILL_FROM_USER__:project_name_1`, `__FILL_FROM_USER__:project_name_2`
- Key people: `__FILL_FROM_USER__:thinker_1`, `__FILL_FROM_USER__:thinker_2`
- Core themes: `vibe coding`, `singularity`, `coordination`, `common knowledge`, `live player`

### Keyword Variations

Some keywords have multiple forms — use case-insensitive search (`grep -i`) to catch them:
- `AI` / `artificial intelligence` / `AGI`
- `__FILL_FROM_USER__:abbreviation` / `__FILL_FROM_USER__:alternate_spelling` / `__FILL_FROM_USER__:full_form`
- Adapt for your own domain vocabulary

## Advanced Search Patterns

### For Connections Between Topics
```bash
# Find files mentioning BOTH topics
grep -ril "topic1" "$SECOND_BRAIN_ROOT" | xargs grep -l "topic2"
```

### For Category-Specific Searches
```bash
# Search only Journal_Intellectual
grep -ri "concept" "$SECOND_BRAIN_ROOT/Journal_Intellectual/" --include="*.md" -l
```

## Quality Over Quantity

- Maximum 5 files read per search pass
- Stop when you have 3 good connections
- If nothing relevant, say so rather than forcing weak connections

## Example Search Flow

Owner discusses "coordination problems in AI governance"

1. Extract keywords: `coordination`, `AI`, `governance`
2. Check `KEYWORD_GUIDE.md` — maps to vocabulary in the brain (e.g., `coordination theory`, `common knowledge`)
3. Search with grep:
   ```bash
   grep -ri "coordination" "$SECOND_BRAIN_ROOT/Journal_Intellectual/" --include="*.md" -l
   ```
4. Find 2–3 relevant files
5. Read quickly for relevance
6. Report: "Your 'Common Knowledge Infrastructure' idea in Journal_Intellectual/ explores similar coordination dynamics"

---

*Grep-based search supersedes any legacy category-index approach.*
