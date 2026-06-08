#!/usr/bin/env python3
"""
Deterministic Second Brain hygiene checks for /weekly-maintenance.

Read-only. Prints categorized MECHANICAL findings (or --json) for the skill's
triage step. Each check maps to a class of drift the LLM review agents proved
unreliable at catching (self-audit 2026-05-31, run wf_251815d0-be0): they sample
rather than enumerate, so structural parity / link resolution / count drift slip
through. This script enumerates exhaustively; the agents keep the semantic/quality
judgments a script can't make.

Exit code is always 0 — findings are data for triage, not a failure signal.
"""
import os, re, sys, glob, json

REPO = "$SECOND_BRAIN_ROOT"
SB = REPO  # brain content lives at the repo root since the 2026-06-02 flatten
ORI = os.path.join(SB, "Orientation_Docs")
PROJ = os.path.join(SB, "Projects")
SKILLS = os.path.join(REPO, ".claude", "skills")
CLAUDE_MD = os.path.join(REPO, "CLAUDE.md")
MEM_DIR = "$HOME/.claude/projects/<your-project-dir-slug>/memory"
MEMORY_MD = os.path.join(MEM_DIR, "MEMORY.md")

# Native Claude Code loader caps (HARD — over either → silent tail-drop):
# the harness loads first 200 lines OR ~24.4 KiB, whichever hits first.
# "24.4 KB" in the loader warning is KiB: 24.4 * 1024 = 24985.6 bytes (≈ the
# docs' "25KB"). Verified 2026-05-31. We warn HIGH only at the true cap, and
# MEDIUM in a headroom band below it so the weekly sweep flags an approaching
# breach BEFORE the tail actually drops (the budget-discipline the audit asked for).
MEM_NATIVE_BYTE_CAP = 24986   # 24.4 KiB — the real loader limit
MEM_NATIVE_LINE_CAP = 200     # the real loader line limit
MEM_BYTE_WARN = 23500         # headroom band (~1.5 KB before breach) → MEDIUM
# Early-warning band below the native line cap (NOT a loader limit) — gives the
# weekly sweep ~20 lines of runway to consolidate before the hard 200 breaches.
# (Was 150; bumped 2026-06-01 after the terse+merge rewrite, which legitimately
# runs ~150 lines, made the old guideline a permanent false-nag.)
MEM_STYLE_LINE_CAP = 180
# Per-ENTRY length nudge: a `- [slug](file.md)` line this long means a cold pointer
# got re-expanded into a paragraph (detail belongs in the topic file). Safety/nag
# lines legitimately carry payload, so the threshold is generous and the preamble /
# bold session-start lines are excluded (only `- [` link entries are checked).
MEM_LINE_LEN_CAP = 250

findings = []  # (severity, category, message)


