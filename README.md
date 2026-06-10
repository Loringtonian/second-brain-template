# Second Brain Template

**A working blueprint for a personal "second brain" that an AI coding agent can navigate — a blank template you clone and fill with your own life.**

> **Start with the why → [INTENT_SPEC.md](INTENT_SPEC.md).** It's the spec everything else in this repo serves: what this kind of brain is *for* (the fixed architecture intent), plus the Owner Intent slots that make it *yours* — your purpose, gaps, goals, and success criteria, filled by `/setup` and re-scored monthly. Read it before anything else; the rest of the repo is machinery in its service.

> **New here, or not very technical?** Start with **[START_HERE.md](START_HERE.md)** — a plain-English, no-jargon setup guide (the easiest path is the **Claude Desktop app**, no terminal needed). Stuck on a word like *clone* or *virtual environment*? See the **[GLOSSARY](GLOSSARY.md)**. Want to help this grow into a community project? See **[CONTRIBUTING.md](CONTRIBUTING.md)**.

This repo is not a notes app and not a finished product. It's a battle-tested *architecture* for a Claude Code "second brain," reduced to its skeleton: the rules, the context-routing logic, the document templates, the skills, and the hooks — everything that teaches a fresh agent how to operate inside a personal knowledge base, with none of the content filled in yet.

Every place your own content goes is marked `__FILL_FROM_USER__`. The whole thing is designed to be cloned and filled in *with the help of an agent* — the docs themselves carry instructions addressed to the AI that will onboard you.

---

> **What to expect on first run:** the repo ships *blank* — every personal slot is a `__FILL_FROM_USER__` marker, and the auto-loaded identity doc (`Orientation_Docs/INTELLECTUAL_LANDSCAPE_LITE.md`) is an empty scaffold *by design*. That's normal, not broken. New here? **[START_HERE.md](START_HERE.md)** lays out the friendliest path (the **Claude Desktop app** — no terminal). Open the repo in Claude Code and say *"set up my second brain"* — the **`/setup`** skill interviews you (purpose, gaps, who you are, voice, tools, privacy levels) and fills the markers. ~20 minutes gets you a working core; the rest accretes over time. A few skills call a helper you install — see [`SETUP.md`](SETUP.md).

---

## Why this is interesting

Most "AI + notes" setups are a vector database and a chat box. This is something else: a **context-engineering system**. The core idea is that a general agent becomes dramatically more useful on personal data when it's routed to exactly the right context for the task at hand — no more, no less. This repo is a worked example of how to build that routing.

The pieces that make it work:

- **Tiered, silent context loading.** `CLAUDE.md` auto-loads on every session and imports one decision guide, `ROUTER.md`. The router then decides — silently, per request — which deeper docs to pull in. A pure coding question loads nothing extra; a "what should I work on?" loads the status tier; a "what do I actually think about X?" loads the full intellectual-context tier. (See [`Orientation_Docs/ROUTER.md`](Orientation_Docs/ROUTER.md).)
- **A three-template document system.** Every piece of content is one of: **A** (the owner's original thinking, preserved verbatim), **B** (someone else's content, always attributed), or **C** (AI-synthesized publishable prose *from* the owner's notes). The author and the trust level are encoded in the template type. (See [`Orientation_Docs/ORIENTATION.md`](Orientation_Docs/ORIENTATION.md); live demos in [`examples/`](examples/).)
- **Skills as the verbs.** Repeatable operations (ingest a brain dump, verify a duplicate, segment a transcript, run weekly maintenance) are packaged as skills in `.claude/skills/`. Each declares the context it needs and loads it on demand.
- **[Hooks](GLOSSARY.md#hook) as the reflexes.** Deterministic behaviors that can't depend on the model remembering — template validation, session checkpointing, reminder injection — live as hooks in `.claude/hooks/`.

---

## How a fresh agent gets oriented (the walkthrough)

Follow the path a new Claude Code session actually takes:

1. **`CLAUDE.md` loads automatically.** It carries the hard rules (preserve exact language, never rename files, ask before deleting), the sub-agent delegation skeleton, the skills table, and the document-hierarchy map. Its first two lines `@`-import `ROUTER.md` and `INTELLECTUAL_LANDSCAPE_LITE.md`, so the agent always knows the routing rules and a one-screen summary of who the owner is.
2. **`ROUTER.md` decides what else to read.** Seven ordered rules map the user's request to a context tier. Coding → stay minimal. Status/navigation → load Tier 1. Deep/strategic/biographical → load Tier 2 (the full intellectual landscape). Writing in the owner's voice → load the voice guide. It loads *silently* — the user never sees "now reading 4 files."
3. **The orientation docs supply the "who/what/where."** `INTELLECTUAL_LANDSCAPE.md` (who the owner is, in depth), `SECOND_BRAIN_MASTER_INDEX.md` (the folder map), `STATE_OF_SECOND_BRAIN.md` (live status), `CONTENT_TAXONOMY.md` (how to classify), and friends.
4. **A skill takes over for real work.** When the task is a known operation, the matching skill fires and loads its own required context — superseding the tier rules.
5. **Hooks fire in the background** to validate, checkpoint, and remind.

The net effect: the agent shows up to every request already knowing the rules, already knowing who it's working for, and holding exactly the context that request needs.

---

## Make this yours

The repo ships as a blank template — here's the easy way and the by-hand way.

1. **Easiest — let `/setup` interview you.** Open the repo in Claude Code (the **Claude Desktop app** is the friendliest — see **[START_HERE.md](START_HERE.md)**) and say *"set up my second brain."* The **`/setup`** skill walks you through who you are, what the brain is for, your voice, tools, and privacy levels, and fills the markers for you. ~20 minutes gets a working core.
2. **By hand — find every fill-in site:**
   ```bash
   grep -rn "__FILL_FROM_USER__" .
   ```
   Each hit is a place your own content goes, in three grades: bare `__FILL_FROM_USER__` (one value), labeled `__FILL_FROM_USER__:worldview` (a named field), and HTML-comment **guidance blocks** that tell the onboarding agent what to ask you. Start with the load-bearing docs — `CLAUDE.md` (owner one-liner) and `Orientation_Docs/INTELLECTUAL_LANDSCAPE_LITE.md` (who you are).
3. **Add your own content and skills.** The skills are a starting kit (30 core + 1 exemplar pattern, `media-pipeline-example`); add domain skills as you build them — and consider **[contributing](CONTRIBUTING.md)** them back. A few skills call a helper you install — see [`SETUP.md`](SETUP.md). The `examples/` folder shows each template with a fictional persona — replace or delete it.

**Using Codex or another agent?** This template is Claude-native; see **[AGENTS.md](AGENTS.md)** for how a non-Claude agent runs the setup (expect a rebuild for deep features).

You do **not** have to fill everything before it's useful. Most of the ~140 markers are **breadcrumbs that fill in as you add content, not homework** — fill the owner one-liner and the landscape-lite and the routing already works.

---

## What's in here

```
INTENT_SPEC.md             # THE WHY — two-layer intent spec: fixed architecture intent + your owner intent
START_HERE.md              # new here? friendly, no-jargon setup guide — read this first
GLOSSARY.md                # plain-English definition of every technical term in this repo
CONTRIBUTING.md            # how to contribute skills/docs back (written for humans + agents)
AGENTS.md                  # entry point for non-Claude agents (Codex, etc.)
CLAUDE.md                  # entry point: hard rules, delegation skeleton, skills table, doc hierarchy
FOLDER_ORIENTATION.md      # quick "which folder for what" routing table
PERSONALIZE.md             # fill-in worksheet — every __FILL_FROM_USER__ site
SETUP.md                   # optional helpers a few skills need
.env.example               # copy to .env — API keys (image gen, etc.)
requirements.txt           # Python deps for the bundled scripts (/setup runs pip install -r)
LICENSE                    # MIT
Orientation_Docs/          # the routing brain
  ROUTER.md                #   the 7-rule context-loading cascade
  ORIENTATION.md           #   procedures + the A/B/C template skeletons
  CONTENT_TAXONOMY.md      #   how to classify any piece of content
  SECOND_BRAIN_MASTER_INDEX.md  # folder map + grep-search patterns
  INTELLECTUAL_LANDSCAPE(_LITE).md  # who the owner is (full + always-loaded summary)
  COGNITIVE_PROFILE.md     #   how the owner thinks (Template C, advisory)
  VOICE_GUIDE.md           #   how to write in the owner's voice
  STATE_OF_SECOND_BRAIN.md #   live status dashboard
  KEYWORD_GUIDE.md         #   the owner's vocabulary
  PRIVACY_DEPTH.md         #   privacy-depth (1–5) rubric + publish/load gating
  TODO_MASTER.md           #   cross-project TODO routing hub
  PHASE_2_VISION.md        #   context-engineering notes / forward vision
.claude/
  skills/                  # 31 skills incl. /setup onboarding (the verbs)
  hooks/                   # deterministic reflexes (validation, checkpointing, reminders)
  scripts/                 # bundled helper: validate_template.py
  agents/                  # sub-agent definitions (orientation oracle, file verifier)
  settings.json            # config — hooks are unwired by default (see SETUP.md)
scripts/                   # tz.py, stamp_depth.py, remove_watermark.py (work); sb_embed.py, build_brain_snapshot.py (stubs)
Inventions/ Journal_*/ Writing_*/ Predictions/ Health/ External_Sources/   # your content —
Written_By_AI/ Reference/ Projects/                                        #   ship as empty stubs
examples/                  # one synthetic file per template type (fictional persona)
```

## What ships blank

Everything personal is left for you to fill: notes, journals, inventions, writing, bookmarks, project content, voice, and intellectual landscape. The personal-content folders ship as empty stubs — `examples/` substitutes one synthetic file per template type. Domain-specific skills tied to a particular person's life (a media archive, a podcast-clip pipeline, etc.) are not included; what remains is the architecture-generic set.

## A note on the hooks and skills

These are real, working pieces — but they were written against a real working setup, with absolute paths replaced by a `$SECOND_BRAIN_ROOT` placeholder. Treat them as **patterns to adapt**, not drop-in runnable code; getting them running is part of making the brain yours. [`SETUP.md`](SETUP.md) lists exactly which skills need a helper and how to enable them.

---

*This is a living template. The best version of it is the one you've filled with your own life.*
