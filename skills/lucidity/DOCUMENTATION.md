# Lucidity - Comprehensive Documentation

This document is the "full manual" for Lucidity.

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

### 1.2 Memory tiers (T0-T4)

Lucidity’s tier naming matches the architecture docs in `skills/lucidity/memory-architecture/`.

At a practical level in OpenClaw workspaces:

- **T0 (Foundation, always-loaded):** stable identity + operating constraints
  - Examples: `SOUL.md`, `USER.md`, `IDENTITY.md`, `AGENTS.md`, `TOOLS.md`
  - Keep small and stable; no secrets.

- **T1 (Working context, short-lived):** what you are actively doing right now
  - Examples: `HEARTBEAT.md` and other local-only coordination files
  - Should decay quickly; prefer structured state where possible.

- **T2 (Daily logs, append-only):** raw chronological record of what happened
  - Example: `memory/YYYY-MM-DD.md`

- **T3 (Topic briefs, compressed):** maintained summaries by topic or project
  - Example: `memory/topics/<topic>.md`
  - Should cite back to T2 for auditability.

- **T4 (Curated long-term):** stable facts, preferences, and durable decisions
  - Example: `MEMORY.md`
  - Small and high-signal.

> Note: tier boundaries are organizational. Actual retrieval is driven by search over file paths.

Canonical spec: `skills/lucidity/memory-architecture/tier-design.md`.

---

## 2) LLM + configuration dependencies

Lucidity is intentionally **local-first**. Most of the functionality (distill/dedupe/apply/backups/rollback) runs as local scripts.

However, **high-quality recall** depends on your OpenClaw deployment configuration:

### 2.1 OpenClaw memory indexing (`memory-core`)

To enable `memory_search` and `memory_get` retrieval, OpenClaw must have the **memory-core plugin** enabled and healthy.

Practical expectations:
- OpenClaw maintains an indexed corpus of chunks derived from eligible files (commonly `MEMORY.md` and `memory/*.md`).
- The index supports:
  - **Vector (embeddings) search** for semantic similarity
  - **FTS** (full-text search) for exact/keyword matching

#### How to verify indexing is healthy

On the host running OpenClaw:

```bash
openclaw status --deep
```

You should see the memory plugin reporting something equivalent to:
- `plugin memory-core` enabled
- `vector ready`
- `fts ready`

If you do not see that, verify your OpenClaw configuration enables memory-core and has an embeddings provider configured. (Exact configuration varies by deployment.)

If indexing is disabled or unhealthy:
- Lucidity maintenance pipelines still produce well-structured Markdown files.
- But retrieval will not work via `memory_search`; you will need to manually open files in prompts.

See:
- `skills/lucidity/memory-architecture/indexing-inputs.md`
- `skills/lucidity/memory-architecture/hybrid-retrieval-policy.md`

### 2.2 LLM dependencies (where models matter)

- **Embeddings model:** required for semantic vector search (part of memory-core).
- **Chat model:** used by your agent to decide when to run recall, which snippets to cite, and whether to promote candidates into curated memory (if you allow apply).

Lucidity does not hardcode a specific provider/model, but it assumes:
- embeddings are configured and available to memory-core
- your agent can call `memory_search` before answering memory-dependent questions

## 3) How recall works in OpenClaw

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

### 3.1 How episodic and procedural memories get created

Lucidity does **not** magically create memories just because tiers exist. It creates structured episodic/procedural content via the **distillation pipeline**.

Source input (most common):
- Raw daily notes in `memory/YYYY-MM-DD.md`

Generation mechanism:
- `distill_daily.py` reads the raw notes and produces **structured candidates** in `memory/staging/…`.
- `dedupe_staging.py` canonicalizes and de-duplicates those staged candidates.
- Optionally, `apply_staging.py` promotes only high-confidence, durable items into `MEMORY.md` (T4).

What makes something "episodic" vs "procedural" is the **schema** + **heuristics** used during distillation.

- **Episodic** candidates typically capture: what happened, when, who/what was involved, decisions/outcomes, and any follow-ups.
- **Procedural** candidates typically capture: a reusable workflow/SOP, commands, preconditions, expected output, and known pitfalls.

Where to see the exact formats:
- `skills/lucidity/memory-architecture/memory-schemas.md`

Where to see the distillation pipeline rules/flow:
- `skills/lucidity/memory-architecture/distillation-pipeline.md`
- `skills/lucidity/memory-architecture/scripts/distill_daily.py`

> Important: for retrieval, the only hard requirement is that the resulting Markdown ends up under paths searched by recall (typically `MEMORY.md` and `memory/*.md`).

### 3.2 `memory_search` vs `memory_get`

These are designed to be used together:

- **`memory_search(query)`**: discovery. It searches across eligible memory sources and returns the best matching snippets (think "search results").
- **`memory_get(path, from, lines)`**: precision. It fetches a specific slice of a specific file once you know where the relevant content is (think "open the source around these lines").

Practical reasons to use both:
- `memory_search` is broad/ranked; `memory_get` is narrow/controlled.
- `memory_get` helps you pull enough surrounding context without loading an entire file into the prompt.

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

### 3.3 Apply (optional) - merge into `MEMORY.md`

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

## 5) Examples (episodic vs procedural)

These examples show how a raw daily note can be distilled into structured candidates that are easy to retrieve via `memory_search`.

### 5.1 Episodic example

**Raw daily note (source)** - `memory/2026-02-23.md` (example):

- Met with BD proposal team about RFP response workflow.
- Decision: standardize compliance matrix format for all RFPs.
- Follow-up: ask Alex for the latest template and update our checklist.

**Distilled episodic candidate (staging output)** (illustrative):

- **Type:** episodic
- **When:** 2026-02-23
- **What:** Discussed RFP response workflow with BD proposal team
- **Decision:** Standardize compliance matrix format
- **Follow-ups:** Request latest template from Alex; update checklist

Why this helps retrieval:
- The "decision" and "follow-ups" become explicit fields/phrases that are easy to match.

### 5.2 Procedural example

**Raw daily note (source)** (example):

- To install Lucidity: run `./install.sh`, then test with `distill_daily.py --staging-only` and `dedupe_staging.py`.

**Distilled procedural candidate (staging output)** (illustrative SOP):

- **Type:** procedural
- **Title:** Install Lucidity and run first staging maintenance
- **Prereqs:** python3, crontab
- **Steps:**
  1. `cd skills/lucidity`
  2. `./install.sh`
  3. `python3 memory-architecture/scripts/distill_daily.py --workspace ~/.openclaw/workspace --staging-only`
  4. `python3 memory-architecture/scripts/dedupe_staging.py --workspace ~/.openclaw/workspace`
- **Verify:** staging files exist under `memory/staging/` and a dedupe report exists under `memory/staging/reports/`.

Why this helps retrieval:
- If you later ask "how do I install Lucidity?" or "what command runs staging distill?", `memory_search` can find this SOP quickly.

## 6) Verification / "How do I know it works?"

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
