#!/usr/bin/env python3
"""Deterministic credential / identity leak guard — the always-on privacy safety net.

A judgment / LLM pass catches SEMANTIC privacy ("this names a partner"); it is unreliable for
hard secrets — sampling routinely misses credential strings that an exhaustive regex catches.
This guard is the complement: a fast, deterministic, exhaustive scan for high-risk patterns
(passport MRZ, bank routing, IBAN, private keys, cloud keys, real password / secret assignments,
national-ID numbers) that flags any file carrying such a pattern while stamped at or below a low
privacy depth.

The rule it enforces: a file holding a CRITICAL pattern must be stamped >= --crit-floor (default 4 —
"Valuable & confidential" in Orientation_Docs/PRIVACY_DEPTH.md). A low-stamped CRITICAL hit is a
privacy FALSE-LOW — the one dangerous error (a private file marked shareable / publishable) — and
exits nonzero so a publish step or weekly sweep can refuse to proceed.

Tiers (by false-positive rate):
  CRITICAL — high-precision, unambiguous: passport MRZ, routing+context, IBAN, private-key header,
             AWS AKIA key, real (non-placeholder) password/secret assignment, national-ID. Low-stamp => leak.
  REVIEW   — FP-prone label hits: bare `password:` / `api_key:` with a placeholder-looking value.
             Surfaced for a human / judgment look, never auto-critical.

Usage:
    python3 scripts/depth_guard.py             # human report; exit 1 if any low-stamp CRITICAL
    python3 scripts/depth_guard.py --json       # machine output (weekly-maintenance consumes this)
    python3 scripts/depth_guard.py --crit-floor 4   # required floor for CRITICAL-bearing files

Repo root resolves from $SECOND_BRAIN_ROOT, else the parent of this scripts/ directory, so the
guard is runnable as-is after cloning. Self-contained — no project-specific dependencies.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SECOND_BRAIN_ROOT") or Path(__file__).resolve().parent.parent)

DEPTH_RE = re.compile(r"^depth:\s*(\d+)\s*$", re.MULTILINE)

# Directories never worth scanning (vendored code, VCS internals, caches).
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".mypy_cache"}

# Values that mean "this is documentation / code / a template, not a real secret".
PLACEHOLDER_RE = re.compile(
    r"^(?:[<\[{\$].*|x{3,}|\*{3,}|\.{3,}|-{3,}|your[_-].*|my[_-].*|changeme|example|sample|test|"
    r"placeholder|redacted|password|passwd|secret|token|admin|user(?:name)?|none|null|todo|"
    r"true|false|string|str|int|integer|bool|boolean|float|object|optional|any|self|the|here|"
    r"fill[_-].*|__fill.*|\$\{.*\}|<.*>|\.\.\..*)$", re.I)


def _clean_token(raw: str) -> str:
    """First real token after a `password:` label, trimmed of markdown emphasis / code wrappers."""
    tok = re.sub(r"^[\s*`_|>~\"']+", "", raw)              # drop leading **, `, |, >, quotes
    tok = re.split(r"[\s`*|~]", tok, 1)[0]                 # first whitespace/markdown-delimited token
    return tok.strip("`'\"*_|.,;)")


def _real_secret(value: str) -> bool:
    """True only when the cleaned value looks like an actual secret, not a placeholder/type/example."""
    v = _clean_token(value)
    if len(v) < 5 or len(v) > 80:
        return False
    if PLACEHOLDER_RE.match(v):
        return False
    if v == v[0] * len(v):            # aaaa / **** / ####
        return False
    # A code expression / env lookup is not a literal secret — e.g.
    # api_key=os.environ.get('X'), pwd=config.get(...), token=process.env.X
    if "(" in v or ")" in v:
        return False
    if re.search(r"environ|getenv|process\.env|\bos\.", v, re.I):
        return False
    return bool(re.search(r"[A-Za-z]", v))


# Assignment label that is `:` or a single `=` (NOT `==`, which is a code comparison).
_ASSIGN = r"(?::|=(?!=))"

# CRITICAL patterns — (name, compiled, validator(match)->bool). Validator None == always real.
# Add your own country's national-ID / tax-ID pattern alongside `national_id` as needed.
CRITICAL = [
    ("passport_MRZ",   re.compile(r"^P[<A-Z][A-Z<]{20,}", re.M), None),
    ("routing_number", re.compile(r"\brouting\s*(?:number|no|#)?\s*[:#]?\s*(\d{9})\b", re.I), None),
    ("iban",           re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){3,7}\b"), None),
    ("private_key",    re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"), None),
    ("aws_akia",       re.compile(r"\bAKIA[0-9A-Z]{16}\b"), None),
    # national_id: a labeled government ID number (e.g. SIN/SSN). Tune the label list to your country.
    ("national_id",    re.compile(r"\b(?:SIN|SSN)\b\s*[:#]?\s*\d{3}[ -]?\d{2,3}[ -]?\d{3,4}\b"), None),
    ("password_assign", re.compile(rf"(?:password|passwd|pwd)\s*{_ASSIGN}\s*(.+)$", re.I | re.M),
     lambda m: _real_secret(m.group(1))),
    ("secret_assign",  re.compile(rf"\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|client[_-]?secret)\b\s*{_ASSIGN}\s*(.+)$", re.I | re.M),
     lambda m: _real_secret(m.group(1))),
]

# REVIEW patterns — surfaced for a look, never auto-critical. Optional validator(match)->bool.
# (Credit-card-shaped digit runs are deliberately NOT here: in prose/transcripts they are almost
#  always noise, so they belong to a human eyeball, not an automated tier.)
REVIEW = [
    ("password_label", re.compile(r"(?:password|passwd|pwd)\s*[:=]", re.I), None),
    ("secret_label",   re.compile(r"\b(?:api[_-]?key|secret[_-]?key|access[_-]?token)\b\s*[:=]", re.I), None),
]


def split_frontmatter(text: str):
    """Return (frontmatter_without_fences, body) or (None, text) if there is no block."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5:]
    return None, text


