# Token, cost, and memory hygiene (OpenClaw field notes)

Date: 2026-02-16
Tags: research, cost, tokens, memory, ops

## What matters

OpenClaw already has the bones of a cost disciplined system. The trick is to make it boring.

1) Keep routine turns small.
- Heartbeats should batch checks.
- Cron should handle exact timing.
- Spawn sub agents for long tasks so the main chat stays lean.

2) Treat memory like a file system, not a brain.
- Daily notes are raw and disposable.
- MEMORY.md is curated and should stay short.
- If you want it to survive a restart, write it down.

3) Build an audit trail before you build features.
- Log what ran, what changed, what it cost.
- Keep it local first.
- Only sync distilled, reviewable summaries into the repo.

## Practical routing rules

A cheap model can carry the water if the task is one of these:
- simple file edits
- formatting and copy rewrites
- grep and small refactors
- running a build and fixing obvious errors

A stronger model earns its keep when the task is one of these:
- messy debugging across multiple files
- API design choices with long tail consequences
- security sensitive changes
- research synthesis with conflicting sources

## Memory hygiene cadence

Daily:
- write raw notes to memory/YYYY-MM-DD.md
- promote only confirmed facts to MEMORY.md

Weekly:
- prune MEMORY.md
- consolidate duplicates
- drop volatile details that did not pay rent

## Ops Deck implications

If Ops Deck is going to be the cockpit, it needs three views:
- Distilled Notes: index, tags, search, markdown render
- Receipts: what the agent did, plus cost and diffs
- Queue: approval needed ideas and risk calls

