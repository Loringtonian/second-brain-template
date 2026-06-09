# ORIENTATION - Procedures & Templates
*Second Brain Project*
*Version: template | Last Updated: `__FILL_FROM_USER__:last_updated`*

> **Purpose:** Procedures, templates, golden rules, and sync triggers for creating/processing files.
> **This is NOT a status dashboard.** For current state, phase, projects, tier roster → STATE_OF_SECOND_BRAIN.md.
> **For context (WHY):** INTELLECTUAL_LANDSCAPE_LITE.md auto-loads every session (Tier 0). Full INTELLECTUAL_LANDSCAPE.md loads via ROUTER.md Tier 2 rules.
> **For classification:** See CONTENT_TAXONOMY.md
> **For boundaries:** See CLAUDE.md
> **For structure:** See SECOND_BRAIN_MASTER_INDEX.md
> **For silent context loading rules:** See ROUTER.md (the only orientation doc auto-imported into CLAUDE.md)

---

## GOLDEN RULES

1. **NEVER modify original files** - Work only inside the brain's content roots
2. **PRESERVE EXACT LANGUAGE** - The owner's keywords are sacred for memory retrieval. **NO PARAPHRASING.** Use the owner's actual words and phrases. Do not "improve," expand, or rephrase. If the original says "vibe coding," write "vibe coding" - not "intuitive AI-assisted development."
3. **NEVER RENAME FILES OR FOLDERS** - The owner's recall is keyword-based. Renaming breaks recall. Use original names exactly, including spaces and capitalization. If copying "Misc Links and Things/", the copy must be named "Misc Links and Things/", not "Misc_Links/" or any variation.
4. **MAINTAIN ATTRIBUTION** - External ideas stay external. If an idea came from a podcast, tweet, or article, it is NOT the owner's idea even if they wrote about it. Use Template B with full attribution. Only the owner's RESPONSE or INSIGHT about external content is theirs.
5. **CHECK AUTHORITATIVE SOURCES FIRST** - Organized folders have more developed content than raw transcripts
6. **DEDUPLICATE AGGRESSIVELY** - Merge similar ideas, keep most complete version

---

## THREE CATEGORIES OF CONTENT

### ORIGINAL THINKING (The Owner's Ideas) → Template A
Sources where the owner is the author (`__FILL_FROM_USER__:original_thinking_sources`), e.g.:
- **Voice dictations** - Brain dumps, ideas at point of utterance
- **Voice notes** - Speech-to-text transcriptions, stream of consciousness
- **A daily-writing practice** - Daily voice/text transcripts
- **Original notes folders** - Journal, Inventions, Writing (authoritative)

### EXTERNAL REFERENCES (Other People's Content) → Template B
Sources that inform/relate to the owner's thinking but aren't their ideas, e.g.:
- **Bookmarks** - Other people's posts/tweets
- **Podcast snips** - Other people's ideas from podcasts
- **Forwarded content** - "Watch this," "Read this" notes

**DESTINATION:** External content goes in `External_Sources/`, NOT mixed with the owner's original thinking. Subfolders by source type (e.g., `X_Bookmarks/`, `Podcasts/`).

**CRITICAL:** Watch for podcast-triggered ideas! Look for "I was listening to..." - these are ORIGINAL THINKING inspired by external content. Use Template A.

### AI SYNTHESIS (AI-Generated Publishable Content) → Template C
Content where AI synthesizes, develops, or articulates the owner's existing ideas into publishable form:
- Essays and analyses
- Developed frameworks
- Polished articles

**KEY DISTINCTION:** Template C is NOT the owner's raw words (Template A) and NOT someone else's content (Template B). It is AI synthesis OF the owner's intellectual world.

**REVIEW STATUS:** All Template C files start as `Unread`. The owner marks them `Approved` after reading and editing. Unapproved files should not be treated as authoritative.

**NOT TEMPLATE C:** Internal docs (orientation, validators, classification rules). Template C is for publishable writing only.

**DESTINATION:** `Written_By_AI/`

**FOLDER NAME:** "Written_By_AI" — transparency is the point. This is not the owner's writing; it is AI writing based on the owner's thinking.

---

## MINING WORKFLOW

> **Large source export?** Calibrate first. Run the `/mine` calibration loop — batches of 10 → the
> owner corrects → write each fix back into the rules → repeat until a batch is clean → then bulk-process.
> Full procedure: `Orientation_Docs/MINING.md`. The steps below are the per-item mechanics that loop uses.

