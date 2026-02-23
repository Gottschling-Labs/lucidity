# Phase 6 — Automation Jobs (Heartbeat + Cron)

This document defines the background maintenance automations that keep memory healthy without manual effort.

Principles:
- Prefer **cron** for exact timing and isolation.
- Prefer **heartbeat** for opportunistic batching.
- All maintenance should be **non-destructive** by default (staging-first), with receipts.

---

## Cron jobs

### 1) Nightly distill + dedupe + auto-merge (high-confidence)
Schedule: daily at 04:15 local time

Purpose:
- Distill yesterday’s T2 daily log into staged candidates.
- Deduplicate staged candidates.
- Auto-merge **high-confidence** candidates into canonical topic briefs.
- Produce reports/manifests.

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