def read_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def iter_md(root):
    """Yield (relpath, abspath) for every .md file under root, skipping vendored/VCS dirs."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".md"):
                p = os.path.join(dirpath, fn)
                yield os.path.relpath(p, root), p


def stamp_of(text: str):
    fm, _ = split_frontmatter(text)
    if fm:
        m = DEPTH_RE.search(fm)
        if m:
            return int(m.group(1))
    return None  # unstamped => treated as the most dangerous (no floor)


def scan_file(text: str):
    crit, review = set(), set()
    for name, rx, val in CRITICAL:
        for m in rx.finditer(text):
            if val is None or val(m):
                crit.add(name)
                break
    for name, rx, val in REVIEW:
        for m in rx.finditer(text):
            if val is None or val(m):
                review.add(name)
                break
    return sorted(crit), sorted(review)


def scan(crit_floor: int):
    crit_leaks, review_hits = [], []
    for rel, p in iter_md(ROOT):
        text = read_text(p)
        if not text:
            continue
        crit, review = scan_file(text)
        if not crit and not review:
            continue
        d = stamp_of(text)
        if crit and (d is None or d < crit_floor):
            crit_leaks.append({"path": rel, "depth": d, "patterns": crit})
        if review:
            review_hits.append({"path": rel, "depth": d, "patterns": review})
    return crit_leaks, review_hits


def main():
    crit_floor = 4
    if "--crit-floor" in sys.argv:
        try:
            crit_floor = int(sys.argv[sys.argv.index("--crit-floor") + 1])
        except (ValueError, IndexError):
            pass
    crit_leaks, review_hits = scan(crit_floor)

    if "--json" in sys.argv:
        print(json.dumps({
            "crit_floor": crit_floor,
            "critical_leaks": crit_leaks,
            "review_hits": review_hits,
        }, indent=2))
        sys.exit(1 if crit_leaks else 0)

    print("== depth-guard: credential / identity leak scan ==")
    print(f"   root: {ROOT}")
    print(f"   rule: a file with a CRITICAL pattern must be stamped depth >= {crit_floor}\n")
    if crit_leaks:
        print(f"!! {len(crit_leaks)} CRITICAL false-low(s) — secret-bearing file stamped below D{crit_floor}:")
        for r in crit_leaks:
            d = "unstamped" if r["depth"] is None else f"D{r['depth']}"
            print(f"   [{d}] {r['path']}  ({', '.join(r['patterns'])})")
        print(f"\n   Fix: raise each file's depth: to >= {crit_floor} "
              f"(python3 scripts/stamp_depth.py <file> {crit_floor}), or remove the secret.")
    else:
        print(f"   no CRITICAL false-lows — every secret-bearing file is stamped >= D{crit_floor}. clean.")
    if review_hits:
        print(f"\n   {len(review_hits)} REVIEW hit(s) to eyeball (usually doc placeholders):")
        for r in review_hits[:20]:
            d = "unstamped" if r["depth"] is None else f"D{r['depth']}"
            print(f"   [{d}] {r['path']}  ({', '.join(r['patterns'])})")
    sys.exit(1 if crit_leaks else 0)


if __name__ == "__main__":
    main()
