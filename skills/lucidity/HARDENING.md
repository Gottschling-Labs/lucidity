# Lucidity - Hardening guide

This document is a best-effort hardening checklist for running Lucidity scripts safely.

Lucidity is local-first by design. The main risk comes from running file-writing scripts against the wrong workspace.

## 1) Threat model (what can go wrong)

- Accidental writes to the wrong workspace root (polluting or overwriting memory files).
- Applying low-quality candidates into canonical memory (noise, drift).
- Leaking sensitive data by committing generated artifacts or indexing sensitive files.
- Supply-chain risk from running arbitrary code as your user.

## 2) Safe execution rules

- Do not run as root.
- Always pass `--workspace <path>` when running scripts.
- Use `--dry-run` for apply/rollback/prune before `--write`.
- Keep backups enabled before enabling automatic apply.
- Keep secrets out of always-loaded tiers (T0/T3/T4).

## 3) Workspace scoping

Recommended workspace roots:
- Production: `~/.openclaw/workspace`
- Demo: `skills/lucidity/demo-workspace`

Lucidity scripts support `--workspace` so that staging stays inside the chosen workspace:
- `memory/staging/**` is always relative to the selected workspace.

## 4) Git hygiene

- Generated artifacts are gitignored:
  - `skills/lucidity/memory/`
  - `skills/lucidity/state/`
  - `skills/lucidity/demo-workspace/memory/staging/`
  - `skills/lucidity/demo-workspace/state/`

Still, do not use `git add -A` blindly. Always review `git status`.

## 5) Indexing hygiene (memory-core)

- Indexing scope should be broader than injection scope, but never include secrets.
- If you enable extra paths for indexing, prefer:
  - stable docs under `skills/lucidity/`
- Avoid:
  - `.git/`, logs, generated staging artifacts, secret stores

See:
- `extra-paths.md`
- `memory-architecture/indexing-inputs.md`

## 6) Automation maturity model

- Stage 0: manual apply only
- Stage 1: scheduled apply as `--dry-run` + review manifests
- Stage 2: scheduled apply as `--write` + backups + monitoring

## 7) Incident response

If memory was polluted or apply went wrong:
- Stop automation (cron/heartbeat).
- Use apply manifests under `memory/staging/manifests/` to identify what changed.
- Roll back using `memory-architecture/scripts/rollback_apply.py` (requires backups).
