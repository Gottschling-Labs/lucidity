---
name: lucidity
version: 0.1.14
description: "Local-first, auditable, tiered memory maintenance + recall policy for OpenClaw. Distill → dedupe → (optional) apply to curated long-term memory, with receipts + backups."
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["python3", "bash"]
---

# Lucidity

This skill packages a **tiered memory architecture** plus **maintenance pipelines** for OpenClaw deployments.

## What it does

- Maintains memory in tiers (episodic → topical → curated long-term)
- Produces **staging outputs** first (safe, reviewable)
- Runs **dedupe/canonicalization** before any merges
- Optionally **applies** vetted staging into `MEMORY.md` (strict gating)
- Emits **receipts/manifests** so every transform is auditable and reversible
- Provides **backup + rollback** tooling

## Layout

- `memory-architecture/` - full documentation + scripts + benchmarks + operating guide
- `gateway-cron-install.sh` - installs Gateway cron jobs + initializes required directories (with consent)
- `gateway-cron-uninstall.sh` - removes Gateway cron jobs
- `heartbeat.md` - how to run the same maintenance via HEARTBEAT instead of cron

## Quick start

```bash
cd skills/lucidity
./gateway-cron-install.sh
```

Then run a first maintenance pass (staging-only is safest):

```bash
python3 memory-architecture/scripts/distill_daily.py --staging-only
python3 memory-architecture/scripts/dedupe_staging.py
```

## Safety defaults

- **No destructive writes** by default (staging-first)
- **Backups** before apply
- **Idempotent apply** (reruns should not duplicate)

## Docs

Start here: `memory-architecture/README.md` and `memory-architecture/HANDOVER.md`.
