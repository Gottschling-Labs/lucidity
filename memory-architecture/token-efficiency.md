# Phase 8 — Token Efficiency Comparison vs Baseline

This document estimates memory-related token overhead for answering a memory-dependent query.

Because we do not yet have full retrieval telemetry wired into the agent loop, this is an **approximation** based on:
- size of retrieved snippet text (from `memory_search`)
- size of naive baseline “inject whole memory files” behavior

We use a rough conversion:
- **1 token ≈ 4 characters** (English prose heuristic)

---

## Test query
Query: `OpenClaw running in WSL Ubuntu`

### Retrieved approach (current policy)
`memory_search` returned 1 snippet:
- `MEMORY.md#L1-L9`
- snippet length: ~229 characters (from indexed chunk `MEMORY.md` 1–9)

Estimated tokens injected from memory:
- 229 / 4 ≈ **57 tokens**

### Baseline approach (naive)
Inject full files into prompt context:
- `MEMORY.md`: 231 chars
- `memory/2026-02-16.md`: 2275 chars

Total chars: 231 + 2275 = 2506
Estimated tokens: 2506 / 4 ≈ **626 tokens**

---

## Comparison
- Retrieved snippet injection: ~57 tokens
- Naive full-file injection: ~626 tokens

Estimated reduction:
- (626 - 57) / 626 ≈ **90.9% fewer memory tokens** for this query

---

## Notes / limitations
- This is a small-corpus test today (only 2 memory files indexed). As memory grows, the benefit of snippet retrieval grows.
- Real injection also includes T0 baseline files; this comparison isolates the *memory* portion.
- A future enhancement is to log actual injected token counts via the recall-tracking model and/or gateway prompt builder hooks.
