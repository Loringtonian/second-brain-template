# scripts/

Helper scripts the skills and hooks call. This folder ships with **one working generic helper
(`tz.py`) and one stub (`sb_embed.py`)** — add your own as you wire skills up.

| Script | Used by | Status |
|--------|---------|--------|
| `tz.py` | anything that timestamps (`from tz import now`) | **works** — set your zone via `SECOND_BRAIN_TZ` in `.env` |
| `sb_embed.py` | `/semantic-search`, `/verify-idea`, `/explore-second-brain`, `/connection-finder` | **stub** — implement to enable semantic search; until then those skills fall back to `grep` |
| `.claude/scripts/validate_template.py` | `/process-content`, the `*-example` ingest skills, the `validate_template_b` hook | **works** — bundled (note: lives under `.claude/scripts/`, not here) |

To enable semantic search, replace `sb_embed.py` with a real CLI that embeds your `.md` files
(e.g. with [`sentence-transformers`](https://www.sbert.net/) + a model like `BAAI/bge-large-en-v1.5`)
and supports `search "<query>"` and `verify "<idea>"`. See `SETUP.md` at the repo root.

Anything machine-specific (API keys, absolute paths) belongs in `.env`, not here — see `.env.example`.
