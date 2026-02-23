# Gottschling Labs — Lucidity

Lucidity is a **local-first memory architecture + maintenance toolkit** for OpenClaw.

It organizes memory into tiers and provides a staged pipeline:

1) **Distill** daily notes into structured candidates (staging)
2) **Dedupe/canonicalize** staging
3) (Optional) **Apply** vetted candidates into `MEMORY.md` (curated long-term)
4) Always emit **receipts**, keep **backups**, and support **rollback**

## What’s in this repo

- `skills/lucidity/` — the OpenClaw skill bundle (what you install)
  - `memory-architecture/` — full docs + scripts + policies
  - `install.sh` — cron-based install (recommended default)
  - `heartbeat.md` — how to run it via HEARTBEAT instead

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

## How recall works (T2/T3 vs T4)

OpenClaw recall is driven by **searching files**, not by a tier “switch”.

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

Private (for now).