# Memory Architecture - Handover & Operating Guide

This is the practical checklist for running the tiered memory system day-to-day.

## What is "done" vs "future"
Done in this project:
- Tier definitions (T0-T4) + schemas
- Hybrid retrieval policies (vector + FTS) documented
- Recall tracking model documented (JSONL schema)
- Staging-first distillation + dedupe + pruning scripts implemented
- Nightly cron job for staging-only maintenance
- Sensitive tier (T‑S) design documented (encryption approach)

Not implemented (by design / deferred):
- Automatic promotion of staged candidates into `MEMORY.md` (T4) (auto-merge currently targets topic briefs first)
- Actual encrypted sensitive-tier tooling (age/gpg) and decrypt/use flows
- Retrieval telemetry wired into the gateway prompt builder

---

## Daily workflow (recommended)

### 1) Capture (T2)
Write important events to today’s daily log:
- `workspace/memory/YYYY-MM-DD.md`

### 2) Nightly staging maintenance (automated)
Cron job runs daily at **04:15 ET**:
- distills yesterday’s daily log into staging
- dedupes staging

Job name: `memory-nightly-distill-dedupe (staging-only)`

### 3) Review staged candidates (manual)
Review:
- `memory/staging/topics/*.md`
- `memory/staging/deduped/topics/*.md`
- `memory/staging/MEMORY.candidates.md`

### 4) Promote (automated + manual override)
By default, promotion can be automated via the nightly cron auto-merge step (high-confidence gated).

Manual override: you can still copy/merge high-signal items yourself:
- Procedures → `memory/topics/<topic>.md`
- Durable facts/preferences → `MEMORY.md`

Rule of thumb:
- If it’s not durable, don’t put it in `MEMORY.md`.
- If it’s not frequently used, don’t put it in T0.

### 5) Archive staging (optional)
To archive old staging artifacts (default retention 14 days), dry run:

```bash
python3 memory-architecture/scripts/prune_staging.py --days 14
```

Then apply:

```bash
python3 memory-architecture/scripts/prune_staging.py --days 14 --write
```

---

## Scripts (staging-only)

Distill a daily log into staging:
```bash
python3 memory-architecture/scripts/distill_daily.py --path memory/YYYY-MM-DD.md
```

Dedupe/canonicalize staging outputs:
```bash
python3 memory-architecture/scripts/dedupe_staging.py --write
```

Archive old staging outputs (no deletion):
```bash
python3 memory-architecture/scripts/prune_staging.py --days 14 --write
```

---

## Safety rules (must keep)
- Never store secrets in `SOUL.md`, `USER.md`, `IDENTITY.md`, `AGENTS.md`, `TOOLS.md`, `MEMORY.md`, or `memory/topics/`.
- Scripts must remain **staging-first**.
- Prefer retrieval snippets over injecting whole files.

---

## Configuration knobs to consider (optional)
- `agents.defaults.compaction.memoryFlush.*` prompts: align with schemas and keep it silent (NO_REPLY).
- `agents.defaults.memorySearch.extraPaths`: only if you intentionally want to index additional Markdown (not logs).

---

## "Sensitive tier" (T‑S) next steps (if you want it)
1) Choose encryption tool: `age` recommended.
2) Decide key management: recipients vs passphrase.
3) Implement explicit flows:
   - store encrypted notes
   - decrypt only on explicit user request
   - never embed sensitive plaintext

See: `memory-architecture/sensitive-tier-encryption.md`.
