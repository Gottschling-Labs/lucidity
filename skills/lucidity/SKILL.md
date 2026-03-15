---
name: lucidity
version: 0.4.0
description: "Local-first, auditable Dream Mode memory system for OpenClaw. Semantic, procedural, and episodic memory with staged maintenance, autonomous promotion, receipts, and backups."
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["python3", "bash"]
---

# Lucidity

This skill packages a **safe-autonomous Dream Mode memory system** plus supporting maintenance pipelines for OpenClaw deployments.

## What it does

- Maintains memory in tiers across **semantic, procedural, and episodic** classes
- Produces **staging outputs** first (safe, reviewable)
- Runs **dream/reflection + dedupe/canonicalization** before durable promotion
- Supports autonomous promotion of vetted semantic/procedural memory under strict gating
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

# Preferred (Dream Mode via Gateway-managed cron jobs)
./gateway-cron-install.sh

# Alternative (local install helpers)
# ./install.sh
```

Then run a first maintenance pass (staging-first is safest):

```bash
python3 memory-architecture/scripts/distill_daily.py --staging-only
python3 memory-architecture/scripts/dedupe_staging.py
```

## Safety defaults

- **Dream Mode** is the primary path
- **Backups** before autonomous promotion
- **Idempotent apply** (reruns should not duplicate)
- **Episodic memory** remains lower-tier by default unless distilled into durable insight

## Docs

Start here:
- `README.md`
- `DREAM_MODE.md`
- `AUTO_PROMOTION_POLICY.md`
- `memory-architecture/README.md`
- `memory-architecture/HANDOVER.md`
