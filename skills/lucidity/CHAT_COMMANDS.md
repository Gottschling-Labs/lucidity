# Lucidity - Chat commands (manual)

Lucidity does not require a special bot integration to use from chat.

These are **copy/paste chat commands** you can send to your OpenClaw agent. They are intended to be deterministic, safe-by-default, and to always specify a workspace.

> Note: These commands rely on the agent having host exec access. In OpenClaw, the agent typically runs these scripts on the same host where the workspace lives.

## Conventions

- Always include `--workspace ~/.openclaw/workspace` for production.
- Prefer dry runs before writes.

## Status / health

"Lucidity status"

- Verifies that memory-core indexing looks healthy
- Prints Lucidity workspace stats (last backup/apply, staging sizes)

Suggested message:

```text
lucidity status
```

## Staging (safe)

Distill pending (catch-up):

```text
lucidity distill pending
```

Dedupe staging:

```text
lucidity dedupe --write
```

## Apply (promotion)

Dry run apply:

```text
lucidity apply --dry-run
```

Write apply (promotes into canonical memory):

```text
lucidity apply --write
```

## Backup

```text
lucidity backup --write
```

## Prune staging (archive old staging artifacts)

Dry run:

```text
lucidity prune --days 14
```

Write:

```text
lucidity prune --days 14 --write
```

## Deterministic execution helper (recommended)

If you want the agent to execute chat commands in a deterministic way, you can have it run:

- `skills/lucidity/scripts/lucidity_chat.py`

Examples:

```bash
python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace status
python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace distill-pending --limit 7
python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace dedupe --write
python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace apply --dry-run
python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace backup --write
python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace prune --days 14 --write
```

## What the agent should execute (reference)

If you prefer direct script invocation, these chat commands map to:

- status:
  - `openclaw status --deep`
  - `python3 skills/lucidity/memory-architecture/scripts/memory_stats.py --workspace ~/.openclaw/workspace`
- distill pending:
  - `python3 skills/lucidity/memory-architecture/scripts/distill_pending.py --workspace ~/.openclaw/workspace --limit 7`
- dedupe:
  - `python3 skills/lucidity/memory-architecture/scripts/dedupe_staging.py --workspace ~/.openclaw/workspace --write`
- apply:
  - `python3 skills/lucidity/memory-architecture/scripts/apply_staging.py --workspace ~/.openclaw/workspace --dry-run|--write`
- backup:
  - `python3 skills/lucidity/memory-architecture/scripts/backup_memory.py --workspace ~/.openclaw/workspace --write`
- prune:
  - `python3 skills/lucidity/memory-architecture/scripts/prune_staging.py --workspace ~/.openclaw/workspace --days N --write`
