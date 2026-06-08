---
name: launch-idea
description: Launch an invention from elevator pitch to spec sheet - tiered pipeline for shipping ideas from Inventions/ files
user_invocable: true
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - Skill
required_context_files:
  - Orientation_Docs/KEYWORD_GUIDE.md
  - Orientation_Docs/CONTENT_TAXONOMY.md
  - Orientation_Docs/ORIENTATION.md
---

# Launch Idea

<!-- silent-context-load:v1 -->
## Step 0 — Silent Context Load

Before doing anything else, silently `Read` each file in `required_context_files` (listed in frontmatter) if it is not already in your context. Do NOT announce the reads. Do NOT ask permission. This ensures the skill has the orientation it needs without bloating sessions that don't invoke it.

Files:
- `Orientation_Docs/KEYWORD_GUIDE.md`
- `Orientation_Docs/CONTENT_TAXONOMY.md`
- `Orientation_Docs/ORIENTATION.md`

<!-- silent-context-load:v1 -->

**Status: WIP/Prototype** — Skeleton defined, lower tiers work, upper tiers need real tooling.

Fire off an idea with various degrees of finality. From elevator pitch to landing page. The pipeline that takes ideas sitting in files and starts shipping them.

## Trigger Conditions

- "launch this idea", "escalate this", "boost this concept"
- "make images for this", "pitch deck", "elevator pitch"
- User points at an Inventions/ file and wants to do something with it

## Philosophy

The core insight: "If ideas are just sitting in the file, they're not shipping — there's nothing there." This skill puts the owner's judgment at the heart of the pipeline — operating "like an executive and your CEO for a whole bunch of random startups until you find the ones that work." Leverage judgment and taste, not turn things to slop.

## Tier Model

Each tier is independent. Run any tier solo or chain them. Lower number = less effort, faster.

| Tier | What                  | Status        | Tooling                              |
|------|-----------------------|---------------|--------------------------------------|
| 1    | Elevator Pitch        | **WORKS NOW** | AI text generation (straightforward) |
| 2    | Concept Images        | **WORKS NOW** | Nano Banana Flash skill              |
| 3    | X Announcement        | **WORKS NOW** | voice guide + X posting              |
| 4    | Spec Sheet            | MANUAL        | write a product spec (PRD)           |
| 5    | Pitch Deck            | NOT BUILT     | No slide generation tooling yet      |
| 6    | Landing Page          | NOT BUILT     | No website builder integrated        |
| 7    | Video                 | NOT BUILT     | No script-to-video for non-podcasts  |

## Tier 1: Elevator Pitch

**Input:** Idea file path (Template A from Inventions/)
**Output:** 2-3 sentence pitch, tagline, target audience

1. Read the idea file
2. Read INTELLECTUAL_LANDSCAPE.md for project context
3. Generate:
   - One-liner tagline
   - 2-3 sentence elevator pitch
   - Target audience
   - "What would you pay for..." framing (if applicable)
4. Present for approval

## Tier 2: Concept Images

**Input:** Idea file + approved elevator pitch
**Output:** 3-5 concept images

1. Use Nano Banana Flash to generate concept images
2. Scenes: product in use, ad mock-up, hero shot
3. Save to idea's folder

## Tier 3: X Announcement

**Input:** Idea file + pitch + images
**Output:** Draft X post ready for queue

1. Write post copy using the owner's X persona voice (`__FILL_FROM_USER__:x_handle`)
2. Attach best concept image
3. Queue via your posting workflow (or present for manual post)

## Tier 4: Spec Sheet

**Input:** Idea file
**Output:** a product specification (PRD)

1. Write a product spec from the idea, aggregating related Second Brain content
2. Produce a PRD suitable for automated code generation

## Tiers 5-7: NOT YET BUILT

These need real tooling work:
- **Tier 5 (Pitch Deck):** Slide generation, narrative structure, export to PDF/PPTX
- **Tier 6 (Landing Page):** Website builder integration, hosting, domain
- **Tier 7 (Video):** Script writing, visual generation, voiceover, editing pipeline

## Usage

```
/launch-idea [tier] [idea-file-path]

# Examples:
/launch-idea 1 Inventions/Atoms/My_Hardware_Idea.md
/launch-idea 1-3 Inventions/Bits/My_Software_Idea.md   # chain tiers 1 through 3
```

## Open Questions (Future Work)

- **Asset management:** Where do generated files live? Folder conventions?
- **Project tracker integration:** Status progression as tiers complete
- **Batch mode:** Run pipeline across multiple ideas in Inventions/
- **Scoring:** Which ideas deserve which tiers? Prioritization heuristic
- **Cost tracking:** API costs per tier (image gen, etc.)
