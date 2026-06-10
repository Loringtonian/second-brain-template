# Glossary — Plain-English Definitions

Every technical word in this repo, in one friendly sentence. No prior knowledge assumed.
Where a term points at something **`/setup` does for you**, we say so — usually you don't have
to do it by hand.

### GitHub
A website that stores code and files (like this template) so people can download, copy, and
improve them. It lives at [github.com](https://github.com).

### Repository (repo)
One project's folder of files on GitHub. This template is a single repo.

### GitHub account
A free login on GitHub. You **don't** need one to download this template (use *Download ZIP*),
but it's handy for getting updates and contributing back.

### Git
The program that tracks versions of files; GitHub is the website built around it. Macs include
it already; on Windows you install it once from
[git-scm.com/downloads/win](https://git-scm.com/downloads/win) (defaults are fine).

### Clone
Making a copy of a repo onto your computer using Git. If that sounds technical, skip it — just
*Download ZIP* instead.

### Fork
Your *own* copy of someone's repo on GitHub that you can change freely. You fork when you want
to improve the template and offer the changes back.

### Branch
A parallel line of work inside a repo — you make changes on a branch so the main copy stays
untouched until you're ready.

### Pull request
A proposal on GitHub to merge your changes into the original repo. You describe what you changed
and why, and the maintainers review it.

### Download ZIP
The no-account way to get these files: the green **`< > Code`** button on the repo page →
**Download ZIP** → double-click the file to unzip it.

### Terminal (command line)
A text window where you type commands instead of clicking buttons. Powerful — but **you can
avoid it entirely** by using the Claude Desktop app.

### CLI (command line interface)
A program you use by typing commands in a terminal instead of clicking buttons. "The Claude Code
CLI" just means Claude Code run from a terminal.

### PowerShell
Windows' built-in terminal app. Open it by typing "PowerShell" in the Start menu.

### grep
A search command that finds lines of text inside files. When a doc says "grep for X," it means
"search the files for X" — your AI assistant runs it for you.

### Sandbox
A sealed-off workspace where a program runs without touching the rest of your computer. Web and
cloud AI sessions run inside one — safe, but more limited than running locally.

### Claude Code
Anthropic's AI coding assistant: the thing that reads this repo and runs the setup. It comes as
a **Desktop app** (buttons — easiest), a **terminal command**, and a **website**.

### claude.ai (versus Claude Code)
`claude.ai` is the Claude **chat** website. **Claude Code** is the version that can open a
folder and run skills. Plain chat with file uploads can *read* your notes but can't run this
template's automation.

### Claude Desktop app
The Mac/Windows app that bundles Claude Code with a friendly interface — our recommended way to
set this up.

### Codex
OpenAI's AI coding assistant. It can use this template via **[AGENTS.md](AGENTS.md)**, though
some Claude-specific features may need rebuilding.

### Slash command (like `/setup`)
A shortcut you type to make Claude Code run a packaged task. `/setup` runs the onboarding
interview. Just type it and press Enter.

### Skill
A packaged, repeatable task Claude Code knows how to do (e.g. `/setup`, ingest a note). Skills
live in the `.claude/skills/` folder.

### Hook
A small action that fires automatically (e.g. checking a note's format when you save). Optional,
and off by default in this template.

### Python
A common programming language. A few of this template's helper scripts use it. `/setup` installs
what's needed for you.

### pip
Python's tool for installing add-on packages. `/setup` runs it for you — you don't have to.

### Virtual environment (venv)
A private sandbox holding one project's Python add-ons, so they don't clash with anything else
on your computer. `/setup` creates it automatically.

### API key
A secret password that lets the brain use a paid service (e.g. image generation). You paste it
into a `.env` file. Only needed for optional extras.

### .env file
A plain text file holding your secret keys. It's kept out of GitHub so your secrets stay
private. `/setup` creates it for you from `.env.example`.

### Markdown (.md)
A simple way to write formatted text using plain symbols (`#` for a heading, `-` for a bullet).
Every note in this brain is a Markdown file.

### Frontmatter
The small block between `---` lines at the very top of a Markdown file, holding settings — like
a skill's name and description, or a note's `depth:` privacy label.

### Template A / B / C
The three note types. **A** = your own original thinking (kept word-for-word). **B** = someone
else's content (a quote, a clip), always credited. **C** = an AI-written summary made *from*
your own notes.

### depth (`depth: 1–5`)
A privacy label on each note: **1** = fine to share, **5** = most private. It tells the agent
what's safe to show, publish, or hand to another agent.

### Embedding / semantic search
A way to find notes by *meaning* rather than exact words. Optional — until you set it up, search
falls back to plain keyword matching, which still works.

### `__FILL_FROM_USER__`
A placeholder marking a spot for your own content. `/setup` finds and fills the important ones
by interviewing you; the rest fill in over time as you add real notes.

### MEMORY.md
A file holding things the agent should remember about you across sessions. `/setup` creates it
from `MEMORY.example.md`.
