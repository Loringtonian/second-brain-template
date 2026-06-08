---
name: disk-cleanup
description: >-
  Recurring internal-disk cleanup. Phase 1 itemizes regenerable caches,
  local-LLM model stores (HuggingFace / Ollama / LM Studio), dev toolchain
  versions, and Docker — every item shown with its size, deleted only on explicit
  per-item confirmation. Phase 2 (optional, runs when an external drive is
  present) tars the big archival folders (Claude backups, audio recordings) to
  the external drive, verifies entry counts, then deletes the originals.
  Use when user says "/disk-cleanup", "clean up my disk", "disk cleanup",
  "free up space", "my laptop is full", "internal disk is full", or asks for the
  recurring every-few-weeks cleanup. Phase 1 is safe to run alone; Phase 2 needs
  the external drive plugged in.
user_invocable: true
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# disk-cleanup

Recurring internal-disk cleanup. Two phases. Phase 1 (caches + model stores +
toolchain + Docker) always runs. Phase 2 (tar big folders to external, then
delete) runs only when an external drive is connected.

This skill **itemizes everything** — every candidate is presented with its size
and deleted only after the user confirms that specific item or an explicit list.
Honor the itemize-everything approach over batch-confirm shortcuts.

> **Calibrate this at `/setup`.** It ships working on safe defaults, but it's
> precise once it knows *your* disk and what to protect: your internal disk size,
> the external drive Phase 2 archives to, and any production local model that must
> never be deleted. The `/setup` machine-&-environment phase records that in your
> machine profile (`CLAUDE.md` `__FILL_FROM_USER__:machine_profile`) and at
> `__FILL_FROM_USER__:production-ollama-model` below. Until then, everything is
> itemized and confirmed per item, so it's safe to run uncalibrated.

## Hard rules

- **Never delete without itemized confirmation.** Present each candidate with its
  path and size. The user approves per item or names an explicit list. No "delete
  all caches" shortcut.
- **Protect any production model flagged as KEEP.** If a specific Ollama model is
  designated a production model (e.g., a vision model backing an active pipeline),
  list it as KEEP — never as a deletion candidate. `__FILL_FROM_USER__:production-ollama-model`
- **Phase 2 uses `tar`, never `rsync`.** macOS ships rsync 2.6.9, which has no
  incremental file list and copies hardlinks as full file copies. Claude Code
  backup folders are hardlink-dense (Claude Code dedups `shell-snapshots/` and
  session file-history via hardlinks). Observed once: a 22 GB source expanded to
  259 GB on the destination and was still unfinished after 3.5 hours. The same
  data via `tar -cf` finished in ~8 minutes. Always tar.
- **Verify entry counts before deleting any backed-up original.**
  `find <src> | wc -l` must equal `tar -tf <archive> | wc -l`. No match → do not
  delete; investigate.
- **Keep the laptop on the charger during Phase 2.** A tar of tens of GB takes
  several minutes; a battery cutoff mid-write corrupts the in-flight archive.
- **`df -H /` is misleading on Apple Silicon Macs.** It reports the sealed read-only
  system snapshot (~18 GB). The real number is the Data volume. Use
  `diskutil apfs list` → "Capacity In Use By Volumes" and `du` on `~`.

## Phase 0 — Scan and baseline

```bash
df -H /
diskutil apfs list | grep -E "Capacity (In Use|Not Allocated)"
du -d 1 -h ~ 2>/dev/null | sort -hr | head -25
du -d 1 -h ~/.cache ~/Library/Caches "~/Library/Application Support" 2>/dev/null | sort -hr | head -20
```

Record free space now; report the delta at the end.

## Phase 1 — Itemized cleanup (always runs)

Work category by category. For each: gather the candidate list with sizes,
present a table to the user, get confirmation, delete only confirmed items, then
run `df -H /` to show the delta.

### 1A — Regenerable caches

These all regenerate on next use; the only cost of deleting is a one-time
re-fetch. Still itemize each with its current size:

