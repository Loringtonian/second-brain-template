# Routing Rules

Content type → destination mappings for brain dump ingestion.

## Priority Rule: Project Folder Wins

**If an idea is about an active project with its own folder, route to that project folder — NOT the generic category folder.** An idea for a specific project goes in `Projects/[ProjectName]/`, not a generic category like `Inventions/Bits/`. Only use category folders (`Journal_Intellectual/`, `Inventions/Bits/`, etc.) for ideas that don't belong to a specific project.

**Adjacency warning:** When a voice note contains multiple ideas, do NOT bleed project connections between them. Each idea gets its own project connections based on its content, not its proximity to other ideas in the same recording.

## By Content Type

| Type        | Destination                             | Notes                                         |
|-------------|-----------------------------------------|-----------------------------------------------|
| NEW_IDEA    | `[Category]/`              | Use Template A, verify with verify-idea first |
| TODO        | Project TODO file                       | Format: `- [ ] [content] (Source: [date])`    |
| AUGMENT     | Existing file                           | Propose addition, get approval                |
| PREDICTION  | `Predictions/`                          | Include timeline, confidence                  |
| READING_LIST| `AA_Lists/READING_LIST.md`              | Checkbox item                                 |
| NEW_PROJECT | `INTELLECTUAL_LANDSCAPE.md`             | Include status, keywords                      |
| QUESTION    | Log only                                | Don't create file                             |
| OBSERVATION | Evaluate                                | If valuable → NEW_IDEA, else discard          |

## By Source Type

| Source                   | Template | Key Rule                                          |
|--------------------------|----------|---------------------------------------------------|
| Claude Code conversation | A        | Owner's words THIS conversation                   |
| Voice dictation          | A        | Owner's words only — remove any AI responses      |
| Voice notes (transcribed)| A        | Transcription of owner's original thinking        |
| Podcast / external clips | B        | EXTERNAL content — attribute speakers             |
| Bookmark exports         | B        | OTHER people's content                            |

## Category Folder Selection

| Content About                         | Folder                  |
|---------------------------------------|-------------------------|
| Philosophy, AI analysis, frameworks   | `Journal_Intellectual/` |
| Personal reflections, feelings        | `Journal_Personal/`     |
| Software, SaaS, apps                  | `Inventions/Bits/`      |
| Hardware, physical products           | `Inventions/Atoms/`     |
| Sci-fi, story concepts                | `Writing_SciFi/`        |
| Activism, lyrics, other creative      | `Writing_AllElse/`      |
| Forecasts with timelines              | `Predictions/`          |
| Wellness, nutrition                   | `Health/`               |

## TODO Routing

TODOs route to project-specific TODO files. Each project should declare its own TODO file path. Example pattern:

| Project                      | TODO File                                       |
|------------------------------|-------------------------------------------------|
| `__FILL_FROM_USER__:project1`| `Projects/[ProjectName]/TODO_[ProjectName].md`  |
| `__FILL_FROM_USER__:project2`| `Projects/[ProjectName]/TODO_[ProjectName].md`  |
| Second Brain (meta)          | `Orientation_Docs/TODO_Second_Brain.md`         |
| Miscellaneous                | `Orientation_Docs/TODO_Miscellaneous.md`        |

Replace the placeholder rows with your actual project TODO paths.
