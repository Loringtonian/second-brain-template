---
name: explore-second-brain
description: Spawn a subagent to scan Second_Brain files and find content related to new input. Uses semantic search + grep for comprehensive results. Returns a manifest of relevant files. Use before processing new content to avoid duplicates and find related ideas.
allowed-tools: Read, Grep, Glob, Bash
required_context_files:
  - Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md
  - Orientation_Docs/CONTENT_TAXONOMY.md
---

# Explore Second Brain

> **Setup note:** the semantic-search half of this skill calls `scripts/sb_embed.py` (**not bundled** — see `SETUP.md` at the repo root); the grep half works as-is, so the skill degrades gracefully.

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md`
- `Orientation_Docs/CONTENT_TAXONOMY.md`

<!-- silent-context-load:v1 -->

Spawns a Task subagent (Sonnet 4.6) to efficiently scan existing Second_Brain files using semantic search + grep. Sonnet is required because the subagent must read the DUPLICATE/HIGHLY_RELATED files' `## Connections` sections and expand each named file into its own manifest entry — Haiku fabricates paths and duplicates entries under that load (validated via A/B testing Apr 2026).

## When to Use

Before:
- Processing new voice notes or dictation
- Creating a new idea file
- Adding content to the Second Brain
- Any operation that needs to know what already exists

## How It Works

1. Main instance spawns Task subagent (model: sonnet)
2. Subagent uses Tier 1 docs (INTELLECTUAL_LANDSCAPE.md, SECOND_BRAIN_MASTER_INDEX.md)
3. Subagent analyzes input to determine relevant search terms
4. **Subagent runs semantic search first** for broad conceptual matches
5. Subagent uses grep for exact keyword/phrase matches
6. Subagent combines and deduplicates results
7. Subagent reads candidate files
8. Subagent applies intelligence to filter for actual relevance
9. Subagent returns manifest of genuinely relevant files

## Search Strategy: Semantic + Grep

| Method | Strengths | Use For |
|--------|-----------|---------|
| **Semantic search** | Finds rephrased ideas, conceptual matches | Broad recall, duplicates |
| **Grep** | Exact matches, 100% precision | Keywords, phrases, names |

**Best practice:** Run both, combine results, deduplicate.

## Invocation

When activated, spawn a Task subagent with model: sonnet and this prompt (with the input content substituted into the `<context>` block):

---

<purpose>
You are exploring the Second Brain to find content related to a new input, before the orchestrator decides whether to create a new file, merge into an existing one, or link. Your manifest is the input the orchestrator uses to avoid duplicating existing ideas and to surface connections the author might not have annotated. Complete recall matters more than brevity — the orchestrator can discard, but cannot recover what you never surfaced.
</purpose>

<role>
Semantic + keyword searcher with taste for genuine conceptual connection, not surface keyword overlap.
</role>

<return>
Return a markdown manifest in this exact structure:

## Exploration Results

**Input Analyzed:** [one-line description]
**Search Terms Used:** [list of the semantic queries and grep patterns you ran]
**Files Found:** [count before filtering]
**Relevant Files:** [count after filtering]

### Relevant Files

#### 1. [Absolute file path]
**Relevance:** DUPLICATE | HIGHLY_RELATED | RELATED | CONTEXT_ONLY
**Why:** [1–2 sentences on the semantic connection, in your own words]
**Key Excerpt:** [verbatim quote from the file — OR, if no single quote demonstrates the connection, prefix with `CONTEXT:` followed by a short paraphrase and label the file CONTEXT_ONLY]
**Recommendation:** [one of: merge into this file / link to it / cite as context / this input is a duplicate of this file]

[repeat for every relevant file — open-ended, not capped]

### Summary
Lead with the one-word verdict (new / duplicate / expansion). Then, if the found files form a coherent pattern, add a short numbered synthesis (2–5 bullets) showing how the input connects across the files — e.g., philosophical foundation → tactical protocol → portfolio strategy. End with the most valuable next action for the orchestrator.
</return>

