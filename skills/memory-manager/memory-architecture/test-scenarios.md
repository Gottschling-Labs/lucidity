# Phase 7 — Test Scenarios

This file defines a minimal test suite for validating:
- recall quality (semantic + keyword)
- tier correctness (T2/T3/T4 behavior)
- distillation + dedupe pipeline outputs
- safety constraints (no secrets, no canonical mutation)

## Test inventory

### T7.1 — Memory search returns curated facts (T4)
Query: "Where is OpenClaw running?" / "WSL Ubuntu".
Expected: snippet from `MEMORY.md` showing WSL Ubuntu.

### T7.2 — Memory search returns daily log evidence (T2)
Query: something known to exist in `memory/2026-02-16.md`.
Expected: snippet from `memory/2026-02-16.md`.

### T7.3 — Hybrid retrieval handles exact-ish tokens
Query: an exact filename like `openclaw.json`.
Expected: returns a relevant chunk (may fail until extraPaths are configured).

### T7.4 — Expanded retrieval suite (10 queries)
Run 10 queries spanning:
- Setup facts
- Writing preferences
- Ops Deck project details
- Secrets/local-env notes

Expected: ≥8/10 queries return at least one relevant snippet with correct source citation.

### T7.5 — Distillation script produces staging outputs
Action: run `distill_daily.py` against an existing daily log.
Expected:
- `memory/staging/topics/*.md`
- `memory/staging/receipts/<date>.json`
- `memory/staging/MEMORY.candidates.md`

### T7.6 — Dedupe script produces deduped outputs + report
Action: run `dedupe_staging.py --write`.
Expected:
- `memory/staging/deduped/topics/*.md`
- `memory/staging/reports/dedupe-report.json`

### T7.7 — Prune script writes manifests (dry-run)
Action: run `prune_staging.py --days 0` (dry-run).
Expected:
- `memory/archive/staging/<YYYY>/<MM>/manifests/prune-<ts>.json`
- No files moved when `--write` is omitted.

## Recording results
Results are recorded in: `memory-architecture/test-results.md`.
