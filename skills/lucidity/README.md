# Gottschling Labs - Lucidity

Lucidity is a **local-first, auditable memory system for OpenClaw companions**.

It organizes memory into tiers and provides a staged pipeline across three memory classes — **semantic, procedural, and episodic**:

1) **Distill** daily/session material into structured candidates (staging)
2) **Dedupe/canonicalize** staging
3) (Optional) **Apply** vetted durable candidates into canonical memory
4) Always emit **receipts**, keep **backups**, and support **rollback**

By default, episodic memory is preserved as searchable lower-tier context, while semantic and procedural memory are the main candidates for durable promotion.

## What’s in this repo

- `skills/lucidity/` - the OpenClaw skill bundle (what you install)
  - `DOCUMENTATION.md` - comprehensive manual (concepts, pipeline, retrieval model)
  - `memory-architecture/` - full design docs + scripts + policies
  - `install.sh` - Gateway cron install (recommended)
  - `uninstall.sh` - remove Gateway cron jobs
  - `gateway-cron-install.sh` - deprecated wrapper (back-compat)
  - `gateway-cron-uninstall.sh` - deprecated wrapper (back-compat)
  - `heartbeat.md` - how to run the same maintenance via HEARTBEAT instead of cron

## Installation (Gateway cron, recommended)

Gateway cron jobs are visible to OpenClaw and are the expected user experience.

```bash
cd skills/lucidity
./install.sh
```

This will:
- ask for consent + workspace root
- ask you to choose **Dream Mode** (recommended) or **Custom**
- default routine maintenance runs to **silent** reporting
- enable Dream Mode's backup + distill + reflection + dedupe + autonomous promotion flow by default
- detect timezone from the host when possible
- create Gateway cron jobs visible via `openclaw cron list`

Docs:
- `skills/lucidity/GATEWAY_CRON.md`
- `skills/lucidity/INSTALL.md`
- `skills/lucidity/UPGRADING.md`
- `skills/lucidity/CHAT_COMMANDS.md` (chat command cheat sheet)
- `skills/lucidity/AGENTS_SNIPPET.md` (recommended AGENTS.md additions)

## Installation (heartbeat)

If you prefer batching work into heartbeats (lower overhead, less rigid timing):

1. Read: `skills/lucidity/heartbeat.md`
2. Copy the provided checklist into your `HEARTBEAT.md`
3. Disable cron jobs (or set them to staging-only)

## Full documentation

- `skills/lucidity/DOCUMENTATION.md`
- `skills/lucidity/DREAM_MODE.md` - primary Dream Mode product definition
- `skills/lucidity/AUTO_PROMOTION_POLICY.md` - safe autonomous promotion rules
- `skills/lucidity/anima-interface.md` - Lucidity ↔ Anima boundary and portability contract
- `skills/lucidity/profiles/README.md` - initial runtime/retrieval profile examples

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
- `memory_search` searches `MEMORY.md` + `memory/*.md` so semantic, procedural, and episodic tier files are eligible
- the prompt injection policy limits how much content gets injected and prefers higher-signal snippets

See: `skills/lucidity/memory-architecture/prompt-injection-policy.md`.

## Verification

See:
- `skills/lucidity/memory-architecture/test-scenarios.md`
- `skills/lucidity/memory-architecture/test-results.md`
- `skills/lucidity/memory-architecture/eval-harness.md`

## Community positioning

Near-term, Lucidity should be understood as:

> a local-first, auditable memory system for OpenClaw companions

That means:
- **safe defaults** (staging-first, backups, reversibility)
- **quiet defaults** (silent maintenance unless explicitly announced)
- **simple install story** (install → nightly pipeline → inspect receipts if needed)
- **clear separation of concerns** between Lucidity (memory operations) and future portable identity layers such as Anima

## License

GPL-3.0-or-later (see `../../LICENSE`).

Public, but still pre-1.0.
