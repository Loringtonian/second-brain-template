# SETUP — Optional Helpers

**You do not need any of this to start.** The rules, context-routing (ROUTER → tiers),
the Template A/B/C system, and most skills are prompt-driven — they work the moment you
open this repo in Claude Code. **Easiest path: say "set up my second brain"** to run the
[`/setup`](.claude/skills/setup/SKILL.md) interview (purpose, who you are, voice, tools/keys,
privacy levels). Fill in your brain first; wire the helpers below up later, when you want the
matching skill.

> **Never used a terminal, or unsure what a "virtual environment" or "API key" is?** You can
> ignore almost all of this file. If you set up via the **Claude Desktop app** (see
> [`START_HERE.md`](START_HERE.md)), the `/setup` skill does every technical step for you. This
> page is for wiring up an optional extra by hand later. Plain-English definitions of every term
> here live in the **[GLOSSARY](GLOSSARY.md)**.

A few skills are **patterns to adapt** rather than drop-in code: they call a helper script or
external tool that is specific to one person's machine and is not bundled. Here's what each needs.

## Helper scripts

| Skill / hook | Needs | What it does | Status |
|---|---|---|---|
| `process-content`, `/ingest-brain-dump`, the `validate_template_b` hook | `.claude/scripts/validate_template.py` | Validates Template A/B/C structure | **Bundled — works out of the box.** |
| timestamps; `/setup` privacy phase | `scripts/tz.py`, `scripts/stamp_depth.py` | Canonical timezone + `depth:` privacy stamping | **Bundled — work out of the box.** |
| `/semantic-search`, `/verify-idea`, `/explore-second-brain`, `/connection-finder` | `scripts/sb_embed.py` + a local embedding model | Embedding-based semantic search & duplicate detection over your notes | **Stub.** Until you implement it, these skills fall back to `grep`. |
| `/load-brain` | `scripts/build_brain_snapshot.py` | Concatenates your brain into one Tier-4 snapshot | **Stub.** Implement to walk your content folders; see the file's docstring. |