<approach>
Run semantic search first via `sb_embed.py` — this catches rephrased duplicates that grep would miss. Then use grep for precision on distinctive keywords, phrase fragments, and project-tag lines. Combine the two result sets, dedupe, and read each candidate file. Apply your own judgment to decide whether each candidate is actually connected to the input at the level of *shared idea*, not just *shared word*. Prefer surfacing a few too many over missing a genuine match; the orchestrator will filter. Two different kinds of connection exist — (a) the input IS a duplicate of an existing file, and (b) the input is a new idea that relates to several existing ones — and your manifest should disambiguate them.

When you identify a DUPLICATE or HIGHLY_RELATED file, read its `## Connections` section (and any `**Connections:**` / `**Projects:**` metadata lines). For each file named there, open that file, read it, and — if it meets the concrete-action bar — add it as its own numbered entry in the Relevant Files list with its own Relevance label, Key Excerpt, Why, and Recommendation. Treat each propagated file the same way you treat a hit from semantic search: a first-class candidate that earns its own slot in the manifest. Author-annotated connections are high-signal because the owner wrote them knowing the neighborhood, and they often name files that share no keywords with the input yet are genuinely related through the author's mental model.
</approach>

<examples>
<example>
Input: "I need a way to automatically sort and curate my podcast snips by topic so I can find related clips later."

Search strategy: semantic for "podcast snip curation topic clustering"; grep for "snip", "topic boundary", "curation".

Manifest excerpt:

#### 1. $SECOND_BRAIN_ROOT/Projects/Transcript_Segmenter/INTENT_SPEC.md
**Relevance:** HIGHLY_RELATED
**Why:** This project is exactly this — automatic segmentation and classification of podcast transcripts into taxonomic categories.
**Key Excerpt:** "Segment podcast transcripts into discrete ideas and classify each into the KEYWORD_GUIDE taxonomy for retrieval."
**Recommendation:** This input belongs as a TODO or use-case note on the segmenter project, not as a new file.

