---
depth: 1
---
<!-- APPROVED master. Lives in the real brain (Projects/Stripped_Brain/) as the source of truth.
     Transfer a copy to the handout repo root as INTENT_SPEC.md once the repo relocation completes.
     Owner Intent ships as __FILL_FROM_USER__ markers for /setup to fill. -->

# Second Brain — Intent

> **Status:** OFFICIAL — architecture intent owner-approved 2026-06-08. Two layers: the **architecture intent** (authored, stable — what this kind of brain is and why; approved) and the **owner intent** (your `__FILL_FROM_USER__` slots, elicited by `/setup` and revised as your brain grows). The architecture half is settled; the owner half is filled per-owner at setup.

## What This Is For

This is a **standardized, self-shaping Second Brain template**. It ships blank and **molds itself to whoever owns it** — their material, their workflow, their goals — rather than assuming one kind of mind. One owner fills it with half-formed ideas and voice memos; another with research, client work, writing, or code. The architecture is the same; it adapts to each.

What it does, for any owner, is turn that scattered output — notes, voice memos, half-formed ideas, things read and reacted to, automated pulls from your own feeds — into **context an AI agent can navigate**, so a general-purpose agent shows up to every task already knowing who it's working for and holding exactly the slice of that person's mind the task needs. It is not a notes app and not a search box over a pile of documents. It is a **context-engineering system**: the value is not in storing information, it's in *routing the right context to the right task at the right depth*. The gap it fills is specific — a frontier model is brilliant in general and blind to *you*; without your context it gives answers that are correct but misframed. This brain closes that gap by making its owner legible to their own agent — in effect, an **API to their own intellectual world** — and it does so the same way regardless of what that world looks like.

## Core Intent

