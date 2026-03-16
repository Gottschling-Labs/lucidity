# Lucidity structure assessment — `memory-architecture/` duplication

Date: 2026-03-15

## Summary

Lucidity currently contains two substantially overlapping trees:

- top-level `memory-architecture/`
- `skills/lucidity/memory-architecture/`

This is not a small amount of duplication. It is effectively a **two-tree layout with divergence**.

## Key findings

### 1) The skill-tree copy is the actual runtime/install surface
The install flow and operational docs point at:
- `skills/lucidity/install.sh`
- `skills/lucidity/memory-architecture/scripts/*`
- `skills/lucidity/memory-architecture/config/auto-merge.json`

This means the skill-tree path is the one that actually matters for:
- Gateway cron installation
- chat command references
- CI checks
- most skill-facing documentation

### 2) The top-level tree is not canonical in practice
The root README references top-level `memory-architecture/scripts/*` commands in several places, but the installer and skill docs use the skill-tree paths.

This creates mixed signals:
- contributors may edit top-level files thinking they are canonical
- operators may copy commands from the root README that do not match the actual installed skill surface
- the two trees can continue drifting silently

### 3) The duplication is broad and already divergent
Observed during assessment:
- shared filenames across the two trees: **dozens**
- `diff -rq` shows most overlapping files differ
- the skill-tree copy also contains additional scripts not present top-level, including:
  - `distill_pending.py`
  - `reflect_pending.py`
  - `reflect_apply_candidates.py`
  - `reflect_prompt.md`
  - `sanitize_staging_quotes.py`
  - `staging_sanitizer.py`

This means the top-level tree is not just duplicated — it is also **less complete**.

### 4) The skill tree currently appears to be the safer canonical candidate
Because the skill-tree version is what:
- installer paths use
- CI references
- most current docs reference
- Dream Mode operational instructions rely on

…it is the strongest candidate for **canonical source of truth**.

## Recommendation

## Recommended direction: make `skills/lucidity/memory-architecture/` canonical

Then, in a follow-up restructuring PR:

1. **Treat `skills/lucidity/memory-architecture/` as the canonical source** for:
   - scripts
   - config
   - architecture docs that ship with the skill
   - operational manuals tied to installation/runtime

2. **Reduce or remove top-level `memory-architecture/` duplication** by one of these approaches:

### Option A — remove top-level duplicate tree entirely
Use only the skill-tree path everywhere.

Pros:
- simplest conceptual model
- no future drift
- easiest for contributors

Cons:
- root README / older references must be updated
- some contributor-facing docs may need relocation

### Option B — keep top-level tree as generated or curated mirror
Only if there is a strong packaging/documentation reason.

Pros:
- allows a contributor-facing top-level docs surface

Cons:
- requires generation/sync tooling or a very disciplined process
- otherwise drift will continue

My assessment: **Option A is probably better unless a concrete distribution need argues otherwise.**

## Cleanup outcome

This assessment has now been acted on:

1. root and skill docs were updated to make the canonical path explicit
2. contributor guidance now points feature work at `skills/lucidity/memory-architecture/`
3. stale duplicate planning/handover files were pruned
4. the top-level duplicate `memory-architecture/` tree was removed

Installer behavior, CI checks, and primary docs now align around the skill-tree copy.

## Follow-up focus

Future Lucidity work should build on the resolved structure rather than revisiting duplication:
- feature work goes into `skills/lucidity/memory-architecture/`
- top-level docs should stay repo-oriented
- Dream orchestrator and session-capture work should assume the duplicate-tree cleanup is complete

## Bottom line

This redundancy should eventually be eliminated.

The right approach was not a blind dedupe.
The right approach was:

> declare the canonical tree first, then migrate references and remove the duplicate tree in a focused structural cleanup.

That cleanup is now complete, and `skills/lucidity/memory-architecture/` is the sole canonical tree.