| Candidate | Path | How to clear |
|---|---|---|
| `__pycache__` dirs | `~/Desktop`, `~/Documents` | `find ... -type d -name __pycache__ -prune -exec rm -rf {} +` |
| npm cache | `~/.npm` | `npm cache clean --force` |
| Homebrew cache + orphans | `~/Library/Caches/Homebrew` | `brew cleanup -s && brew autoremove` |
| pip cache | `~/.cache/pip` | `rm -rf ~/.cache/pip/*` |
| HuggingFace xet (chunk) cache | `~/.cache/huggingface/xet` | `rm -rf ~/.cache/huggingface/xet` |
| conda package cache | `~/miniconda3/pkgs` | `conda clean --all --yes` |
| Claude desktop VM bundle | `~/Library/Application Support/Claude/vm_bundles` | `rm -rf` (re-creates on next use) |
| Claude desktop caches | `~/Library/Application Support/Claude/Cache`, `.../Code Cache` | `rm -rf` |
| Stale app-updater caches | `~/Library/Caches/*ShipIt*`, `*updater*` | `rm -rf` the stale ones |

Get sizes first: `du -sh <each path> 2>/dev/null`. Skip any path that doesn't
exist. Exclude `__pycache__` inside paths the user flags as active — confirm
current active projects before deleting.

### 1B — HuggingFace hub models

```bash
du -sh ~/.cache/huggingface/hub/* 2>/dev/null | sort -hr
```

Auto-flag obvious junk for deletion (still confirm): `tmp*` orphan files,
0-byte / metadata-only stubs. Itemize every real model with its size; the user
picks. Guidance to offer, not enforce: embedding models in active use (`bge-*`,
`nomic-embed-*`, `all-MiniLM-*`) and whisper variants are usually worth keeping;
large image-gen checkpoints (e.g. SDXL) are often superseded by ComfyUI — ask.

### 1C — Ollama models

```bash
ollama list
```

Itemize each with size and last-modified age. Any model explicitly designated
KEEP (see hard rules above) must never appear as a candidate. For the rest, flag
anything not used in months and let the user decide. Delete with
`ollama rm <name>`.

### 1D — Dev toolchain

```bash
ls ~/.pyenv/versions/ 2>/dev/null
ls ~/.nvm/versions/node/ 2>/dev/null
conda env list 2>/dev/null
which python python3 && python3 --version
```

Itemize. Flag end-of-life Pythons (2.7, 3.7, 3.8, anything past EOL) and Node
versions that are not the current default. Confirm the active versions before
proposing removal. Remove with `pyenv uninstall <v>`, `nvm uninstall <v>`,
`conda env remove -n <env>`.

### 1E — Docker

```bash
docker system df    # needs the daemon running
```

Offer `docker system prune -a --volumes`. Note: the Docker VM disk image does
not shrink even after a prune — reclaiming its full size needs Docker Desktop →
Settings → Reset to factory defaults, which the user should decide on explicitly.

## Phase 2 — Backup-then-delete (optional)

Run only if an external drive is connected. Detect:

```bash
ls /Volumes/ | grep -v "Macintosh HD"
```

No external drive → tell the user Phase 2 is skipped and stop cleanly. Phase 1
results stand on their own.

If a drive is present, confirm which one to use, then for each large archival
folder (default set: `~/.claude-backup-*`, `__FILL_FROM_USER__:large-archival-folder`;
add anything else the user names):

1. **Tar to the external drive.** Destination folder dated, e.g.
   `/Volumes/<drive>/laptop-cleanup-backup-<YYYY-MM-DD>/archives/`.
   ```bash
   tar -cf "<dest>/<name>.tar" -C "$(dirname <src>)" "$(basename <src>)"
   ```
   Run in the background and monitor; tar reads sequentially so it is fast.
2. **Verify.** Counts must match:
   ```bash
   find <src> | wc -l
   tar -tf "<dest>/<name>.tar" | wc -l
   ```
3. **Delete the original only on an exact match.** `rm -rf <src>`. On any
   mismatch, keep the original and report.

Keep the laptop on the charger throughout. If the drive must be ejected:
`sync` first, then `diskutil unmount "/Volumes/<drive>"` (use
`diskutil unmount force` if Spotlight's `mds_stores` holds it).

## Final report

End with: free space before vs after, total reclaimed, what was deleted by
category, and what is now backed up on the external drive (with the archive
paths). If Phase 2 ran, remind the user the originals are gone and the only
copies are the verified tar archives on the external drive.
