# Phase 4 — Dedupe + Canonicalization

This document defines how we prevent duplicate memory facts/procedures from accumulating as we distill (T2 → staged → T3/T4).

Goals:
- Prevent repeated entries that differ only by wording.
- Ensure stable IDs and predictable formatting.
- Keep transforms auditable and reversible.

---

## Canonicalization rules

Applied to **staged outputs** (first), then to canonical files when we implement “apply staged”:

1) **Whitespace normalization**
- Trim trailing spaces
- Collapse 3+ blank lines into 2

2) **Stable section boundaries**
- Each candidate block begins with `## <type> ...` and ends with a blank line.

3) **Deterministic metadata ordering**
Within a candidate block, keep metadata fields in this order when present:
- `- type:`
- `- id:`
- `- confidence:`
- `- trigger:`
- `- source:` or `- evidence:`
- `- generated_at:`

4) **Stable IDs**
If no `id:` exists, derive:
- `id = <YYYY-MM-DD>-<slug(heading)>`

---

## Dedupe rules

We dedupe at two levels:

### Level 1: Receipt-based (hard dedupe)
If two staged outputs have the same:
- `source.sha256`

Then they are duplicates. Keep the earliest output and drop the rest.

### Level 2: Snippet-hash based (soft dedupe)
If two outputs have identical:
- `output.sha256`

Drop the later one.

### Level 3: Semantic-ish heuristic (v0, no embeddings)
Within a single topic file candidate, consider blocks duplicates if:
- same normalized heading, AND
- same `type:`

Keep the one with more metadata/evidence.

---

## Implementation
Implemented as a conservative script that:
- reads staged receipts JSON
- scans `memory/staging/topics/*.md` and `memory/staging/MEMORY.candidates.md`
- produces a **deduped copy** under `memory/staging/deduped/`
- emits a report under `memory/staging/reports/`

No canonical files are modified.