def add(sev, cat, msg):
    findings.append((sev, cat, msg))


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def frontmatter_name(text):
    """Return the YAML `name:` value (stripped of quotes) or '' if empty/missing."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None  # no frontmatter at all
    fm = m.group(1)
    nm = re.search(r"^name:\s*(.*)$", fm, re.M)
    if not nm:
        return None
    return nm.group(1).strip().strip('"').strip("'")


# ---------------------------------------------------------------------------
def check_skills_table():
    """CLAUDE.md skills table + count line vs actual .claude/skills/ dirs."""
    dirs = sorted(
        d for d in os.listdir(SKILLS)
        if os.path.isdir(os.path.join(SKILLS, d))
    )
    txt = read(CLAUDE_MD) or ""
    # skills referenced in the table as /skill-name
    documented = set(re.findall(r"`/([a-z0-9][a-z0-9-]+)`", txt))
    documented &= set(dirs)  # only count ones that map to real skill dirs
    missing = [d for d in dirs if d not in documented]
    if missing:
        add("high", "skills-table",
            f"{len(missing)} of {len(dirs)} skills absent from CLAUDE.md table: "
            + ", ".join(missing))
    # count line "~N skills"
    cm = re.search(r"~(\d+)\s+skills", txt)
    if cm:
        stated = int(cm.group(1))
        if abs(stated - len(dirs)) > 5:
            add("medium", "skills-table",
                f"CLAUDE.md says '~{stated} skills' but {len(dirs)} exist on disk")
    # every skill dir has SKILL.md
    for d in dirs:
        if not os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")):
            add("medium", "skills-table", f"skill dir missing SKILL.md: {d}")


# ---------------------------------------------------------------------------
def _resolve_link(src_path, target):
    """Resolve a markdown link target to an absolute path, or None if external/anchor."""
    target = target.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    if target.startswith("@"):
        # @X -> REPO/X (flat repo root) ; @~/X -> home
        t = target[1:]
        if t.startswith("~/"):
            return os.path.expanduser(t)
        return os.path.join(REPO, t)
    if target.startswith("/"):
        return target  # absolute
    if target.startswith("~"):
        return os.path.expanduser(target)
    return os.path.normpath(os.path.join(os.path.dirname(src_path), target))


def check_doc_links():
    """Resolve markdown links + @imports in high-traffic docs; flag dead/malformed."""
    docs = [CLAUDE_MD]
    docs += sorted(glob.glob(os.path.join(ORI, "*.md")))
    for top in sorted(glob.glob(os.path.join(PROJ, "*"))):
        if not os.path.isdir(top):
            continue
        for fn in ("ORIENTATION.md", "STATE.md", "README.md", "CLAUDE.md"):
            p = os.path.join(top, fn)
            if os.path.isfile(p):
                docs.append(p)
        docs += glob.glob(os.path.join(top, "TODO*.md"))
    link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for d in docs:
        txt = read(d)
        if txt is None:
            continue
        for ln, line in enumerate(txt.splitlines(), 1):
            for tgt in link_re.findall(line):
                if "](" in tgt:  # nested, skip
                    continue
                if tgt.startswith(".../"):
                    add("high", "dead-link",
                        f"{d}:{ln} malformed '.../' path: {tgt}")
                    continue
                resolved = _resolve_link(d, tgt)
                if resolved is None:
                    continue
                if not os.path.exists(resolved):
                    add("medium", "dead-link", f"{d}:{ln} unresolved link: {tgt}")


# ---------------------------------------------------------------------------
def check_intent_inventory():
    """Scan Projects/*/INTENT_SPEC.md vs INTENT_SPEC_INVENTORY.md claims."""
    inv = os.path.join(ORI, "INTENT_SPEC_INVENTORY.md")
    txt = read(inv)
    if txt is None:
        add("medium", "intent-spec", "INTENT_SPEC_INVENTORY.md not found")
        return
    on_disk = {}
    for top in sorted(glob.glob(os.path.join(PROJ, "*"))):
        p = os.path.join(top, "INTENT_SPEC.md")
        if os.path.isfile(p):
            head = "\n".join((read(p) or "").splitlines()[:20]).upper()
            on_disk[os.path.basename(top)] = (
                "UNOFFICIAL" if "UNOFFICIAL" in head else "OFFICIAL?"
            )
    # entries the inventory names with a `Projects/X/INTENT_SPEC.md` path whose
    # spec file is absent on disk. Scoped to the Projects/ prefix so the regex
    # does not false-positive on prose mentions of non-Projects paths
    # (e.g. the meta-root `INTENT_SPEC.md`, which is tracked
    # separately and is not a Projects/ subdir).
    # dict.fromkeys dedups while preserving order — a project named in two
    # inventory rows should flag once, not once per mention.
    for proj in dict.fromkeys(re.findall(r"`Projects/([A-Za-z0-9_]+)/INTENT_SPEC\.md`", txt)):
        if proj not in on_disk:
            add("medium", "intent-spec",
                f"inventory lists Projects/{proj}/INTENT_SPEC.md but no such file on disk")
    # internal table-vs-detail consistency for bucket (d)
    dm = re.search(r"\(d\).*?\|\s*(\d+)\s*\|", txt)
    dlist = re.search(r"\(d\)\s+\*\*FULL UNOFFICIAL DRAFT\*\*.*?(?=\n\(e\)|\n---)", txt, re.S)
    if dm and dlist:
        listed = len(re.findall(r"^\d+\.\s", dlist.group(0), re.M))
        if int(dm.group(1)) != listed:
            add("medium", "intent-spec",
                f"bucket (d) summary count={dm.group(1)} but detail list has {listed}")
    # staleness of the "Last rewritten" date
    if re.search(r"Last rewritten 2026-04", txt):
        add("low", "intent-spec",
            "INTENT_SPEC_INVENTORY 'Last rewritten' date is April — likely stale")


# ---------------------------------------------------------------------------
def check_memory_hygiene():
    """Memory frontmatter names, wikilink resolution, index integrity, orphans."""
    files = [f for f in glob.glob(os.path.join(MEM_DIR, "*.md"))
             if os.path.basename(f) != "MEMORY.md"]
    name_slugs, file_slugs = set(), set()
    for f in files:
        slug = os.path.basename(f)[:-3]
        file_slugs.add(slug)
        txt = read(f) or ""
        nm = frontmatter_name(txt)
        if nm == "" or nm is None:
            add("medium", "memory",
                f"{f} has empty/missing frontmatter name: field")
        elif nm:
            name_slugs.add(nm)
    valid = name_slugs | file_slugs
    def norm(s):
        return s.lower().replace("-", "_").removesuffix(".md")
    valid_norm = {norm(v): v for v in valid}
    # wikilink resolution. A dangling [[link]] is only an ERROR when it is a
    # case/separator/.md-suffix variant of a real slug (a typo). A link with no
    # variant match is a sanctioned forward-reference per the memory design
    # ("a [[name]] that doesn't match yet is fine") — informational, not a defect.
    for f in files:
        for ln, line in enumerate((read(f) or "").splitlines(), 1):
            for wl in re.findall(r"\[\[([^\]]+)\]\]", line):
                if wl in valid:
                    continue
                hit = valid_norm.get(norm(wl))
                if hit:
                    add("medium", "memory",
                        f"{f}:{ln} misnamed wikilink [[{wl}]] -> should be [[{hit}]]")
                else:
                    add("low", "memory",
                        f"{f}:{ln} forward-ref wikilink [[{wl}]] (no target yet — ok per design)")
    # MEMORY.md index integrity + orphans
    mem = read(MEMORY_MD) or ""
    indexed = set()
    for tgt in re.findall(r"\]\(([A-Za-z0-9_./-]+\.md)\)", mem):
        slug = os.path.basename(tgt)[:-3]
        indexed.add(slug)
        if not os.path.exists(os.path.join(MEM_DIR, tgt)):
            add("medium", "memory", f"MEMORY.md index link to missing file: {tgt}")
    # Orphans = topic files in the dir with NO index line. These are REGROWTH
    # SEEDS: there is no native re-indexer, but the *model* re-adds any un-indexed
    # topic file it finds (reproduced 2026-06-01), silently re-bloating MEMORY.md.
    # MEDIUM (not LOW) so /weekly-maintenance acts on it. Resolution is a judgment
    # call (index it with a terse line, OR move/merge it out of the dir), so the
    # script flags rather than auto-fixes. See feedback_memory_hygiene memory.
    orphans = sorted(file_slugs - indexed)
    if orphans:
        add("medium", "memory",
            f"{len(orphans)} memory topic file(s) have NO MEMORY.md index line "
            f"(REGROWTH SEED — add a terse index line, or move/merge the file out of "
            f"the memory dir): " + ", ".join(orphans[:12]) + ("…" if len(orphans) > 12 else ""))


def check_memory_budget():
    mem = read(MEMORY_MD)
    if mem is None:
        add("medium", "memory-budget", "MEMORY.md not found")
        return
    lines = mem.splitlines()
    nbytes = len(mem.encode("utf-8"))
    # Native HARD caps first — over either means the tail actually drops at load.
    if nbytes > MEM_NATIVE_BYTE_CAP:
        add("high", "memory-budget",
            f"MEMORY.md is {nbytes} bytes — OVER the ~{MEM_NATIVE_BYTE_CAP}-byte "
            f"(24.4 KiB) native loader cap; the tail silently drops at session start")
    elif nbytes > MEM_BYTE_WARN:
        add("medium", "memory-budget",
            f"MEMORY.md is {nbytes} bytes — within {MEM_NATIVE_BYTE_CAP - nbytes} "
            f"bytes of the ~{MEM_NATIVE_BYTE_CAP} native cap; consolidate before it breaches")
    if len(lines) > MEM_NATIVE_LINE_CAP:
        add("high", "memory-budget",
            f"MEMORY.md is {len(lines)} lines — OVER the {MEM_NATIVE_LINE_CAP}-line "
            f"native loader cap; lines past {MEM_NATIVE_LINE_CAP} drop at session start")
    elif len(lines) > MEM_STYLE_LINE_CAP:
        add("low", "memory-budget",
            f"MEMORY.md is {len(lines)} lines (over the file's own ~{MEM_STYLE_LINE_CAP}-line "
            f"style guideline, but under the {MEM_NATIVE_LINE_CAP}-line native cap)")
    # Only `- [` link-entry lines (skip the preamble + bold session-start lines,
    # which are intentionally long).
    longs = [i + 1 for i, l in enumerate(lines)
             if l.lstrip().startswith("- [") and len(l) > MEM_LINE_LEN_CAP]
    if longs:
        add("low", "memory-budget",
            f"{len(longs)} MEMORY.md entry lines exceed {MEM_LINE_LEN_CAP} chars "
            f"(a cold pointer re-expanded into a paragraph? lines "
            f"{', '.join(map(str, longs[:8]))}{'…' if len(longs) > 8 else ''})")


# ---------------------------------------------------------------------------
# Light, enumerated cross-doc contradiction checks. Deep/novel contradictions
# stay the LLM agents' job — this is only the known-pairs guard rail.
def check_doc_contradictions():
    phase2 = read(os.path.join(ORI, "PHASE_2_VISION.md")) or ""
    state = read(os.path.join(ORI, "STATE_OF_SECOND_BRAIN.md")) or ""
    if re.search(r"Status:\s*PLANNED\s*-\s*Not yet implemented", phase2, re.I):
        if re.search(r"Phase 2.*ACTIVE", state, re.I) or re.search(r"\*\*Phase 2\*\*.*ACTIVE", state):
            add("medium", "doc-contradiction",
                "PHASE_2_VISION.md says 'PLANNED - Not yet implemented' but "
                "STATE_OF_SECOND_BRAIN marks Phase 2 ACTIVE")


# ---------------------------------------------------------------------------
def main():
    as_json = "--json" in sys.argv
    for fn in (check_skills_table, check_doc_links, check_intent_inventory,
               check_memory_hygiene, check_memory_budget,
               check_doc_contradictions):
        try:
            fn()
        except Exception as e:  # a broken check must not abort the sweep
            add("low", "checker-error", f"{fn.__name__} raised {type(e).__name__}: {e}")

    if as_json:
        print(json.dumps(
            [{"severity": s, "category": c, "message": m} for s, c, m in findings],
            indent=2))
        return

    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get(f[0], 9), f[1]))
    counts = {s: sum(1 for f in findings if f[0] == s) for s in ("high", "medium", "low")}
    print("== weekly-maintenance deterministic checks ==")
    print(f"   {len(findings)} findings  "
          f"(high {counts['high']} / medium {counts['medium']} / low {counts['low']})\n")
    cur = None
    for sev, cat, msg in findings:
        if cat != cur:
            print(f"\n### {cat}")
            cur = cat
        print(f"  [{sev.upper()}] {msg}")
    if not findings:
        print("  clean — no mechanical drift detected.")


if __name__ == "__main__":
    main()
