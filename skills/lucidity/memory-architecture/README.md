# Memory Architecture (Tiered Hybrid Memory)

This folder is the operations and design deck for the OpenClaw memory architecture project.

## What this is
A **local-first**, **auditable**, tiered memory system:
- **T0**: foundational always-loaded Markdown (identity, safety, user prefs)
- **T1**: working context (lightweight state)
- **T2**: daily logs (append-only)
- **T3**: topic briefs (compressed, maintained)
- **T4**: curated long-term memory (durable facts)

Key design principle: **Markdown is the source of truth**; search and automation are helpers.

---

## Quick start (how to use)

### Daily log (T2)
Write events to:
- `workspace/memory/YYYY-MM-DD.md`

### Distill (staging-only)
Generate candidates from a daily log:

```bash
python3 memory-architecture/scripts/distill_daily.py --path memory/2026-02-16.md
```

Outputs (staged):
- `memory/staging/topics/*.md`
- `memory/staging/receipts/*.json`
- `memory/staging/MEMORY.candidates.md`

### Dedupe (staging-only)

```bash
python3 memory-architecture/scripts/dedupe_staging.py --write
```

Outputs:
- `memory/staging/deduped/**`
- `memory/staging/reports/dedupe-report.json`

### Apply (auto-merge, high-confidence)
Auto-merge deduped staging candidates into canonical topic briefs (and later curated memory), gated by a configurable "high-confidence" policy.

Dry run:

```bash
python3 memory-architecture/scripts/apply_staging.py --dry-run
```

Write:

```bash
python3 memory-architecture/scripts/apply_staging.py --config memory-architecture/config/auto-merge.json --write
```

Outputs:
- `memory/staging/manifests/apply-*.json`

### Prune staging (archive-only)
Dry run:

```bash
python3 memory-architecture/scripts/prune_staging.py --days 14
```

Apply moves:

```bash
python3 memory-architecture/scripts/prune_staging.py --days 14 --write
```

Outputs:
- `memory/archive/staging/YYYY/MM/...`
- manifest: `memory/archive/staging/YYYY/MM/manifests/*.json`

---

## Documents (index)

### Plan
- `PROJECT_PLAN.md`

### Tier design + schemas
- `tier-design.md`
- `memory-schemas.md`
- `tier-rules.md`

### Retrieval
- `indexing-inputs.md`
- `hybrid-retrieval-policy.md`
- `recall-tracking-model.md`

### Compression
- `distillation-pipeline.md`
- `dedupe-canonicalization.md`

### RAG + integration
- `prompt-injection-policy.md`
- `integration-sessions-compact.md`

### Automation
- `automation-jobs.md`

### Pruning
- `pruning-policy.md`

### Testing
- `test-scenarios.md`
- `test-results.md`

---

## Automation
A nightly cron job (staging-only) runs distill + dedupe.
See `automation-jobs.md` for details.

---

## Safety
- Canonical memory files (`MEMORY.md`, `memory/YYYY-MM-DD.md`, `memory/topics/*.md`) are never modified automatically by these scripts.
- Staging-first + receipts/manifests are required for auditability.
