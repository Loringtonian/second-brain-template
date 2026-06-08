---
name: html-tweaker
description: Launch the HTML Tweaker — direct-manipulation styling for LLM-generated HTML. Drag an HTML file in, fiddle sliders/toggles/color pickers for CSS custom properties, swap between aesthetic presets (Cockpit / Manuscript / Ares), and export either the restyled HTML or a Claude Code skill bundle that makes future generations match the chosen taste. Use when user says "/html-tweaker", "tweak this html", "style this html", "open html tweaker", "design playground", "I want to adjust this", or asks to fiddle/tune/restyle an LLM-generated HTML artifact.
allowed-tools: Bash, Read, Edit, Write
---

# HTML Tweaker — Launch

## What this does

Starts a tiny local HTTP server in `Projects/Design_System/HTML_Tweaker/`,
opens the tool in a browser, and prints the URL. The tool itself is a
single-file HTML app at `Projects/Design_System/HTML_Tweaker/index.html`.

## When to invoke

- User says `/html-tweaker`
- User says "tweak this HTML" / "restyle this HTML" / "open the tweaker"
- User has an LLM-generated HTML artifact and wants to taste-tune it without
  re-prompting
- User is iterating on the Design System and wants to define / refine their
  light or dark mode token preferences
- Just after generating a new HTML artifact, if the user mentions wanting
  to tune the aesthetic

## How to run

1. Check whether port `8901` is already serving. If yes, just open the
   browser at the existing URL:

   ```bash
   lsof -i :8901 -t
   ```

2. If not, start the server in the background:

   ```bash
   cd $SECOND_BRAIN_ROOT/Projects/Design_System/HTML_Tweaker
   python3 -m http.server 8901
   ```

   (Use `run_in_background: true` on the Bash tool — the server should stay
   up across calls.)

3. Open in your browser (`__FILL_FROM_USER__:browser_open_command`, e.g. `open -a Firefox http://localhost:8901/`):

   ```bash
   # __FILL_FROM_USER__:browser_open_command
   open -a Firefox http://localhost:8901/
   ```

4. Print the URL so it can be re-opened if the tab closes:

   > HTML Tweaker is running at http://localhost:8901/

## Optional: load a specific HTML file

If the user invoked the skill with a path argument, e.g.
`/html-tweaker Inventions/Bits/Some_Category/Artifacts/foo.html`, copy
that file into `HTML_Tweaker/samples/` (create the dir if needed) and tell
the user to use the "Open HTML…" button or drag the file from Finder onto
the preview. The tool reads files via the browser FileReader API — no path
needs to be passed to the URL.

## Stopping the server

If the user is done and wants to free the port:

```bash
lsof -i :8901 -t | xargs kill
```

Only do this if explicitly asked.

## Notes

- The tool has no build step. The single dependency (Tweakpane) loads from
  CDN — first run needs internet.
- The "Claude skill bundle" export writes three files (`SKILL.md`,
  `tokens.css`, `tokens.json`). If the user wants those installed somewhere
  specific in the Second Brain or another project, ask where, then move
  them after they're downloaded to `~/Downloads/`.
- This skill does NOT modify any HTML files automatically. All edits happen
  inside the running browser app; the user manually exports.
