# Robustness Addendum — Automated Backups (7/30/90)

This document defines the automated backup strategy for the modular memory solution.

## Goals
- Create a **pre-maintenance restore point** daily.
- Keep components **semantically together** inside the workspace.
- Provide auditable manifests (hashes + file list).
- Enforce retention: **7 daily / 30 weekly / 90 monthly**.

## Backup scope (workspace-relative)
Included:
- `MEMORY.md` (if present)
- `memory/YYYY-MM-DD.md`
- `memory/topics/**/*.md`
- `memory/staging/**` (candidates, deduped, receipts, reports, manifests)
- `memory/sensitive/**` (ciphertext + receipts only; no decryption performed)

Excluded:
- `memory/backups/**` (avoid recursive backups)
- non-Markdown junk (node_modules/logs do not live under memory/ by default)

## Storage location (bundled)
- `workspace/memory/backups/`

Layout:
- `memory/backups/<YYYY>/<MM>/backup-<timestamp>.tar.gz`
- `memory/backups/<YYYY>/<MM>/backup-<timestamp>.manifest.json`

## Retention policy (7/30/90)
Given backups indexed by their timestamp:
- **Daily set**: keep the most recent **7** backups.
- **Weekly set**: keep the most recent backup for each ISO week, up to **30** weeks.
- **Monthly set**: keep the most recent backup for each month, up to **90** months.

Union of these sets is retained; everything else is pruned.

## Restore
Restoration is manual:
- extract the desired archive into a temp dir
- selectively copy back `MEMORY.md`, `memory/`, etc.

A future milestone adds a guided rollback command.
