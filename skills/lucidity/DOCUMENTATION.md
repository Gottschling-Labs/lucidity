# Lucidity — Comprehensive Documentation

This document is the “full manual” for Lucidity.

If you want the fast path, start with:
- `README.md` (repo root)
- `skills/lucidity/README.md`

---

## 1) Concepts

### 1.1 Goals

Lucidity is designed to:

- Improve **recall quality** across sessions (retrieve the right context reliably)
- Reduce **token cost** (inject smaller, higher-signal snippets instead of entire files)
- Maintain **auditability** (every transform has receipts/manifests)
- Preserve **reversibility** (backups + rollback)
- Minimize privacy risk via **staging-first** and **consent/PII defaults**

### 1.2 Memory tiers (T2–T4)

Lucidity’s tier naming matches the architecture docs in `skills/lucidity/memory-architecture/`.

At a practical level in OpenClaw workspaces:

- **T4 (Curated long-term):** `MEMORY.md`
  - Stable: preferences, decisions, durable facts
  - Small and high-signal

- **T2/T3 (Near-term / topical / procedural):** files under `memory/`
  - Larger, more granular, time-scoped
  - Used as source material for distillation into T4

> Note: tier boundaries are organizational. Actual retrieval is driven by search over file paths.

---

## 2) How recall works in OpenClaw

OpenClaw recall is typically implemented as:

1) A **pre-answer recall step** runs (e.g., `memory_search`).
2) The recall step searches **`MEMORY.md` + `memory/*.md`**.
3) The agent injects the most relevant snippets into the prompt with a tight budget.

Lucidity supports this by:

- Keeping `MEMORY.md` small and curated (high signal)
- Keeping near-term notes structured so snippets are easy to retrieve
- Defining a prompt injection policy (what to include, where, and how much)

References:
- `skills/lucidity/memory-architecture/prompt-injection-policy.md`
- `skills/lucidity/memory-architecture/hybrid-retrieval-policy.md`

---

## 3) The maintenance pipeline

Lucidity’s pipeline is **staging-first**:

### 3.1 Distill (daily → staged candidates)

Purpose:
- Convert raw daily notes into structured memory candidates.

Command:

```bash
python3 skills/lucidity/memory-architecture/scripts/distill_daily.py \
  --workspace ~/.openclaw/workspace \
  --staging-only
```

Outputs:
- Writes into `memory/staging/…`
- Produces receipts linking sources → outputs

### 3.2 Dedupe / canonicalize staging

Purpose:
- Remove duplicates, normalize phrasing, unify canonical entries.

Command:

```bash
python3 skills/lucidity/memory-architecture/scripts/dedupe_staging.py \
  --workspace ~/.openclaw/workspace
```

Outputs:
- `memory/staging/deduped/…`
- `memory/staging/reports/…`

### 3.3 Apply (optional) — merge into `MEMORY.md`

Purpose:
- Promote only high-confidence, non-time-bound, safe items into curated long-term memory.

Command (example):

```bash
python3 skills/lucidity/memory-architecture/scripts/apply_staging.py \
  --workspace ~/.openclaw/workspace
```

Safety properties:
- Makes backups first
- Writes manifests/receipts
- Designed to be **idempotent** (reruns should not duplicate content)

### 3.4 Backup & rollback

Backups:

```bash
python3 skills/lucidity/memory-architecture/scripts/backup_memory.py \
  --workspace ~/.openclaw/workspace
```

Rollback (restore from pre-apply backups/manifests):

```bash
python3 skills/lucidity/memory-architecture/scripts/rollback_apply.py \
  --workspace ~/.openclaw/workspace
```

References:
- `skills/lucidity/memory-architecture/backup-policy.md`

---

## 4) Cron vs Heartbeat operation

### 4.1 Cron (recommended default)

Best when:
- You want predictable timing (nightly backups, consistent staging maintenance)

Install:

```bash
cd skills/lucidity
./install.sh
```

Default cron installs:
- nightly backup
- staging-only distill
- staging dedupe

> Apply is intentionally *not* enabled by default.

### 4.2 Heartbeat

Best when:
- You want to batch maintenance with other checks
- You want human-in-the-loop review before apply

Instructions:
- `skills/lucidity/heartbeat.md`

---

## 5) Verification / “How do I know it works?”

Minimum verification checklist:

1) Run distill → confirm staging files created.
2) Run dedupe → confirm deduped staging + report exists.
3) Run apply (optional) → confirm `MEMORY.md` updated AND manifests/receipts recorded.
4) Re-run apply → confirm no duplicates (idempotency).

References:
- `skills/lucidity/memory-architecture/test-scenarios.md`
- `skills/lucidity/memory-architecture/test-results.md`
- `skills/lucidity/memory-architecture/eval-harness.md`

---

## 6) Security / privacy notes

- Keep secrets out of always-loaded files.
- Prefer staging-first + review for the first week of a new install.
- Sensitive tier guidance is included in the architecture docs.

References:
- `skills/lucidity/memory-architecture/sensitive-tier-encryption.md`
- `skills/lucidity/memory-architecture/require-review.md`
- `skills/lucidity/memory-architecture/SANDBOXING.md` (if present in your version)
