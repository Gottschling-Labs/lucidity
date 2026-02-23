# Gottschling Labs - Lucidity

Lucidity is a **local-first memory architecture + maintenance toolkit** for OpenClaw.

It organizes memory into tiers and provides a staged pipeline:

1) **Distill** daily notes into structured candidates (staging)
2) **Dedupe/canonicalize** staging
3) (Optional) **Apply** vetted candidates into `MEMORY.md` (curated long-term)
4) Always emit **receipts**, keep **backups**, and support **rollback**

## What’s in this repo

- `skills/lucidity/` - the OpenClaw skill bundle (what you install)
  - `DOCUMENTATION.md` - comprehensive manual (concepts, pipeline, retrieval model)
  - `memory-architecture/` - full design docs + scripts + policies
  - `install.sh` - cron-based install (recommended default)
  - `heartbeat.md` - how to run it via HEARTBEAT instead

## Installation (cron, recommended)

```bash
cd skills/lucidity
./install.sh
```

This will:
- ask for consent + PII minimization defaults
- create required workspace directories under `~/.openclaw/workspace/`
- install cron entries for maintenance + backups

## Installation (heartbeat)

If you prefer batching work into heartbeats (lower overhead, less rigid timing):

1. Read: `skills/lucidity/heartbeat.md`
2. Copy the provided checklist into your `HEARTBEAT.md`
3. Disable cron jobs (or set them to staging-only)

## Full documentation

- `skills/lucidity/DOCUMENTATION.md`

## Tier architecture (T0-T4)

Lucidity uses a tiered model to keep memory **cheap, auditable, and useful**:

- **T0:** foundation (always-loaded identity/safety)
- **T1:** working context (short-lived)
- **T2:** daily logs (append-only)
- **T3:** topic briefs (compressed)
- **T4:** curated long-term (`MEMORY.md`)

See: `skills/lucidity/memory-architecture/tier-design.md`.

## LLM + configuration dependencies

Lucidity’s scripts are local-first, but `memory_search` recall depends on OpenClaw **memory indexing** (memory-core) with **embeddings + vector search** and **FTS** enabled.

Verify indexing health:

```bash
openclaw status --deep
```

You should see the memory plugin reporting `vector ready` and `fts ready`.

See:
- `skills/lucidity/memory-architecture/indexing-inputs.md`
- `skills/lucidity/memory-architecture/hybrid-retrieval-policy.md`

## How recall works (T2/T3 vs T4)

OpenClaw recall is driven by **searching files**, not by a tier "switch".

- **T4**: `MEMORY.md` (curated long-term, stable facts / preferences / decisions)
- **T2/T3**: files under `memory/` (near-term episodic + topic/procedural notes)

Lucidity works because:
- your agent runs a recall step (e.g., `memory_search`) before answering memory-dependent questions
- `memory_search` searches `MEMORY.md` + `memory/*.md` so tier files are eligible
- the prompt injection policy limits how much content gets injected and prefers higher-signal snippets

See: `skills/lucidity/memory-architecture/prompt-injection-policy.md`.

## Verification

See:
- `skills/lucidity/memory-architecture/test-scenarios.md`
- `skills/lucidity/memory-architecture/test-results.md`
- `skills/lucidity/memory-architecture/eval-harness.md`

## License

GPL-3.0-or-later (see `../../LICENSE`).

Private (for now).