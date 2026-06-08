# SECOND BRAIN MASTER INDEX
*Folder Structure Documentation*
*Last Updated: `__FILL_FROM_USER__:last_updated`*

---

## Layered Orientation System

Orientation docs follow a layered pattern:

| Level | Document | Purpose |
|-------|----------|---------|
| **Root** | `FOLDER_ORIENTATION.md` | Quick routing table - which folder for what |
| **Folder** | `[Folder]/ORIENTATION.md` | Detailed guidance for each folder |
| **Central** | `Orientation_Docs/INTELLECTUAL_LANDSCAPE.md` | Projects, themes, key people |

**For routing:** Start with `FOLDER_ORIENTATION.md`, then read the folder-specific `ORIENTATION.md`.

---

## Stats

File counts are approximate and change constantly. Track them with `scripts/update_counts.py` rather than by hand; don't update docs just for count discrepancies. Record the current snapshot here when you run a sync (`__FILL_FROM_USER__:file_counts`).

**Note (a common gotcha worth recording):** podcast snips often live in TWO locations — a raw vault (episode files, each containing multiple snips) and a processed tree (individual snips as Template B files), plus full episode transcripts. Note any such split here so search knows where to look.

---

## Folder Structure

> This is a representative second-brain layout. The content folders below are a reusable starting taxonomy; the `Projects/` subtree is entirely the owner's own and is shown here as placeholders (`__FILL_FROM_USER__:projects`).

```
Second_Brain/
├── AA_Lists/              # Personal lists (reading, watch, games, places, people, tips)
├── Orientation_Docs/      # Central docs (INTELLECTUAL_LANDSCAPE, ORIENTATION, etc.)
├── Projects/              # Active project folders — __FILL_FROM_USER__:projects
│   ├── <project_a>/       # e.g. a tool you're building
│   ├── <project_b>/       # e.g. a writing/creative project
│   └── <project_c>/       # e.g. a research project
├── Inventions/
│   ├── Bits/              # Software, SaaS, apps
│   ├── Atoms/             # Hardware, physical products
│   ├── Art/               # Creative, audiovisual concepts
│   └── Mixed/             # AR, BCI, board games, hybrid
├── Journal_Intellectual/  # Philosophy, analysis, frameworks
├── Journal_Personal/      # Diary, reflections, personal
├── Writing_SciFi/
│   └── <flagship_project>/ # The owner's flagship writing project
├── Writing_AllElse/       # Lyrics, activism, other creative
├── Written_By_AI/         # AI-synthesized publishable writing (Template C)
├── Predictions/           # Forecasts with timelines
├── External_Sources/
│   ├── podcast_clips/     # Podcast clips (Template B)
│   ├── Podcast_Transcripts/ # Full episode transcripts
│   ├── X_Bookmarks/       # Processed bookmarks (Template B)
│   └── ChatGPT_Research/  # Research references
├── Reference/             # External references
├── Health/                # Wellness, nutrition, sleep
├── Twitter_Personas/      # Social content, personas
├── To_Study/              # Learning queue
├── Creative_AudioVisual/  # Multimedia concepts
├── Podcasts/              # Raw podcast vault (episode files, auto-syncing)
├── Wiki/                  # Personal knowledge wiki
├── Intellectual_Scraps/   # Raw intellectual fragments (unclassified drafts)
└── Personal_Operations/   # Life-ops: trips, contracts, memberships. Confidential, gitignored content.
```

---

## Folder Descriptions

### Original Thinking (Template A)

| Folder | Content | Projects |
|--------|---------|----------|
| **Inventions/Bits/** | Software, SaaS, AI tools | `__FILL_FROM_USER__:bits_projects` |
| **Inventions/Atoms/** | Hardware, physical products | `__FILL_FROM_USER__:atoms_projects` |
| **Inventions/Mixed/** | Hybrid concepts | (hybrid project nuggets) |
| **Journal_Intellectual/** | Philosophy, analysis, frameworks | (themes, not projects) |
| **Journal_Personal/** | Personal reflections, diary | None |
| **Writing_SciFi/** | Sci-fi stories | The flagship writing project |
| **Writing_AllElse/** | Activism, lyrics, other creative | None |
| **Predictions/** | Forecasts with timelines | None |
| **Health/** | Wellness, chronic pain, nutrition | None |

### External References (Template B)

| Folder | Content | Source |
|--------|---------|--------|
| **External_Sources/podcast_clips/** | Podcast clips (Template B) | the clip pipeline |
| **External_Sources/Podcast_Transcripts/** | Full episode transcripts | yt-dlp, show sites, Whisper |
| **External_Sources/X_Bookmarks/** | Saved posts from others | bookmark exports |
| **External_Sources/ChatGPT_Research/** | Research and reference material | research conversations |

---

## How to Search

Use grep for all searches (100% accuracy, ~100 tokens per search):

### Find files by project:
```bash
grep -r "**Projects:**.*<ProjectName>" "$SECOND_BRAIN_ROOT/" --include="*.md"
```

### Find files by keyword:
```bash
grep -ri "<keyword>" "$SECOND_BRAIN_ROOT/" --include="*.md" -l
```

### Find files by category:
```bash
grep -r "**Primary:** Journal - Intellectual" "$SECOND_BRAIN_ROOT/" --include="*.md"
```

### Find files mentioning a person:
```bash
grep -ri "<person>" "$SECOND_BRAIN_ROOT/" --include="*.md" -l
```

### Count files in a project:
```bash
grep -r "**Projects:**.*<ProjectName>" "$SECOND_BRAIN_ROOT/" --include="*.md" | wc -l
```

---

## Key Themes by Location

Map the owner's recurring themes to where they live (`__FILL_FROM_USER__:themes_by_location`). Example shape:

| Theme | Where to Search |
|-------|-----------------|
| AI & technology | Journal_Intellectual/, Predictions/, Writing_SciFi/ |
| Startups, Business | Inventions/Bits/, Inventions/Atoms/ |
| Economics & markets | Journal_Intellectual/, External_Sources/ |
| Governance, coordination | Journal_Intellectual/, Predictions/ |
| Sci-Fi, Stories | Writing_SciFi/ |
| Personal Development | Journal_Personal/, Health/ |
| Climate, Energy | Writing_AllElse/, Journal_Intellectual/ |

---

## Archive Note

Pre-built category indexes have been deprecated in favor of grep-based search.

**Rationale:** Grep search is far more token-efficient and provides 100% accuracy vs stale indexes.

---

*This document lives in Orientation_Docs/. Use grep for all content searches.*
