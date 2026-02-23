# Demo workspace (sanitized)

This folder is a tiny, sanitized OpenClaw workspace corpus for validating Lucidity without using private data.

## What it is

- Example `MEMORY.md` and `memory/YYYY-MM-DD.md` content.
- Safe to commit.
- Intended for:
  - verifying distill + dedupe behavior
  - verifying basic retrieval expectations once indexed

## What it is not

- It is not your real workspace.
- It should not contain any secrets or private identifiers.

## How to use

Run the Lucidity scripts against the demo daily log.

From `skills/lucidity/`:

```bash
cd skills/lucidity

# 1) Distill the demo daily log (writes to memory/staging under skills/lucidity/)
python3 memory-architecture/scripts/distill_daily.py \
  --path demo-workspace/memory/2026-02-23.md

# 2) Dedupe staging (dry-run by default; add --write to materialize deduped outputs)
python3 memory-architecture/scripts/dedupe_staging.py

# 3) (Optional) Apply staging (use --dry-run first)
python3 memory-architecture/scripts/apply_staging.py --dry-run
```

Then inspect:
- `skills/lucidity/memory/staging/`

Notes:
- The current scripts treat `skills/lucidity/` as the workspace root.
- The `demo-workspace/` folder is a sanitized input corpus.

