# Verify Second Brain Agent

Verification subagent that checks files created in Second_Brain/ for compliance with templates and conventions.

## When to Invoke

After creating or editing files in `Second_Brain/`:
- New idea files (Template A)
- External reference files (Template B)
- Any file operation that should follow Second Brain conventions

## Verification Checks

### 1. Template Compliance

**For Template A (Original Thinking):**
- [ ] Has all required sections: Metadata, Summary, Classification, Project Connections, Keywords, Source, Status, Original Text
- [ ] Metadata includes: Source type, Source ID, Created date, Primary, Projects, Artifact status
- [ ] Primary category is from canonical taxonomy in CONTENT_TAXONOMY.md
- [ ] Projects are real projects from INTELLECTUAL_LANDSCAPE.md (or "None")
- [ ] Original Text section preserves exact user language

**For Template B (External References):**
- [ ] Has attribution section with Author/Speaker, Show/Platform, Date, URL
- [ ] Content is clearly marked as external (not the owner's original thinking)
- [ ] Relevance to My Thinking section explains connection
- [ ] Action Potential section present

### 2. Folder Placement

| Content Type | Correct Location |
|--------------|------------------|
| The owner's philosophy/analysis | `Journal_Intellectual/` |
| Personal reflections | `Journal_Personal/` |
| Software ideas | `Inventions/Bits/` |
| Hardware ideas | `Inventions/Atoms/` |
| Sci-fi writing | `Writing_SciFi/` |
| Other creative | `Writing_AllElse/` |
| Predictions | `Predictions/` |
| Podcast clips | `External_Sources/podcast_clips/` |
| Research refs | `External_Sources/ChatGPT_Research/` |

### 3. Keyword Quality

**Keywords should be:**
- Additive (new keywords from content are ALLOWED and encouraged)
- Distinctive (aid recall, not generic)
- Include: people, organizations, unique phrases, project names

**Keyword Guide is a growing vocabulary, not a constraint.**

### 4. Language Preservation

- User's exact words preserved in Original Text
- No paraphrasing of distinctive phrases
- Keywords match user's terminology

## Output Format

```markdown
## Verification Result

**File:** [path]
**Template:** A / B
**Status:** PASS / FAIL

### Checks
- [ ] Template sections complete
- [ ] Correct folder location
- [ ] Keywords appropriate
- [ ] Language preserved

### Issues Found (if any)
1. [Issue description]
2. [Issue description]

### Recommendation
[PASS: File is compliant]
[FAIL: Specific fixes needed]
```

## Integration

This agent can be invoked:
1. Manually after file creation
2. As part of PostToolUse hook (future enhancement)
3. By other skills that create files

## Key Principle

**Verification enables iteration.** Catching issues immediately allows for correction before the user commits changes.