- **Capture at the speed of thought — actively and passively.** The hardest part of any second brain is the friction between having a thought and storing it usefully. The system minimizes that friction two ways. **Actively** — dictation, brain-dumps, reaction-capture — preserving what's captured *in the owner's exact words* (keywords are sacred for retrieval; the system never paraphrases the owner's original thinking). And **passively** — your own data exports plus lightweight pullers the agent builds for you on request: your X archive (downloaded from X), your reading and highlights (Readwise/Kindle), an RSS feed — auto-filed, auto-connected, and turned into to-dos and follow-ups once wired. The template ships the *pattern* for this (`/media-pipeline-example` + `SETUP.md`), not a pre-built scraper for any one service — you point the agent at a source and it builds the pull. So capture can keep happening even when you aren't deliberately capturing.

- **The agent shows up oriented.** Every session, `CLAUDE.md` auto-loads and imports one decision guide, `ROUTER.md`, which then silently pulls exactly the context tier a request needs — your saved coding preferences (and little else) for a pure coding task, the status tier for "what should I work on," the full intellectual-context tier for "what do I actually think about X." The owner never re-explains who they are. The agent holds exactly what the task needs — no more, no less.

- **Authorship and trust are encoded, not assumed.** Every piece of content is one of three templates — **A** (the owner's original thinking, verbatim), **B** (someone else's content, always attributed), **C** (AI-synthesized prose *from* the owner's notes). The template type carries who wrote it and how far to trust it, so the agent never mistakes a synthesis for a source or the owner's words for someone else's.

- **The brain is an orchestration nexus.** It is not just a context store — it is where the agent's *capabilities* are organized and grown. It pulls in repos from GitHub, registers new skills and tools, and wires in external services, so the agent augments its own abilities in a coherent, managed way rather than ad hoc. New power lands in one declared, discoverable place instead of scattered across one-off scripts. The brain is the agent's workshop as much as its memory.

- **You own it, and it's portable — model- and provider-agnostic.** The brain is plain files you own and control. Contrast a hosted assistant's memory — ChatGPT recalls and stores well, but you don't own it, can't inspect it, and can't take it with you. Here, your context is yours: swap models, swap agents (move from one runtime to another), or run several at once, and your accumulated self-model comes along intact. No lock-in to a model, a provider, or a vendor's memory format.

- **The brain co-evolves with its owner.** This is the load-bearing intent. The brain ships blank and grows through ongoing interaction between the owner and whatever agent runs the file system. The owner dumps thoughts; the agent files, connects, and synthesizes them; the structure routes future context; the owner corrects, and the corrections compound. Over time the brain becomes a higher-fidelity, queryable model of the owner's intellectual world than the owner could ever write down deliberately. **This spec exists to keep that growth pointed in the right direction** — so accretion deepens the model instead of drifting into a junk drawer.

- **Privacy is a dimension, not an afterthought.** Every file carries a depth (1–5): 1 is public footprint, 5 is private interiority. Depth gates two things — what the agent loads into context for a task, and what may ever be shared or published. The intent is that the owner's most private thinking can live in the same system as their public ideas *without risk of leaking*, because the boundary is encoded per-file and enforced by tooling.

- **Surface signal from the owner's own noise.** A heavily-used brain accumulates far more than its owner can act on. Part of the system's job is to help recognize which of the owner's *own* ideas are worth returning to — recognition being easier than generation — and to keep good ideas alive and surfaced rather than buried and decaying unacted-upon.

- **The agent proposes; the owner decides.** The system is collaborative, not autonomous. The agent drafts, files, and suggests, but a few rules are inviolable: preserve the owner's exact language, never rename files (keyword recall depends on stable names), and ask before deleting or merging. Trust comes from the owner staying in the loop on anything irreversible.

## Owner Intent (`__FILL_FROM_USER__` — elicited by `/setup`, revised as the brain grows)

The section above is fixed: it's the intent of the *architecture*. This section is **yours**, and it's what makes the spec a live instrument rather than a manifesto. `/setup` interviews you to fill it; revisit it whenever your brain's purpose sharpens.

- **What this brain is for (you):** `__FILL_FROM_USER__:brain_purpose`
- **The gaps it fills — what you're weak at that it should cover:** `__FILL_FROM_USER__:gaps_filled`
- **Your goals — what acting on this brain should produce in your life and work:** `__FILL_FROM_USER__:owner_goals`
- **Success looks like:** `__FILL_FROM_USER__:success_criteria`
- **Explicit non-goals — what you do NOT want this to become:** `__FILL_FROM_USER__:owner_non_goals`
- **Your privacy register — the one-line test for "too private to share":** `__FILL_FROM_USER__:privacy_register` (calibrated in `Orientation_Docs/PRIVACY_DEPTH.md`)
- **Your toolchain — the services and tools you want the brain to orchestrate:** `__FILL_FROM_USER__:toolchain` (your cloud/deploy provider, GitHub, the agents and apps you live in)
- **Credentials to wire in (names only — secrets live in `.env`, never in this file):** which credentials you'll provide so the brain can act for you — GitHub, deployment (e.g. fly.io / your cloud), API keys: `__FILL_FROM_USER__:credentials_to_wire`

> **Secrets never live in this file.** `/setup` records *which* tools and credentials you use and wires the actual values into a gitignored `.env` (or your secret store). This spec — which is safe to share — only ever *names* them, so the orchestration intent is legible without exposing a single key.

## Done Criteria (the architecture is "working")

The brain is doing its job once: a fresh agent, handed any task, routes to the right context without the owner re-explaining themselves; capture friction is low enough — active *and* passive — that thoughts and signals actually land in the system; the owner can retrieve their own past thinking by keyword or meaning; the agent can *act* through the owner's wired-in tools, not only answer; and the brain has begun to *accrete* — each week modeling its owner a little more faithfully than the last. There is no finish line; "done" is the loop running and compounding.

*Two of these are owner-activated, by design: passive capture and semantic retrieval. The template ships the patterns and the stubs — they come online once you've pointed the agent at a feed to pull (passive capture) and implemented the embedding stub against your own content (semantic retrieval). Until then, active capture and keyword retrieval carry the loop, and both work from day one.*

## What This Is Not

- **Not a notes app or a read-it-later pile.** Those optimize for storage and reading. This optimizes for *an agent acting well on your behalf*. A feature that helps you file more and act better belongs; one that just stores more does not.
- **Not a vector database with a chat box.** Retrieval-only systems answer "find me the note about X." This routes *the right context for the task* — a different and harder problem. Routing over raw retrieval is the whole point.
- **Not locked to one model or provider.** It's plain files you own, portable across agents and runtimes — not a memory feature trapped inside someone else's product. Switch models or agents and your self-model comes with you.
- **Not for one kind of person.** It's a self-shaping template, not a clone of any one owner's workflow. It adapts to whatever you bring — ideas, research, writing, code, a business.
- **Not a finished product.** It ships as a blank template and is only ever as good as what its owner fills it with. The best version is the one filled with a real life.
- **Not a vault for content you want kept from your agent.** Truly private material is gated by depth or kept out entirely. Privacy here is *expressible*, not absent.
- **Not autonomous.** The agent never silently rewrites the owner's words, renames their files, or deletes their content. Human-in-the-loop on anything irreversible is a feature, not a limitation.

## Already Settled (Ships With the Template)

- **Tiered, silent context loading** via `Orientation_Docs/ROUTER.md` — ordered rules mapping request → context tier.
- **The three-template document system** (A/B/C), authorship and trust encoded in the type.
- **Skills as verbs, hooks as reflexes** — repeatable operations in `.claude/skills/`; deterministic behaviors that can't depend on the model remembering in `.claude/hooks/`.
- **Orchestration of capabilities** — skills, hooks, pulled-in repos, and wired tools register in one place so the agent's abilities grow coherently rather than ad hoc.
- **Model/provider-agnostic, owner-owned storage** — plain files you control, portable across agents; no vendor memory lock-in.
- **`/setup` is the front door** — it interviews the owner and fills every *load-bearing* `__FILL_FROM_USER__` marker at onboarding: the Owner Intent section above (purpose, gaps, goals, privacy register, toolchain, and which credentials to wire into `.env`), plus identity, voice, privacy calibration, and machine profile. The markers that can only be filled once you have real content (project rosters, mined keywords, cognitive-profile synthesis) carry a breadcrumb telling the agent when to fill them — so nothing reads as forgotten, it reads as *not yet earned*. It also **gets the environment runnable** — verifying Python and Git, creating a virtual environment, and installing the brain's dependencies — so the brain can install and run its own tooling out of the box, surfacing a manual step only when something can't be set up automatically.
- **Privacy depth 1–5** on every file, gating both context-load and publish/share, calibrated per owner in `PRIVACY_DEPTH.md`.
- **The inviolable rules** in `CLAUDE.md`: preserve exact language, never rename files/folders, ask before deleting or merging, never destroy data before verifying capture.

## Not Declared Here (Lives Elsewhere)

This file declares *what the brain is and why it exists*. It does not declare *how the machinery works* — the routing rules (`ROUTER.md`), the template schemas (`ORIENTATION.md`), the taxonomy (`CONTENT_TAXONOMY.md`), the skills and hooks (`.claude/`), and the helper setup (`SETUP.md`) each own their domain. When this spec and the machinery disagree, this spec describes the *intent* and the machinery is what gets corrected — or, if the machinery reveals a better intent, this spec is what the owner revises.
