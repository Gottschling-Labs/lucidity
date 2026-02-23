# Phase 7 - Test Results

Run date: 2026-02-19

## T7.1 - Memory search returns curated facts (T4)
Query: `WSL Ubuntu OpenClaw running in`
Result: PASS
- Returned `MEMORY.md#L1-L9`

Query: `assistant identity name Gordon`
Result: PASS
- Returned `MEMORY.md#L1-L9`

## T7.2 - Memory search returns daily log evidence (T2)
Query: `Ops Deck Stage values Backlog Doing Review Done`
Result: PASS
- Returned `memory/2026-02-16.md#L1-L24`

## T7.3 - Expanded retrieval suite (10 queries)
Target: ≥8/10 PASS

1) Query: `OpenClaw running in WSL Ubuntu`
   - PASS (`MEMORY.md#L1-L9`)
2) Query: `assistant identity name Gordon`
   - PASS (`MEMORY.md#L1-L9`)
3) Query: `Ops Deck Stage values Backlog Doing Review Done`
   - PASS (`memory/2026-02-16.md#L1-L24`)
4) Query: `do not use em dashes writing preferences`
   - PASS (`memory/2026-02-16.md#L19-L34`)
5) Query: `Preferred voice Gordon Freeman Arthur Morgan`
   - PASS (`memory/2026-02-16.md#L19-L34`)
6) Query: `Chrome Relay browser control works occasional timeouts`
   - PASS (`memory/2026-02-16.md#L19-L34`)
7) Query: `TELEGRAM_GORDON_PRIME_BOT_API`
   - PASS (`memory/2026-02-16.md#L19-L34`)
8) Query: `local-only secrets ~/.openclaw/secrets.env EnvironmentFile systemd user unit`
   - PASS (`memory/2026-02-16.md#L1-L24`)
9) Query: `KanikaBK status 2022180444587077882 liked authorized`
   - PASS (`memory/2026-02-16.md#L19-L34`)
10) Query: `SES SMTP email skill path email-smtp`
   - FAIL (no results; likely because phrasing differs and current corpus is small)

Summary: 9/10 PASS

## T7.4 - Distillation script produces staging outputs
Result: PASS (validated earlier)
- `distill_daily.py` created:
  - `memory/staging/topics/*.md`
  - `memory/staging/receipts/2026-02-16.json`
  - `memory/staging/MEMORY.candidates.md`

## T7.5 - Dedupe script produces deduped outputs + report
Result: PASS (validated earlier)
- `dedupe_staging.py --write` created:
  - `memory/staging/deduped/topics/*.md`
  - `memory/staging/reports/dedupe-report.json`

## T7.6 - Prune script writes manifests (dry-run)
Result: PASS
- Dry-run created manifest:
  - `memory/archive/staging/2026/02/manifests/prune-2026-02-19T16:29:06Z.json`
- No files moved (dry-run)
