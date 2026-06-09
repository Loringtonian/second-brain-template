# AGENTS.md — Working inside `.claude/skills/`

> Read the root **[`/AGENTS.md`](../../AGENTS.md)** first for the full picture. (Codex only
> loads *this* file when you are operating inside `.claude/skills/` — otherwise the root one
> applies.)

Each subfolder here is a **skill**: a `SKILL.md` plus an optional `references/` folder. In
Claude Code these run as slash commands (`/setup`, `/process-content`, …). If you are a
different agent you **can't** invoke `/name`, but every `SKILL.md` is a **self-contained
procedure you can read and execute manually**.

- **Start with `setup/SKILL.md`** — the onboarding interview that personalizes the template.
- A skill's frontmatter (`name`, `description`, `allowed-tools`) tells you when it applies and
  which tools it needs.
- **Adding a skill?** Copy this folder pattern and follow **[`/CONTRIBUTING.md`](../../CONTRIBUTING.md)**:
  generic only, no personal data or hardcoded paths, positive framing, degrade gracefully.