1. **Confirm INTELLECTUAL_LANDSCAPE context** - INTELLECTUAL_LANDSCAPE_LITE.md is auto-loaded (Tier 0); the full INTELLECTUAL_LANDSCAPE.md loads via ROUTER.md Tier 2 for deep work. If you're mining, you're in Tier 2 — the full file should already be in your context.
2. **Read CONTENT_TAXONOMY.md** - Understand source hierarchy and idea categories
3. **Check SECOND_BRAIN_MASTER_INDEX.md** - Understand folder structure
4. **Check KEYWORD_GUIDE.md** - Use existing keywords, note new ones
5. **Use grep for duplicate checking** - Search the brain directly (100% accuracy)
6. **Extract ideas** - Preserve exact language, add keywords
7. **Output FULL Template A** - Template A IS the artifact. NEVER summarize. Every artifact must be presented as complete Template A, not as a table or brief description.
8. **Update KEYWORD_GUIDE.md** - Add significant new keywords discovered
9. **Update the maintenance/tracking log** - Log your work
10. **Update TODO_MASTER.md** - Add any action items found

---

## CONVENTIONS (Canonical)

### Metadata (required)

All new artifacts MUST include a `## Metadata` section. This is plain text (no YAML) so it's easy for both humans and agents.

**Minimum required fields:**
- **Source type:** Dictation / Voice Note / Daily Journal / Original Notes / Podcast clip / Bookmark / Web Scrap / AI Synthesis / Other
- **Source ID:** filename, conversation ID (e.g., `C-2143`), email ID, snip timestamp, URL, etc.
- **Created date:** when the source was created (or published for external content)
- **Primary:** one canonical taxonomy category (see below)
- **Projects:** comma-separated list of real projects from `INTELLECTUAL_LANDSCAPE.md` (or `None`)
- **Artifact status:** see status enum below

Optional but encouraged:
- **Inspiration source:** for "I was listening to…" style triggers
- **Key people:** when notable

### Status enums (use consistently)

**Artifact status** (for the idea/reference itself):
- `Nugget` | `Plan` | `Active` | `Archived` | `ReferenceOnly`

**Processing status** (for trackers/queues, not the idea itself):
- `PENDING` | `IN_PROGRESS` | `IN_REVIEW` | `COMPLETE` | `SKIPPED` | `ARCHIVED`

### Timezone

**All timestamps: the owner's local timezone (`__FILL_FROM_USER__:timezone` — e.g. `America/New_York` or `UTC`).** Scripts use `from tz import now as tz_now` (see `scripts/tz.py`). Label timestamps with the zone.

### Privacy depth (frontmatter)

Every file also carries a one-line YAML **`depth: N`** (1–5) frontmatter — its privacy/disclosure level (1 = public … 5 = sealed). It gates what agents auto-load and what you publish (ship ≤2, review 3, keep 4–5 private). See `Orientation_Docs/PRIVACY_DEPTH.md` for the rubric; stamp with `scripts/stamp_depth.py <file> <N>`.

---

## TEMPLATE A IS THE ARTIFACT (CRITICAL)

**Override default Claude behavior:** Your base training says to be concise and summarize. FOR INGESTION WORK, that instinct is WRONG when dealing with Template A.

- Template A = the actual file that gets saved
- Summarizing Template A = losing fidelity, making editorial decisions that aren't yours
- When presenting artifacts for review: FULL Template A, always
- When agents output artifacts: FULL Template A, always
- When processing autonomously: FULL Template A, always

**Never:** "Here's a summary of the 3 files..."
**Always:** "Here is the full Template A for each file: [complete content]"

---

## TEMPLATE A: ORIGINAL THINKING (The Owner's Ideas)

```markdown
# [Idea Title]

## Metadata
**Source type:** [Dictation / Voice Note / Daily Journal / Original Notes / Other]
**Source ID:** [Filename or conversation ID]
**Created date:** [When created]
**Primary:** [From canonical taxonomy below]
**Projects:** [Comma-separated project list from INTELLECTUAL_LANDSCAPE.md, or None]
**Artifact status:** [Nugget / Plan / Active / Archived / ReferenceOnly]
**Processed:** Phase [N] Batch [B] | [YYYY-MM-DD]

## Summary
[Core concept in the owner's exact words - 2-3 sentences]

## Classification
**Primary:** [From canonical taxonomy below]
**Secondary:** [If applicable]

## Project Connections
[From INTELLECTUAL_LANDSCAPE.md projects - or "None - General Reference"]

## Keywords
[No artificial limits - as many as appropriate for the content]
[Include: unique words, unique ideas, people, organizations, project names]

## Source
**Type:** [Dictation / Voice Note / Daily Journal / Original Notes]
**File:** [Filename or conversation ID]
**Date:** [When created]

## Status
[Nugget / Plan / Active / Archived / ReferenceOnly]

## Inspiration Source (if applicable)
[If triggered by podcast/article/conversation - note what inspired it]
[Look for phrases like "I was listening to..." at the start]

---

## Original Text
[Preserved source material - never modified]
```

