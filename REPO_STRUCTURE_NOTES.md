# Repo structure notes

This file records the outcome of Lucidity's repo-structure cleanup.

## Resolved decision

Lucidity previously had two overlapping trees:

- top-level `memory-architecture/`
- `skills/lucidity/memory-architecture/`

That duplication has now been resolved in favor of the skill-bundle copy.

## Canonical paths

- Treat **`skills/lucidity/` as the installable/distributable surface**.
- Treat **`skills/lucidity/memory-architecture/` as the canonical runtime/docs tree** for Lucidity architecture docs, scripts, and config.
- Keep top-level docs focused on repo overview, roadmap, governance, and contributor guidance.

## Why this matters

This avoids contributor confusion about:
- which path is canonical
- where new docs/scripts should be edited
- which files are part of the installable skill bundle versus broader repo documentation

## Historical note

The reasoning behind this cleanup is preserved in `STRUCTURE_ASSESSMENT-memory-architecture.md`.
