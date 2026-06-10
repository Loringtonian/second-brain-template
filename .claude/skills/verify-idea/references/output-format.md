# Output Format

## Verification Result Template

```markdown
## Verification Result

**Idea Checked:** [title from input]
**Core Concept:** [the nugget being verified]

**Status:** DUPLICATE | OVERLAP | NOT FOUND | UNCERTAIN

### Search Performed
- Folders searched: [list]
- Terms searched: [list]
- Files examined: [count]

### Match Details (if applicable)
- **File:** [full path]
- **Similarity:** high/medium/low
- **Shared:** [what overlaps]
- **Distinct:** [what differs]

### Recommendation
- DUPLICATE → Skip, already captured at [path]
- OVERLAP → Consider merging with [path] or linking
- NOT FOUND → Safe to create new file in [category]/
- UNCERTAIN → Review these files: [list paths]
```

## Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| DUPLICATE | Exact same idea exists | Skip creation |
| OVERLAP | Related but distinct | Consider merge or link |
| NOT FOUND | No semantic match | Safe to create |
| UNCERTAIN | Possible matches | Human review needed |

## Semantic Comparison Rules

**Same idea** = same core proposal/insight, different words OK
**Different idea** = different proposal, even if similar topic

Examples:
- "Vibe coding cleanup agent" = "context janitor" = "agent that cleans failed experiments" → SAME
- "Vibe coding is growing" vs "Tools for vibe coders" → DIFFERENT (observation vs product)
- "AI will transform X" vs "AI will transform Y" → DIFFERENT (different domains)

## Common Pitfalls

- Shared keywords ≠ same idea ("AI" appears everywhere)
- Similar topic ≠ same idea (many ideas about "vibe coding")
- Different framing = same idea ("X will happen" vs "I predict X")
