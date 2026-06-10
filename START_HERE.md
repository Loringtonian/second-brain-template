# Start Here — A Friendly Setup Guide

Welcome. This is a **template for a "second brain"** — a folder of notes, plus an AI
assistant that already knows how to organize and use them for you. **You do not need to be
technical**, and you do not need to understand the rest of this repository. This one page
takes you from zero to a working brain.

> **The one-sentence version:** get these files onto your computer, open the folder in an AI
> coding assistant (we recommend the **Claude Desktop app** — it has buttons, no typing
> commands), and say **"set up my second brain."** A guided interview does the rest (~20 min).

Hit a word you don't know — *clone, repo, terminal, virtual environment, API key?* Open the
**[GLOSSARY](GLOSSARY.md)**. Every scary term is explained there in one plain sentence.

---

## What you need

1. **An AI coding assistant.** This template is built for **[Claude Code](GLOSSARY.md#claude-code)**
   (by Anthropic). The friendliest version is the **Claude Desktop app** — a normal app with
   a window and buttons. (Other tools — the Claude website, or OpenAI's Codex — can work too;
   see [Other ways](#other-ways).)
2. **A Claude subscription** (Pro or Max — create an account / subscribe at
   **https://claude.com/pricing**). The Desktop app signs you in. If clicking **Code** asks you
   to upgrade, your account isn't on a paid plan yet.
3. **This repo's files on your computer** — Step 1 below shows the no-account way to get them.

You do **not** need a [GitHub account](GLOSSARY.md#github-account) to start. (It's worth making
a free one later — see [A note on GitHub](#a-note-on-github) — but it is not required.)

---

## The easiest path (recommended)

### Step 1 — Get the files onto your computer (no account needed)

1. Go to the repo page: **`https://github.com/Loringtonian/second-brain-template`**
2. Click the green **`< > Code`** button.
3. Click **Download ZIP**.
4. Find the downloaded file (usually in your **Downloads** folder) and unzip it —
   **Mac:** double-click it. **Windows:** right-click → **Extract All…** → **Extract**
   (double-clicking only peeks *inside* the zip without really unpacking it). You'll get a
   folder named `second-brain-template-main`. Move it somewhere you'll find again — your
   **Documents** folder is fine.

That's the whole "getting the code" step. No [terminal](GLOSSARY.md#terminal-command-line), no
commands.

### Step 2 — Install the Claude Desktop app

1. Download the Claude app for Mac or Windows from **https://claude.com/download** and install
   it like any other app. (Step-by-step walkthrough:
   https://code.claude.com/docs/en/desktop-quickstart · Linux has no Desktop app — use the
   [terminal path](#prefer-the-terminal-claude-code-command-line) below.)
2. Open it and **sign in** with your Claude account.
3. Click the **Code** tab at the top.
4. Choose **Local**, then **Select folder**, and pick the folder you unzipped in Step 1.
   - **Windows only:** local sessions need **[Git](GLOSSARY.md#git)** installed first — grab it
     from **https://git-scm.com/downloads/win** and click through the installer with the
     defaults. (Macs already include it.)

### Step 3 — Say the magic words

In the message box, type:

> **set up my second brain**

…and press Enter. From here a guided interview — the **[`/setup`](GLOSSARY.md#slash-command-like-setup)**
skill — takes over. It asks who you are, what you want the brain to do, your writing voice, and
so on, and it quietly handles every technical bit (installing small helper programs, creating
files) **for you**. Just answer its questions and approve its changes as it suggests them.
Claude asks permission before each step — some approval boxes show technical-looking commands;
clicking **Allow** is exactly the "approving" this guide means, not something you need to understand.

**That's it.** ~20 minutes gets you a working core. See [what to expect](#what-to-expect-after-setup).

---

## Other ways

You don't need these if the path above worked — they're for people who prefer a different tool.

### Prefer the terminal? Claude Code (command line)
One-time install, then one command:
- **Mac:** in your [terminal](GLOSSARY.md#terminal-command-line), run `curl -fsSL https://claude.ai/install.sh | bash`
- **Windows:** in PowerShell, run `irm https://claude.ai/install.ps1 | iex`

Then move into the unzipped folder and start Claude:
```
cd path/to/second-brain-template-main
claude
```
Type **`/setup`** and press Enter.

### Web portal (claude.ai on the web, or ChatGPT/Codex in a browser)? **Not the way to set this up.**
This template is built for a **local** AI assistant. The web portal requires a
[GitHub account](GLOSSARY.md#github-account) *and* this repo already pushed to **your own**
GitHub — the Download-ZIP path above simply doesn't apply there. And because a web session runs
in a cloud [sandbox](GLOSSARY.md#sandbox), some of the template's local automation may behave
differently than it does on your machine. **Use the Claude Desktop app (above) or the terminal
version ([CLI](GLOSSARY.md#cli-command-line-interface)) instead.** Once your brain is set up
locally, you can still chat with it from anywhere.

### Using OpenAI's Codex (or another AI agent)?
This template is **Claude-native** — the `/setup` shortcut and some automation are Claude Code
features. A different agent can still use it: there's an **[AGENTS.md](AGENTS.md)** at the repo
root written for exactly this case. Open the folder in your agent and tell it:
*"Read AGENTS.md and set up my second brain."* Heads-up: deeper features (automatic hooks,
semantic search) may need a **rebuild** for your tool — and if you do that work, please **fork
the repo and contribute it back** (see **[CONTRIBUTING.md](CONTRIBUTING.md)**). We'd love this
to grow into a community project.

---

## A note on GitHub

[GitHub](GLOSSARY.md#github) is just the website that hosts these files. You can grab them with
no account (the ZIP in Step 1). But a **free GitHub account** is worth making, because it lets
you:
- **Get updates** easily as the template improves, instead of re-downloading the ZIP each time.
- **Contribute** your own skills and fixes back (see [CONTRIBUTING.md](CONTRIBUTING.md)).

Make one in ~2 minutes at **https://github.com/signup**. Then you can [fork](GLOSSARY.md#fork)
the repo to keep your own copy, or use the web path above.

---

## What to expect after setup

- The repo ships **blank on purpose.** Empty identity docs and `__FILL_FROM_USER__`
  placeholders are normal, not broken — they're the spots `/setup` fills with *your* life.
- `/setup`'s ~20-minute core fills the important parts (who you are, what it's for) — and ends by
  running your **first real capture loop**, so you see the brain actually work before the session ends.
- Curious what this whole system is *for*? Read **[INTENT_SPEC.md](INTENT_SPEC.md)** — the one-page
  "why" the rest of the repo serves. `/setup` fills its Owner Intent section with *your* answers.
- The **other ~140 placeholders are breadcrumbs** that fill in gradually as you add real content —
  they are **not** homework you must finish before the brain is useful.
- Lost on a word? → **[GLOSSARY.md](GLOSSARY.md)**
- Want to help build this? → **[CONTRIBUTING.md](CONTRIBUTING.md)**

Welcome to your second brain.
