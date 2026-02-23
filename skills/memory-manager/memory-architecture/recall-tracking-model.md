# Phase 3 — Recall Tracking Data Model

This document defines *what to log* so we can measure whether the memory system is improving recall and token efficiency over time.

Design goals:
- **Local-first** (no external telemetry)
- **Auditable** (human-readable logs)
- **Low overhead** (append-only JSONL)
- **Privacy-aware** (avoid logging raw sensitive content)

---

## What “recall tracking” means here
We want to answer questions like:
- Did retrieval return the right memory for a query?
- Did the assistant actually *use* the retrieved memory?
- Did retrieval cost too many tokens?
- Are we indexing too much noise?

We track retrieval as a series of events tied to a session and time window.

---

## Storage format

### Primary store (recommended)
Append-only JSON Lines:
- Path: `workspace/state/memory-recall-events.jsonl`
- One JSON object per line

Rationale: easy to append, diff, inspect, and summarize.

### Optional derived summaries
- `workspace/state/memory-recall-summary.json` (rolling aggregates)

---

## Event types

### 1) retrieval.request
Logged when we decide to query memory.

```json
{
  "type": "retrieval.request",
  "ts": "2026-02-19T13:28:16.000Z",
  "session": "agent:main:main",
  "query": {
    "text": "what was that rule about tier promotion?",
    "sha256": "<hash>",
    "lang": "en"
  },
  "policy": {
    "mode": "single-pass-hybrid",
    "topK_vec": 12,
    "topK_fts": 12,
    "expansions": 2
  },
  "index_scope": {
    "sources": ["memory"],
    "allow": ["MEMORY.md", "memory/"],
    "deny": ["**/node_modules/**", "**/logs/**"]
  }
}
```

Notes:
- We store the **raw query text** by default because it’s usually not sensitive and enables evaluation.
- If we later introduce a sensitive tier, we can add a redaction/scrub step and store only hashes.

### 2) retrieval.results
Logged after we get candidates.

```json
{
  "type": "retrieval.results",
  "ts": "2026-02-19T13:28:17.000Z",
  "session": "agent:main:main",
  "query_sha256": "<hash>",
  "results": [
    {
      "rank": 1,
      "path": "memory-architecture/tier-rules.md",
      "start_line": 1,
      "end_line": 40,
      "chunk_id": "<id>",
      "score": 0.87,
      "channels": ["vec", "fts"],
      "tier": "T3",
      "kind": ["procedural", "semantic"],
      "snippet_sha256": "<hash>",
      "snippet_chars": 820
    }
  ],
  "latency_ms": 180,
  "candidates": {
    "vec": 12,
    "fts": 12
  }
}
```

Notes:
- We capture enough fields to reproduce provenance without storing huge text.
- `tier` is derived from path mapping rules.

### 3) retrieval.injection
Logged when we decide what actually gets injected into the prompt context.

```json
{
  "type": "retrieval.injection",
  "ts": "2026-02-19T13:28:17.500Z",
  "session": "agent:main:main",
  "query_sha256": "<hash>",
  "injected": [
    {"chunk_id": "<id>", "rank": 1, "chars": 820}
  ],
  "budget": {
    "max_tokens": 1200,
    "estimated_tokens": 210,
    "chunks_max": 6,
    "chunks_used": 1
  }
}
```

### 4) retrieval.outcome
Logged after we can infer whether retrieval helped.

```json
{
  "type": "retrieval.outcome",
  "ts": "2026-02-19T13:29:10.000Z",
  "session": "agent:main:main",
  "query_sha256": "<hash>",
  "outcome": {
    "self_reported_helpful": true,
    "confidence": "medium",
    "notes": "User confirmed the tier thresholds answer was correct"
  }
}
```

How do we set `self_reported_helpful`?
- Initially: heuristic based on the user’s follow-up (“yes”, “that’s it”, “perfect”, etc.)
- Later: explicit thumbs-up/down UI hook (if we add it)

---

## Metrics derived from events
- **Recall@k** (proxy): fraction of queries where at least one injected chunk is later marked helpful
- **Precision proxy**: helpful chunks / injected chunks
- **Token efficiency**: estimated injected tokens per successful query
- **Noise ratio**: retrieved candidates from excluded/low-signal paths (should trend down)

---

## Privacy and safety constraints
- Never log secrets.
- If query contains patterns like tokens/keys, redact query text and store only hash.
- Do not log full snippet text by default; store hashes + sizes + provenance.

---

## Implementation note (future milestone)
This doc is the *model*. Implementation will be done in a later phase via:
- a lightweight logger in the memory retrieval layer (or hook)
- a daily summarizer job that writes rolling aggregates
