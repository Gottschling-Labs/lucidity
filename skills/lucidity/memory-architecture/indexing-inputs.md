# Phase 3 — Memory-core Indexing Inputs (Current State)

This doc records what OpenClaw’s `memory-core` is *currently* indexing on this host, based on inspection of the local memory store.

## Evidence source
- Local memory DB: `~/.openclaw/memory/main.sqlite`
- Status: `openclaw status --deep` reports `plugin memory-core · vector ready · fts ready`.

## Storage model (observed)
The sqlite DB contains:
- `files` table: tracks indexed file paths + hash + mtime + size
- `chunks` table: text chunks with line ranges and associated embedding
- `chunks_fts*` tables: FTS virtual tables for keyword search
- `chunks_vec*` tables: vector index tables for embedding similarity

## Currently indexed files (observed)
From `files` table (`path`, `source`, `size`, `mtime`, `hash`):
- `MEMORY.md` (source=`memory`)
- `memory/2026-02-16.md` (source=`memory`)

## Current chunking (observed)
From `chunks` table (`path`, `start_line`, `end_line`):
- `MEMORY.md`: lines 1–9 (1 chunk)
- `memory/2026-02-16.md`: split into 2 chunks (1–24, 19–34)

Notes:
- Chunk ranges overlap (e.g., 1–24 and 19–34). This is a common retrieval tactic to avoid “boundary loss” across chunks.

## Implications
- `MEMORY.md` is already indexed today — good alignment with the desired future state.
- Index scope appears intentionally narrow: only the curated long-term file + at least one daily log.
- Both vector and FTS are provisioned and share the same chunk corpus.

## Phase-3 followup (policy work)
Next steps (planned milestone): define an explicit include/exclude policy for indexing scope, starting with:
- Include: `MEMORY.md`, `memory/YYYY-MM-DD.md`, `memory/topics/*.md`, selected config/docs (meta-awareness)
- Exclude: `**/node_modules/**`, `**/logs/**`, `**/*.log`, large generated artifacts, `.git`

We will keep **indexing broader than injection** (index for retrieval; inject only minimal T0 + tiny T1 + retrieved snippets).