**To enable semantic search:** write a small CLI at `scripts/sb_embed.py` that embeds your `.md`
files (e.g. with [`sentence-transformers`](https://www.sbert.net/) and a model such as
`BAAI/bge-large-en-v1.5`) and supports `search "<query>"` and `verify "<idea>"` subcommands.
The three skills above call it with those subcommands; until it exists they degrade to keyword
search, so they still work — just less semantically.

## Python dependencies

The bundled scripts (`scripts/remove_watermark.py` + the `/nano-banana` image skills) need a few
Python packages, pinned in [`requirements.txt`](requirements.txt). The **`/setup`** environment
bootstrap creates a **virtual environment** (a private sandbox for this project's Python add-ons —
see the [GLOSSARY](GLOSSARY.md#virtual-environment-venv)) and installs them for you automatically;
to do it by hand:

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
```

Heavier extras (`simple-lama-inpainting` for `/remove-watermark --lama`, `sentence-transformers`
for semantic search) are commented out in `requirements.txt` — uncomment to enable them.

## Hooks

Everything in `.claude/hooks/` is an **example mechanism** — these are NOT wired into
`.claude/settings.json` by default, so they don't run until you register them. To activate one,
add it under a `hooks` key in `settings.json` (see the Claude Code hooks docs). They reference a
`$SECOND_BRAIN_ROOT` placeholder where an absolute path used to be — set it to your repo root.
Treat them as patterns to adapt, not guaranteed-runnable code.

- `validate_template_b.py` — auto-validates Template B files on Write/Edit (uses the bundled validator).
- `precompact_checkpoint.py`, `verify_reminder.py`, `breadcrumb_detect.py`, `mark_embedding_pending.py`, `check_inbox.py` — small reflex hooks; adapt paths/triggers to your setup.
- `trace_tokens.py` + `analyze_token_trace.py` + `arm_/disarm_trace_oneshot.py` — an optional token-usage profiler (`touch /tmp/token_trace.active` to start a trace).

## Companion tools — what your brain can plug into

This template is prompt-driven and runs on its own, but a handful of external tools make it much
more capable. **None ship in this repo** — install the ones that fit how you work. The `/setup`
wizard walks you through this menu and asks what you actually do.

### Capture by voice (strongly recommended)
Talking is the highest-bandwidth, most human way to feed a brain — the single easiest habit that
makes a second brain actually stick. Wire up dictation and make voice your default input:
- **superwhisper** — accurate system-wide voice-to-text for Mac (subscription). https://superwhisper.com
- **Claude Code's native voice input** — built in, nothing to install.
- **Wispr Flow** — fast, polished dictation that works across every app. https://wisprflow.ai

### Makes the bundled skills fully work
- **Embedding engine** — powers `/semantic-search`, `/verify-idea`, `/connection-finder`, and
  `/explore-second-brain`; without it they fall back to plain `grep`. Implement the shipped
  `scripts/sb_embed.py` stub with `sentence-transformers` + a model like `BAAI/bge-large-en-v1.5`.
- **A headless-browser CLI** — drives the `$B` Browser-Verification Protocol in `CLAUDE.md`
  (fills `__FILL_FROM_USER__:browser_harness_path`). Use **browser-harness** (direct CDP control)
  and/or **gstack's `/browse`** — either works.
- **Google Gemini key** — unlocks `/nano-banana-flash` and `/nano-banana-pro` image gen. Set
  `GEMINI_API_KEY` in `.env`.
- **ripgrep + jq** — assumed by `CLAUDE.md` SEARCHING and every CLI-JSON workflow. `brew install ripgrep jq`.

### Power-ups (recommended)
- **gstack** — turns Claude Code into a virtual eng team: `/browse`, `/codex`, `/review`, `/qa`,
  `/cso`, `/ship`, plus a full design suite (MIT, ~23 skills). Needs [Bun](https://bun.sh):
  `git clone --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`

### Connect your real life (zero install — toggle in Claude settings)
- **Gmail · Google Drive · Google Calendar · Notion connectors** — let the agent read your mail,
  docs, calendar, and notes. Optional, but this is what turns a notes folder into a real *second brain*.

### By workflow (install only what matches what you do)
- **Code review / second opinion** → **Codex CLI** (OpenAI); gstack's `/codex` wraps it for adversarial review.
- **Media / podcast pipelines** → **ffmpeg / ffprobe** + **yt-dlp** (durations, transcripts, clip extraction).
- **Deploying services** → **fly** (Fly.io VMs) + **tailscale** (private device mesh / phone sync).
- **3D / CAD** → **Blender** (MCP) + **ForgeCAD** (parametric `.forge.js` models).
- **Messaging capture** → **Hermes** — bridges Telegram / WhatsApp / Discord / Signal into the brain as a comms layer.

### Passive capture — your own trail, pulled in
The template ships **no scraper**. Passive capture is your own data plus a puller the agent builds on request:
- **X / Twitter** → download your archive from X (Settings → *Download an archive of your data*), then run `/ingest-brain-dump` on it. Export your data; don't scrape.
- **Reading & highlights** (Readwise, Kindle, Pocket, RSS) → ask the agent to *build you a puller* using the `/media-pipeline-example` pattern (detect → process → enrich → file) and your service key in `.env` (e.g. `READWISE_API_KEY`). It files attributed Template B entries.
- Once a puller exists, schedule it (cron / launchd) so capture keeps happening without you lifting a finger.

## Keys, voice & privacy depth

- **API keys live in `.env`** (gitignored). `cp .env.example .env` and fill what you use —
  `GEMINI_API_KEY` makes the image skills work; add a speech-to-text key (e.g. `DEEPGRAM_API_KEY`)
  if you wire up dictation.
- **Voice / dictation capture** is the highest-bandwidth way to feed a brain — wiring up a `/voice`
  or dictation skill is strongly recommended (`/setup` prompts you for it).
- **Privacy depth** — every file carries a `depth: N` (1–5) line; `scripts/stamp_depth.py <file> <N>`
  stamps it and `/setup` calibrates your rubric. See `Orientation_Docs/PRIVACY_DEPTH.md`.

---

*Everything not listed here works prompt-only. The point of the template is the architecture —
adapt the helper-dependent pieces to your own environment as you grow your brain.*
