# Robustness Addendum - QA Test Plan

This plan verifies correctness, safety, and idempotency of the memory-manager pipeline.

## Scope
- Distill: `distill_daily.py`
- Dedupe: `dedupe_staging.py`
- Apply: `apply_staging.py`
- Prune: `prune_staging.py`
- Telemetry: `state/memory-recall-events.jsonl`

## Test categories

### 1) Idempotency (no duplicates)
**Goal:** Running the same operation twice produces no additional canonical changes.

- Apply idempotency:
  1. Prepare a deduped topic candidate with one high-confidence procedural block.
  2. Run apply with `--write`.
  3. Run apply with `--write` again.
  4. Expect: canonical topic file hash unchanged after the 2nd run; manifest shows 0 net new blocks.

- Distill idempotency (staging):
  - Re-running distill on the same daily log should not create repeated duplicate blocks if receipts already exist (may require future enhancement).

### 2) Duplicate-prevention regression
- Ensure merge keying works even when whitespace differs.
- Ensure block normalization is stable.

### 3) Safety gates
- Candidate contains token-like string → must be blocked.
- Candidate contains "BEGIN PRIVATE KEY" → must be blocked.
- Ensure sensitive tier files are never indexed or injected.

### 4) Rollback readiness
- Every apply run must write a manifest.
- Rollback plan test (once rollback command exists): apply then rollback returns file hashes to pre-apply state.

### 5) Backup
- Verify backup archive created daily.
- Verify retention policy removes/archives correct generations.

### 6) Observability
- `/memory-stats` shows:
  - last cron run
  - last apply manifest
  - staging sizes
  - applied/skipped totals

### 7) Performance
- Measure `memory_search` latency on a representative corpus.
- Target: <200 ms median on the gateway host (document hardware and corpus size).
