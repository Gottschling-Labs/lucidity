# Phase 6 — Automation Jobs (Heartbeat + Cron)

This document defines the background maintenance automations that keep memory healthy without manual effort.

Principles:
- Prefer **cron** for exact timing and isolation.
- Prefer **heartbeat** for opportunistic batching.
- All maintenance should be **non-destructive** by default (staging-first), with receipts.

---

## Cron jobs

### 1) Nightly dream (transcripts + daily log) + dedupe (staging-first)
Schedule: daily at 04:15 local time

Purpose:
- Extract yesterday’s context from **session transcripts** into a T2-like snapshot (staged).
- Distill yesterday’s T2 daily log (if present) into staged candidates.
- Distill the transcript snapshot into staged candidates.
- Deduplicate staged candidates.
- Produce receipts/reports.

Command:
```bash
python3 memory-architecture/scripts/dream_daily.py --date <YESTERDAY> --tz-offset-minutes <LOCAL_OFFSET>
```

Why this exists:
- The most common failure mode is "we talked about it, but it never made it into memory/YYYY-MM-DD.md".
- Dream mode ensures the pipeline still captures decisions and plans from transcripts.

Safety:
- High-confidence gating is configurable: `memory-architecture/config/auto-merge.json`.
- Auto-merge writes to `memory/topics/` (T3) and emits manifests under `memory/staging/manifests/`.
- Does not modify sensitive-tier content.

---

## Heartbeat tasks

Heartbeat is already configured to advance the project plan; once the architecture project is complete, we repurpose heartbeat to:
- Check if a new daily log exists for yesterday and distill it (staging only)
- Check if staging folder is growing too large and suggest cleanup
- Remind for manual promotion/apply step when staged candidates accumulate

---

## Outputs and audit trail

- Staging outputs: `memory/staging/**`
- Receipts: `memory/staging/receipts/*.json`
- Dedupe report: `memory/staging/reports/dedupe-report.json`

---

## Future enhancement (Phase 6 pruning milestone)
Add a pruning job that:
- archives old staged files
- rotates reports
- keeps a manifest of what was moved