---

## TEMPLATE B: EXTERNAL REFERENCE (Other People's Content)

```markdown
# [Reference Title]

## Metadata
**Source type:** [Podcast clip / Bookmark / Forward / Web Scrap / Other]
**Source ID:** [URL, snip link+timestamp, filename, etc.]
**Created date:** [Original publish date]
**Primary:** [From canonical taxonomy below]
**Projects:** [Comma-separated project list from INTELLECTUAL_LANDSCAPE.md, or None]
**Artifact status:** [ReferenceOnly / Archived / Active]
**Processed:** Phase [N] Batch [B] | [YYYY-MM-DD]

## Source
**Type:** [Podcast clip / Bookmark / Forward / Other]
**Author/Speaker:** [Who created this content]
**Show/Platform:** [Podcast name, platform, etc.]
**Date:** [Original publish date]
**URL/Link:** [If available]

## Content
[Preserved original text/transcript - with attribution]

## Core Insight
[1-2 sentence distillation of the key idea]

## Relevance to My Thinking
[How this relates to, informs, or progresses the owner's existing ideas]
- **Connects to:** [Specific ideas/projects this relates to]
- **Complements:** [What existing thinking this supports]
- **Challenges:** [What it contradicts or complicates, if any]

## Keywords
[No artificial limits - as many as appropriate]
[Include: topics, people mentioned, organizations, themes]

## Classification
**Primary:** [From canonical taxonomy below]

## Action Potential
[Tweet material / Essay expansion / Speculative-fiction seed / Business idea / None - pure reference]

---

## Attribution
[Full attribution to original creator - required]
```

---

## TEMPLATE C: AI SYNTHESIS (AI-Generated Publishable Content)

```markdown
# [Title]

## Metadata
**Source type:** AI Synthesis
**Generated by:** [Model, e.g., Claude Opus]
**Generated date:** [YYYY-MM-DD]
**Review status:** Unread
**Primary:** [From canonical taxonomy below]
**Projects:** [From INTELLECTUAL_LANDSCAPE.md, or None]
**Artifact status:** [Draft / Active / Archived]
**Processed:** Template C | [YYYY-MM-DD]

## Summary
[Core thesis in 2-3 sentences]

## Source Material
- `[path/to/file.md]` - [what was drawn from it]

---

## Synthesized Text
[The AI-generated content — front and center for reading]

---

## Classification
**Primary:** [Category]
**Secondary:** [If applicable]

## Project Connections
[Projects or "None"]

## Keywords
[No artificial limits]

## Generation Context
**Prompt/Request:** [What the owner asked for]
**Voice guide used:** [Yes/No, which register]

## Status
[Draft / Active / Archived]
```

**Key design choices:**
- `Synthesized Text` right after Source Material (text-first for readability — metadata/classification comes after)
- `Synthesized Text` not "Original Text" (Template A's sacred section) or "Content" (Template B's)
- `Source Material` traces what Second Brain files informed the synthesis
- `Review status` in Metadata tracks Unread → Approved

---

## CANONICAL TAXONOMY