#### 2. $SECOND_BRAIN_ROOT/Projects/Curation_Layer/INTENT_SPEC.md
**Relevance:** RELATED
**Why:** Surfaced by propagating the `## Connections` section of the segmenter (file #1). The curation layer is directly downstream of the workflow the input describes.
**Key Excerpt:** "Sift classified snips into lanes for human triage."
**Recommendation:** Link to it from the segmenter note so the input's "find related clips later" phrase points at the right downstream tool.

### Summary
**Status:** Expansion of existing project. The segmenter project already scopes this exact workflow; the input is a feature request, not a new idea. Propagated one author-annotated connection (curation layer) that grep alone would have missed.
</example>
</examples>

<constraints>
- Search the actual file system, not your memory of the Second Brain. Structure and contents change frequently.
- Return absolute paths, not relative. Orchestrator runs in different working directories.
- Surface conceptual connections even when keyword overlap is weak. The test is "would a thoughtful human call these related?"
- Open-ended candidate list. If twelve files are genuinely relevant, return twelve.
- Quote only what the file contains verbatim. When a file is genuinely relevant but no sentence from it cleanly shows the connection, use the `CONTEXT:` paraphrase form in the Key Excerpt field and label the file CONTEXT_ONLY — this protects the orchestrator, who trusts every un-prefixed quote as copy-paste accurate.
- Every file you include must demonstrate at least one concrete semantic connection the orchestrator can act on (merge / link / cite). If the best you can say is "shares a keyword," leave it out.
- When a DUPLICATE or HIGHLY_RELATED file has a `## Connections` section, every file it names becomes its own candidate. Open each one, read it, then — for every one that meets the concrete-action bar — add it as a numbered entry in the Relevant Files list with its own Relevance label, Key Excerpt, Why, and Recommendation. A single entry summarizing or citing the Connections section of another file is not a substitute for expanding the named files as individual manifest entries. Missing an author-annotated connection is a recall failure even if semantic search alone wouldn't have surfaced it.
- If no related content meets this bar, say so in the Summary. An honest "no relevant matches" is more useful than a padded list.
</constraints>

<verify>
Before returning, confirm:
- Every file path is absolute and exists.
- Every un-prefixed `Key Excerpt` is copy-paste verbatim from the named file. Re-open each file and search for the quote string before finalizing — if a quote is paraphrased or approximate, prefix it with `CONTEXT:` and flip the relevance label to CONTEXT_ONLY.
- Relevance labels match the explanation (a file labelled DUPLICATE genuinely covers the same idea; CONTEXT_ONLY files provide background, not direct overlap).
- Every file passes the "concrete action" test: the orchestrator could merge / link / cite this, not just note the keyword overlap.
- The Summary leads with a one-word verdict and, where useful, closes with a numbered synthesis showing how the files fit together.
- You ran BOTH semantic search AND grep, not just one.
- For every DUPLICATE or HIGHLY_RELATED file in your manifest, you opened that file's `## Connections` section (if present), opened each named file, and — for every one that met the concrete-action bar — added it as its own numbered manifest entry with its own Relevance / Key Excerpt / Why / Recommendation. If none of the propagated candidates made the cut, that is fine; but the evaluation must have happened and no single entry exists whose purpose is to summarize or cite another file's Connections section.
- Every manifest entry corresponds to a file you actually opened and read during this session. Every manifest entry is one you could quote from or paraphrase with CONTEXT: because you saw the content — not one you reasoned about by filename or metadata alone.
</verify>

<done>
A manifest the orchestrator can act on without re-exploring. If the orchestrator would still need to grep after reading your manifest, the manifest isn't done.
</done>

<return>
Return the manifest exactly as specified in the `<return>` block above. End the output at the Summary line so the orchestrator can parse the manifest without stripping preamble or trailing commentary.
</return>

<context>
**Input content to explore against:**

[paste the new content being processed]

**Search infrastructure available:**

Semantic search (always run first):
```bash
python3 $SECOND_BRAIN_ROOT/scripts/sb_embed.py search "concept" --top-k 20 --json
```

Grep patterns (run after semantic):
```bash
# Files tagged with a project
grep -r "**Projects:**.*[ProjectName]" "$SECOND_BRAIN_ROOT/" --include="*.md"

# Files containing a keyword
grep -ri "[keyword]" "$SECOND_BRAIN_ROOT/" --include="*.md" -l

# Files containing a distinctive phrase
grep -ri "[phrase]" "$SECOND_BRAIN_ROOT/" --include="*.md" -l
```

**Tier 1 orientation context (read these first for project/taxonomy grounding):**

- `$SECOND_BRAIN_ROOT/Orientation_Docs/INTELLECTUAL_LANDSCAPE.md` — project list, themes, people
- `$SECOND_BRAIN_ROOT/Orientation_Docs/SECOND_BRAIN_MASTER_INDEX.md` — folder structure
- `$SECOND_BRAIN_ROOT/Orientation_Docs/KEYWORD_GUIDE.md` — vocabulary
</context>

---

## Key Principles

1. **Return COMPLETE information** - Don't truncate or summarize excessively. The main instance needs enough context to make decisions without re-reading the files.

2. **Use intelligence, not keyword matching** - Two ideas are related if they're conceptually connected, not just because they share words.

3. **Open-ended candidate list** - Find as many related files as exist. Don't limit to a fixed number.

4. **Use Sonnet for exploration** - The task is no longer pure search: Connections-propagation requires holding candidate files, reading each, evaluating against concrete-action bar, avoiding duplicates, and grounding every quote. Haiku fabricates paths under that load (validated Apr 2026).

5. **Grep is always accurate** - Unlike pre-built indexes that can be stale, grep finds current state.

## Example Task Call

```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  prompt="[full prompt from above with input content inserted]"
)
```

## Search Patterns Reference

| To Find | Grep Pattern |
|---------|-------------|
| Files in a project | `grep -r "**Projects:**.*ProjectName"` |
| Files with keyword | `grep -ri "keyword"` |
| Files by category | `grep -r "**Primary:** Journal - Intellectual"` |
| Files mentioning person | `grep -ri "PersonName"` |
| Files with connections | `grep -r "**Connections:**.*[FileName]"` |
