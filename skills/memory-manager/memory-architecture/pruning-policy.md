# Phase 6 — Pruning Without Data Loss

This document defines safe pruning/rotation rules for the **staging area** and maintenance artifacts.

Scope (for now):
- `memory/staging/**`

Non-goals (until Phase 7/8):
- deleting canonical memory (`MEMORY.md`, `memory/YYYY-MM-DD.md`, `memory/topics/*.md`)

Principles:
- Prefer **archive** over delete.
- Keep **manifests** (what moved, when, hashes).
- Never touch canonical tiers automatically.

---

## What gets pruned

### 1) Staging deduped outputs
- `memory/staging/deduped/**`

### 2) Staging topic candidates
- `memory/staging/topics/**`

### 3) Receipts + reports
- `memory/staging/receipts/*.json`
- `memory/staging/reports/*.json`

### 4) MEMORY candidates
- `memory/staging/MEMORY.candidates.md`
- `memory/staging/deduped/MEMORY.candidates.md` (if present)

---

## Retention defaults

- Keep the last **14 days** of staging artifacts in-place.
- Archive anything older than **14 days**.

Rationale:
- Recent staging artifacts are actively reviewed.
- Older artifacts become noise but should remain recoverable.

---

## Archive layout

Archive root:
- `memory/archive/staging/<YYYY>/<MM>/...`

Example:
- `memory/archive/staging/2026/02/topics/openclaw.md`
- `memory/archive/staging/2026/02/receipts/2026-02-16.json`

Each archive run produces a manifest:
- `memory/archive/staging/<YYYY>/<MM>/manifests/<run-ts>.json`

Manifest contains:
- moved file list
- source path → dest path
- file size
- mtime
- sha256

---

## Safety checks

Before moving a file:
- ensure destination directory exists
- compute sha256
- move (rename) within the filesystem
- verify destination exists

Never:
- delete without archiving
- prune outside `memory/staging/**`

---

## Tooling
Implemented by:
- `memory-architecture/scripts/prune_staging.py`

This tool is safe to run repeatedly.