### Template A Categories (The Owner's Original Thinking)
| Category | Use When |
|----------|----------|
| Journal - Intellectual Writings | Philosophy, AI analysis, frameworks, observations (OWNER'S OWN) |
| Personal Journal | Personal reflections, life updates, feelings, daily life |
| Inventions - Bits | Software, digital, SaaS ideas (OWNER'S OWN) |
| Inventions - Atoms | Hardware, physical products (OWNER'S OWN) |
| Writing - Sci Fi | Story concepts, speculative fiction (OWNER'S OWN) |
| Writing - All Else | Activism, lyrics, other creative (OWNER'S OWN) |
| Creative / Audiovisual | Video, audio, multimedia concepts (OWNER'S OWN) |
| Personal Development | Habits, productivity, mindset, self-improvement |
| Predictions | Forecasts with timeline thinking (OWNER'S OWN) |
| Project Action | Actionable items tied to a specific project — things to DO, not ideas to file |

### Template B Categories (External References)
| Category | Use When |
|----------|----------|
| Technology Analysis | Technical deep dives, specific tool/product commentary |
| AI Commentary | AI capabilities, safety, alignment, philosophy discussions |
| Capability Watch | Exponential growth, scaling laws, capability acceleration |
| Zeitgeist | Cultural observations, tech trends, vibes, social dynamics |
| Sci-Fi (General) | External sci-fi ideas, story seeds, speculative concepts |
| Economics/Business | Markets, strategy, business analysis |
| Personal Development | Habits, productivity from external sources |
| Predictions | Forecasts from others (NOT the owner's predictions) |
| Reference Only | Pure capture, no action needed |

**CRITICAL:** Never use Template A categories for Template B content. "Journal - Intellectual Writings", "Inventions", "Writing - Sci Fi", "Writing - All Else", and "Creative / Audiovisual" are for the owner's original ideas only.

### Template C Categories (AI Synthesis)
Template C files can use categories from EITHER Template A or Template B taxonomy — the category describes the topic, not the authorship. Authorship is tracked by the template type itself (`Source type: AI Synthesis`).

**Example:** An AI-synthesized activism essay uses `Writing - All Else / Activism` as its Primary category.

---

## MERGE PROTOCOL

**When merging idea B into existing idea A:**

1. **NEVER delete original text** - Both texts are preserved, always
2. **Append at bottom** - Add `## Merged Content` section with date and full original text of B
3. **Amend keywords** - Union of both keyword sets
4. **Amend summary** - Add key new information if it expands the core insight
5. **Update metadata** - Note "Merged from: [source]" in Metadata section
6. **Preserve connections** - Add any new project connections from B

**Template for merge section:**
```markdown
---

## Merged Content (from [source], [date])

### Additional Keywords Added
[new keywords from merged content]

### Original Text (Merged)
[full preserved text of merged content]
```

**When NOT to merge (create separate file instead):**
- Ideas are related but capture different facets
- Ideas would exceed ~2000 words combined
- New content adds a distinct actionable proposal
- New content has marketing/positioning value worth preserving separately

---

## PROJECT DEVELOPMENT COACHING

**For sufficiently developed projects, proactively prompt marketing development:**

When a project has:
- Core concept defined
- Multiple related idea files
- Clear value proposition

Then proactively help with:
- [ ] **Positioning:** Core insight, pain point, value prop
- [ ] **Copy:** Taglines, headlines, elevator pitch
- [ ] **Handle:** Twitter/X handle options (check availability)
- [ ] **Strategy:** Target audience, competitive landscape, GTM phases
- [ ] **Validation:** Questions to ask potential users

**Don't wait to be asked.** When capturing feature ideas for an active project, also capture their marketing value. The "missing dimension" framing isn't just a feature spec - it's copy.

---

## WHAT NOT TO DO

- Modify original source files
- Paraphrase the owner's language
- **Rename files or folders** - Even when copying. Original names are keywords. "Misc Links and Things" stays "Misc Links and Things", not "Misc_Links"
- Keep duplicates "just in case"
- Invent connections to non-existent projects
- Mine without reading INTELLECTUAL_LANDSCAPE.md first

---

## SYNC TRIGGERS

**Token Efficiency:** Sync triggers are **batched weekly** to reduce token usage. File count updates are deferred to weekly maintenance. See STATE_OF_SECOND_BRAIN.md → WEEKLY MAINTENANCE SCHEDULE.

### Immediate Sync Required
These still require immediate `/sync-orientation-docs`:
- **Phase status changes** - Completing a processing phase
- **Major structural changes** - New folders, skill modifications
- **User explicitly requests** sync

### Deferred to Weekly Maintenance
These are batched weekly:
- File count updates in SECOND_BRAIN_MASTER_INDEX.md
- "Last Updated" timestamps in orientation docs
- Minor doc corrections and count reconciliation

### When NOT to Trigger
- Reading files (read-only operations)
- Simple searches (Glob, Grep without modifications)
- User conversations without file changes
- Normal file creation during mining (batch to weekly)

### Skill → Sync Relationship
| Skill                  | Triggers Sync                                    |
|------------------------|--------------------------------------------------|
| `/weekly-maintenance`  | **YES** — the canonical weekly sync (auto-applies mechanical fixes, surfaces judgment calls, commits). |
| `/sync-orientation-docs` | YES — explicit immediate sync for phase/structural changes. |
| process-content        | **WEEKLY** — file counts batched into weekly maintenance. |
| explore-second-brain   | No (grep-based, read-only).                      |
| verify-idea            | No (embedding + grep, read-only).                |

*Weekly maintenance is the default. Immediate sync only for phase changes or structural modifications.*

---

## MAINTENANCE SCRIPTS

Scripts in `scripts/` that Claude instances can invoke:

### update_counts.py

**Purpose:** Scan the brain and print actual file counts by category.

**When to use:**
- During `/sync-orientation-docs` to verify counts before proposing edits
- When file counts in docs seem stale or inconsistent
- After bulk file operations

**How to invoke:**
```bash
python3 "$SECOND_BRAIN_ROOT/scripts/update_counts.py"
```

**Output:** Prints total and per-category counts. Compare against SECOND_BRAIN_MASTER_INDEX.md to find discrepancies.

---

*"These files matter to me." — adapt this line to your own relationship with the material.*
