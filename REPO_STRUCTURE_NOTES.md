# Repo structure notes

This file records a known structural oddity in the current Lucidity repository:

- top-level `memory-architecture/`
- `skills/lucidity/memory-architecture/`

At the moment these trees substantially overlap rather than cleanly splitting responsibilities.

## Why this matters

This can confuse contributors about:
- which path is canonical
- where new docs/scripts should be edited
- which files are part of the installable skill bundle versus broader repo documentation

## Current recommendation

Until a deeper restructuring pass is done:
- treat **`skills/lucidity/` as the installable/distributable surface**
- treat top-level docs carefully and avoid duplicating new content in both places unless intentional
- do not attempt broad deduplication without confirming how installation and packaging depend on the current layout

## Follow-up assessment needed

A dedicated structural assessment should answer:
1. Should top-level `memory-architecture/` become the canonical source with skill-bundle copies generated from it?
2. Should `skills/lucidity/memory-architecture/` become canonical and top-level duplicates be removed?
3. Which files are actually required for install/runtime vs contributor documentation only?
4. Can duplication be reduced without breaking installer paths, docs links, or packaging expectations?

Until that assessment is complete, prefer **targeted doc fixes** over broad directory moves.
