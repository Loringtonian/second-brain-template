# Contributing

This template is meant to **grow into a community project**. The architecture is the valuable
part, and it gets better every time someone adds a skill, fixes a doc, or makes it work with a
new tool. Humans *and their AI agents* are welcome to contribute — this file is written for
both.

New here? Read **[START_HERE.md](START_HERE.md)** first to understand what the template does.
Unsure of a word? See the **[GLOSSARY](GLOSSARY.md)**.

---

## The one golden rule: no personal data

This is a **public template**. Everything you contribute must be **generic and reusable** —
nothing from your own life. Before you open a pull request, make sure your changes contain:

- **No real names, private notes, or personal content.** Use placeholders (`__FILL_FROM_USER__`)
  or a fictional persona, the way `examples/` does.
- **No secrets.** No API keys, tokens, or passwords — not even in an example. Those belong in a
  user's own `.env` (which is gitignored).
- **No machine-specific absolute paths** like `/Users/yourname/...`. Use a relative path or an
  environment variable such as `$SECOND_BRAIN_ROOT`.

A quick self-audit before you submit:
```bash
# from the repo root — should return nothing surprising
grep -rinE "your-real-name|/Users/|api[_-]?key *= *['\"][A-Za-z0-9]" .
```

---

## Ways to contribute

- **New skills** — a repeatable task (ingest a new source, a new kind of analysis, a tool
  integration). The biggest win.
- **New hooks** — small automatic behaviors.
- **Docs & glossary** — clearer wording, a missing term, a fix.
- **Examples** — a new synthetic Template A/B/C example.
- **New tool paths** — got this running well on **Codex** or another agent? That rebuild is
  exactly the kind of contribution we want (see the note in [AGENTS.md](AGENTS.md)).

---

## How to contribute (the flow)

1. **[Fork](GLOSSARY.md#fork)** the repo on GitHub (you'll need a free
   [GitHub account](GLOSSARY.md#github-account)).
2. Make your change on a branch in your fork.
3. Run the self-audit grep above; confirm it's generic and leak-clean.
4. Open a **pull request** with a short description of *what* you added and *why*. Small, focused
   PRs get reviewed and merged faster than large ones.

---

## How to add a skill (the pattern)

A skill is just a folder with a `SKILL.md`. Copy the shape of an existing one (good models:
`.claude/skills/setup/`, `.claude/skills/process-content/`).

```
.claude/skills/<your-skill-name>/
  SKILL.md            # required
  references/         # optional — companion docs the skill reads
```

`SKILL.md` starts with frontmatter, then the procedure:
```markdown
---
name: your-skill-name
description: >-
  One or two sentences on what it does AND the phrases a user might say to trigger it
  ("when the user says X, Y, or Z"). This is how the agent decides to run it.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob   # only what it needs
---

# Your Skill — Title

(The procedure, written as instructions to the agent. Keep it prompt-driven and generic —
no personal data, no hardcoded paths. Use positive framing: say what to do, not what to avoid.)
```

If your skill delegates work to sub-agents, follow the **10-slot delegation skeleton** in
`CLAUDE.md` (the "SUB-AGENT DELEGATION" section). Make skills **degrade gracefully**: if a
helper they call isn't installed, fall back to something simpler rather than failing.

---

## For your agent (paste this to the AI helping you contribute)

> You are helping add a contribution to a **public** template repository. Constraints:
> (1) **Generic only** — no real names, private content, secrets/API keys, or machine-specific
> absolute paths; use placeholders or a fictional persona. (2) Follow the existing skill folder
> pattern (`.claude/skills/<name>/SKILL.md` with frontmatter: `name`, `description` including
> trigger phrases, `allowed-tools`). (3) Use **positive framing** in instructions (say what to
> do, not what to avoid). (4) Make it **degrade gracefully** when an optional helper is absent.
> (5) Before finishing, run a leak grep over your changes and confirm it's clean. (6) Produce a
> short PR description: what was added and why. Read `CLAUDE.md` and `START_HERE.md` first for
> the repo's conventions.

---

## What makes a great contribution

- **Generic and reusable** — works for anyone, not just you.
- **Leak-clean** — passes the self-audit above.
- **Follows the conventions** — skill pattern, positive framing, the document templates.
- **Degrades gracefully** — still does *something* useful when an optional dependency is missing.
- **Documented** — a clear description, and a glossary entry if it introduces a new term.

Thank you for helping this grow.
