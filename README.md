# Lucidity

Lucidity is a **local-first, auditable memory architecture** for OpenClaw deployments.

It provides:

- A tiered memory model (near-term episodic/topic/procedural → curated long-term)
- Staging-first maintenance pipelines (distill → dedupe → optional apply)
- Backups + rollback + receipts/manifests for reversibility
- A documented recall + prompt-injection policy to stay token-efficient

## Quickstart

```bash
git clone https://github.com/Gottschling-Labs/lucidity.git
cd lucidity
cd skills/lucidity
./install.sh

# Verify indexing (recommended)
openclaw status --deep

# Run a first staging pass (safe)
python3 memory-architecture/scripts/distill_daily.py --workspace ~/.openclaw/workspace --staging-only
python3 memory-architecture/scripts/dedupe_staging.py --workspace ~/.openclaw/workspace

# Demo corpus run (isolated)
python3 memory-architecture/scripts/distill_daily.py --workspace demo-workspace --path memory/2026-02-24.md
```

## Safe defaults (read this)

- The installer schedules **staging-only** distill + dedupe and daily backups.
- **Apply** is where candidates become canonical memory (topic briefs and/or curated long-term). It is optional and should be human-reviewed for new installs.
- Keep secrets out of always-loaded tiers.

## Apply (promotion) - making memory updates real

Apply is the step that merges deduped staging candidates into canonical memory files:

- Procedural and episodic notes (as configured) into `memory/topics/*.md`
- High-confidence semantic candidates into `MEMORY.md`

Start with a dry run:

```bash
cd skills/lucidity
python3 memory-architecture/scripts/apply_staging.py --workspace ~/.openclaw/workspace --dry-run
```

Then write:

```bash
python3 memory-architecture/scripts/apply_staging.py --workspace ~/.openclaw/workspace --write
```

Automation maturity model:
- Manual apply (recommended first)
- Scheduled apply `--dry-run` + review (first week)
- Scheduled apply `--write` (only after confidence)

## Where to start

- **Installable skill bundle:** `skills/lucidity/`
  - `skills/lucidity/README.md` (install + verification)
  - `skills/lucidity/DOCUMENTATION.md` (comprehensive manual)
  - `skills/lucidity/install.sh` (cron-based default)
  - `skills/lucidity/heartbeat.md` (heartbeat-based alternative)

## Tier architecture (T0-T4)

Lucidity uses a tiered model so you can keep high-signal memory small and cheap, while still retaining an auditable paper trail.

- **T0 - Foundation (always-loaded):** identity, safety rails, stable preferences.
  - Examples: `SOUL.md`, `USER.md`, `IDENTITY.md`, `AGENTS.md`, `TOOLS.md`
- **T1 - Working context (short-lived):** active tasks and near-term coordination.
  - Examples: `HEARTBEAT.md` (and other local-only ops notes in your deployment)
- **T2 - Daily logs (append-only):** raw, chronological record.
  - Example: `memory/YYYY-MM-DD.md`
- **T3 - Topic briefs (compressed):** maintained summaries by topic/project.
  - Example: `memory/topics/<topic>.md`
- **T4 - Curated long-term:** stable facts/decisions that remain true.
  - Example: `MEMORY.md`

See the canonical tier spec: `skills/lucidity/memory-architecture/tier-design.md`.

## LLM + configuration dependencies

Lucidity assumes an OpenClaw deployment with:

- **Memory indexing enabled** (OpenClaw `memory-core` plugin) so that `memory_search` can retrieve snippets.
- An **embeddings/vector index** available (for semantic retrieval) and **FTS** available (for exact/keyword retrieval).

Verify indexing health:

```bash
openclaw status --deep
```

You should see the memory plugin reporting `vector ready` and `fts ready`.

If memory indexing is disabled, Lucidity’s maintenance scripts still work (distill/dedupe/apply/backups), but recall will be limited to whatever files you manually open into prompts.

See also:
- `skills/lucidity/memory-architecture/indexing-inputs.md`
- `skills/lucidity/memory-architecture/hybrid-retrieval-policy.md`

## How recall works (T2/T3 vs T4)

OpenClaw recall is driven by **searching files** (e.g., `memory_search`) and injecting only the most relevant snippets.

- **T4:** `MEMORY.md` (curated long-term)
- **T2/T3:** files under `memory/` (more granular, shorter-horizon)

Lucidity’s job is to keep those tiers well-structured and easy to retrieve.

## OpenClaw-specific vs portable

- OpenClaw-specific:
  - The *agent behavior* (calling `memory_search` / `memory_get` before answering memory-dependent questions).
  - `openclaw status --deep` health checks.
  - Memory indexing (`memory-core`) providing embeddings (vector) + FTS.

- Portable:
  - The Lucidity scripts operate on local Markdown files under a workspace root.
  - Distill, dedupe, apply, backup, rollback, and prune are file transforms with receipts.

## Demo workspace (sanitized)

See `skills/lucidity/demo-workspace/` for a tiny, sanitized corpus you can use to validate Lucidity without touching private data.

## Repo structure (high level)

- `skills/lucidity/` - the distributable OpenClaw skill bundle
- `skills/lucidity/demo-workspace/` - sanitized demo corpus for validation

## License

GPL-3.0-or-later (see `LICENSE`).

## Maintainers

See `MAINTAINERS.md` for the public release checklist and recommended improvements.

## Security + sandboxing

Before making Lucidity public, review:
- `skills/lucidity/HARDENING.md`
- `skills/lucidity/SANDBOXING.md`

## Status

Private repo for now (Gottschling Labs). Public release should follow a security + sandboxing review.
