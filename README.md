# Lucidity

Lucidity is a **local-first, auditable memory system for OpenClaw companions**.

It provides:

- A tiered memory model across **semantic, procedural, and episodic** memory
- A staged **Dream Mode** pipeline (dream/distill → reflect → dedupe → autonomous promotion)
- Backups + rollback + receipts/manifests for reversibility
- A documented recall + prompt-injection policy to stay token-efficient

## Quickstart

```bash
git clone https://github.com/Gottschling-Labs/lucidity.git
cd lucidity
cd skills/lucidity

# Recommended: Dream Mode via Gateway cron (jobs visible in OpenClaw)
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

- The installer now presents **Dream Mode** as the primary path.
- Dream Mode is **quiet by default** and includes backup, distill, reflection, dedupe, and autonomous promotion.
- Autonomous promotion should only promote durable **semantic/procedural** memory; **episodic** memory remains searchable in lower tiers by default.
- Keep secrets out of always-loaded tiers.

## Manual runs and inspection

See `skills/lucidity/CHAT_COMMANDS.md` for copy/paste chat commands and a deterministic helper wrapper.

## Autonomous promotion - making memory updates real

Apply is the step that merges deduped staging candidates into canonical memory files:

- Durable **procedural** memory into `memory/topics/*.md`
- High-confidence **semantic** candidates into `MEMORY.md`
- **Episodic** memory remains primarily lower-tier/searchable unless distilled into durable insight

Start with a dry run:

```bash
cd skills/lucidity
python3 memory-architecture/scripts/apply_staging.py --workspace ~/.openclaw/workspace --dry-run
```

Then write:

```bash
python3 memory-architecture/scripts/apply_staging.py --workspace ~/.openclaw/workspace --write
```

## Where to start

- **Installable skill bundle:** `skills/lucidity/`
  - `skills/lucidity/README.md` (install + verification)
  - `skills/lucidity/DOCUMENTATION.md` (comprehensive manual)
  - `skills/lucidity/DREAM_MODE.md` (primary product definition)
  - `skills/lucidity/AUTO_PROMOTION_POLICY.md` (safe autonomous promotion rules)
  - `skills/lucidity/heartbeat.md` (heartbeat-based alternative)
  - `skills/lucidity/CHAT_COMMANDS.md` (chat command cheat sheet)

## Tier architecture (T0-T4)

Lucidity uses a tiered model so you can keep high-signal memory small and cheap, while still retaining an auditable paper trail.

- **T0 - Foundation (always-loaded):** identity, safety rails, stable preferences
- **T1 - Working context (short-lived):** active tasks and near-term coordination
- **T2 - Daily logs (append-only):** raw, chronological record
- **T3 - Topic briefs (compressed):** maintained summaries by topic/project
- **T4 - Curated long-term:** stable facts/decisions that remain true

See the canonical tier spec: `skills/lucidity/memory-architecture/tier-design.md`.

## LLM + configuration dependencies

Lucidity assumes an OpenClaw deployment with:

- **Memory indexing enabled** (OpenClaw `memory-core` plugin) so that `memory_search` can retrieve snippets
- An **embeddings/vector index** available (for semantic retrieval) and **FTS** available (for exact/keyword retrieval)

Verify indexing health:

```bash
openclaw status --deep
```

You should see the memory plugin reporting `vector ready` and `fts ready`.

If memory indexing is disabled, Lucidity’s maintenance scripts still work (dream/distill/dedupe/apply/backups), but recall will be limited to whatever files you manually open into prompts.

## Comparisons and compatibility

Lucidity complements retrieval/index layers such as OpenClaw memory-core or mem0 by keeping Markdown memory canonical, structured, and auditable.

Best practice:
- keep **Markdown as the source of truth**
- let retrieval systems index curated outputs
- avoid dual-writing to multiple canonical memory stores

## Security + sandboxing

Before making Lucidity public, review:
- `skills/lucidity/HARDENING.md`
- `skills/lucidity/SANDBOXING.md`

## License

GPL-3.0-or-later (see `LICENSE`).

## Status

Public, but still pre-1.0 and actively evolving.
