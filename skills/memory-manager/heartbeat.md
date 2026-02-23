# Lucidity via HEARTBEAT (instead of cron)

Cron is best when you want **exact timing** (e.g., nightly at 03:45). Heartbeat is best when you want to **batch work** and reduce background jobs.

## Recommended approach

- Keep **backups** on cron (safety + predictable retention)
- Run **distill + dedupe** on heartbeat (cheaper + fewer always-on schedules)
- Run **apply** (merge into `MEMORY.md`) either:
  - manually on-demand, or
  - heartbeat-gated (only when you’re around to review), or
  - cron in `--require-review` mode for the first week

## Minimal HEARTBEAT checklist

Add something like this to your `~/.openclaw/workspace/HEARTBEAT.md`:

- If API rate limits allow:
  - Run staging-only distillation (non-destructive)
  - Run staged dedupe/canonicalization
  - If the user explicitly approved: run apply (idempotent) + emit receipts

## Why this works

The Lucidity pipeline is **staging-first**. Heartbeat execution just changes *when* it runs — it does not change the safety model.

## Further reading

- `memory-architecture/automation-jobs.md`
- `memory-architecture/require-review.md`
- `memory-architecture/backup-policy.md`
