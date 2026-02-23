# Lucidity

Lucidity is a **local-first, auditable memory architecture** for OpenClaw deployments.

It provides:

- A tiered memory model (near-term episodic/topic/procedural → curated long-term)
- Staging-first maintenance pipelines (distill → dedupe → optional apply)
- Backups + rollback + receipts/manifests for reversibility
- A documented recall + prompt-injection policy to stay token-efficient

## Where to start

- **Installable skill bundle:** `skills/memory-manager/`
  - `skills/memory-manager/README.md` (install + verification)
  - `skills/memory-manager/install.sh` (cron-based default)
  - `skills/memory-manager/heartbeat.md` (heartbeat-based alternative)

## How recall works (T2/T3 vs T4)

OpenClaw recall is driven by **searching files** (e.g., `memory_search`) and injecting only the most relevant snippets.

- **T4:** `MEMORY.md` (curated long-term)
- **T2/T3:** files under `memory/` (more granular, shorter-horizon)

Lucidity’s job is to keep those tiers well-structured and easy to retrieve.

## What is `mission-control/ops-notes`?

This folder is **internal operations notes** created during development (a lightweight “captain’s log”).

- `mission-control/ops-notes/distilled/` contains short, dated writeups of key decisions/lessons.
- `mission-control/ops-notes/tools/` contains small utilities for indexing those notes.

It’s included primarily for maintainers who want context on why things are designed the way they are.

## Repo structure (high level)

- `skills/memory-manager/` — the distributable OpenClaw skill bundle
- `memory-architecture/` — source project docs (historical; the skill bundle includes a copy)
- `mission-control/ops-notes/` — maintainer notes (design/ops context)

## Status

Private repo for now (Gottschling Labs). Public release should follow a security + sandboxing review.
