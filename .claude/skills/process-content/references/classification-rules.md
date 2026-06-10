# Classification Rules

## Segment Types

| Type | Description | Destination |
|------|-------------|-------------|
| `NEW_IDEA` | Novel concept worth storing | [Category]/ |
| `TODO` | Action item, task | Project TODO files |
| `AUGMENT` | Addition to existing idea | Propose addition to existing file |
| `PREDICTION` | Forecast with timeline | Predictions/ |
| `READING_LIST` | Book/article/podcast | AA_Lists/ |
| `QUESTION` | Rhetorical/literal question | Log only |
| `OBSERVATION` | Ephemeral thought | Evaluate for storage value |

## Decision Tree

```
0. Does it belong to an active project with its own folder?
   - Yes → Route to project folder (Projects/[Name]/), not category folder
   - No → Continue to step 1

1. Is it actionable?
   - Yes + specific task → TODO (route to project TODO file)
   - Yes + "should read/watch" → READING_LIST

2. Is it predictive?
   - References future + timeline → PREDICTION

3. Does it extend existing content?
   - Mentions existing project/idea → AUGMENT

4. Is it a novel concept?
   - New idea with storage value → NEW_IDEA
   - Fleeting thought → OBSERVATION
```

**Adjacency warning:** When processing multi-idea voice notes, assign project connections per-idea based on content, not based on what other ideas appeared in the same recording.

## Source → Template Mapping

| Source | Template | Key Rules |
|--------|----------|-----------|
| Claude Code conversation | Template A | User's words = original thinking |
| ChatGPT dictation | Template A | Mine ONLY user inputs, not AI |
| Gmail voice notes | Template A | SuperWhisper = user's voice |
| Podcast clips | Template B | EXTERNAL, attribute speaker |
| X.com bookmarks | Template B | Other people's content |

## Category Routing (for NEW_IDEA)

| Category | Use When |
|----------|----------|
| Journal_Intellectual | Philosophy, frameworks, AI analysis |
| Journal_Personal | Personal reflections, feelings |
| Inventions/Bits | Software, SaaS ideas |
| Inventions/Atoms | Hardware, physical products |
| Writing_SciFi | Sci-fi / speculative fiction, story concepts |
| Writing_AllElse | Activism, lyrics, creative |
| Predictions | Explicit forecasts with timelines |
| Health | Wellness, nutrition, biohacking |

## Boundary Detection

Signs of idea boundaries:
- Topic shifts
- "Another thing..." / "Also..." / "Oh and..."
- Time/context markers ("Today I..." / "Just realized...")
- Category changes (philosophy → product idea)
- Nested ideas (philosophical stance + prediction in same paragraph)

**CRITICAL:** Use SEMANTIC understanding, not algorithmic chunking. A paragraph may contain 3 ideas. 5 paragraphs may be 1 idea.
