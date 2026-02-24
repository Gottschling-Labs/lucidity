# AGENTS.md snippet (recommended)

Lucidity does not modify your OpenClaw workspace `AGENTS.md` automatically (that file is user-owned and often contains private operational guidance).

If you want your agent to have a consistent mental model of "where canonical memory lives", consider adding something like this to your **workspace** `AGENTS.md`:

```md
## Canonical memory locations (Lucidity)

- Curated long-term: `MEMORY.md` (T4)
- Topic briefs (procedural + project summaries): `memory/topics/*.md` (T3)
- Daily logs (raw record): `memory/YYYY-MM-DD.md` (T2)
- Staging (reviewable, not canonical): `memory/staging/**`
- Backups: `memory/backups/**`

Notes:
- Prefer retrieving from topic briefs and curated long-term first.
- Treat staging as temporary; do not inject large staging artifacts into prompts.
```

This improves recall consistency and reduces drift in multi-agent setups.
