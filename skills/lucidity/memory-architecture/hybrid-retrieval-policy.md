# Phase 3 — Hybrid Retrieval Policy (Vector + FTS)

This document defines how OpenClaw memory retrieval should combine **semantic vector search** with **keyword (FTS/BM25) search**, while staying cost-aware and safe.

Status note: On this host, `memory-core` already provisions both:
- Vector index tables (`chunks_vec*`)
- FTS tables (`chunks_fts*`)

(See `memory-architecture/indexing-inputs.md`.)

---

## Goals
- **High recall** for natural-language queries (vector)
- **High precision** for exact strings (FTS/BM25): error codes, filenames, config keys
- **Low token / low latency**: early-stop when results are stable
- **Safety by default**: never surface secrets; avoid injecting large blocks

---

## Retrieval modes

### Mode A: Single-pass hybrid (default)
Used for most queries.

1) **Vector search** over chunks
   - topK_vec = 12
2) **FTS search** over chunks
   - topK_fts = 12
3) **Merge + rerank** into a single list
   - dedupe by chunk hash or (path,start_line,end_line)
   - score = max(normalized_vec, normalized_fts) with small boosts:
     - +0.10 if path is in `memory/topics/` (T3)
     - +0.05 if path is `MEMORY.md` (T4 curated)
     - -0.10 if chunk is older than 365 days (unless user asked historical)
4) **Early-stop**
   - If the top 3 results are from ≤2 files AND each has score above threshold, stop.

### Mode B: Exact-first (when query includes “exact”, codes, filenames)
If the query appears to be:
- contains backticks or quoted strings
- resembles an error code (e.g. `EADDRINUSE`, `404`, `SQLITE_BUSY`)
- includes file paths or extensions (`openclaw.json`, `.md`, `/home/...`)

Then:
1) Run FTS first (topK_fts=20)
2) If FTS finds ≥3 strong hits, only then run vector (topK_vec=6) for augmentation.

### Mode C: Semantic-first (broad “what was that thing…” questions)
1) Run vector first (topK_vec=20)
2) Run FTS second (topK_fts=8) only if:
   - vector confidence is low (spread too flat), OR
   - query contains at least one rare token that might be exact.

---

## Query expansion
To improve recall without bloating results, generate small expansions:

### Lightweight expansions (no extra model call)
- Lowercase + strip punctuation
- Add singular/plural variants for 1–2 key nouns
- If query contains a year/date, also search without it

### LLM-based expansion (optional, future)
If enabled, produce 2–4 short variants:
- synonyms
- alternative phrasings
- include/exclude the user name or project name

Guardrails:
- Never expand into private identifiers
- Hard cap: 4 expansions

---

## Evidence packaging (what retrieval returns)
Returned memory should be a **small set of snippets** with citations:
- path
- line range
- snippet text
- retrieval score (internal)

Do **not** inject entire files.

---

## Injection budget coupling (RAG boundary)
Retrieval output is not automatically injected at full length.

Policy:
- Max 6 chunks surfaced to the agent prompt
- Max 1,200 tokens total from memory snippets
- Prefer:
  1) T3 topic briefs
  2) T4 curated (`MEMORY.md`)
  3) T2 daily logs

---

## Exclusions + safety hooks
- Exclude obvious junk paths from retrieval (even if indexed later):
  - `**/node_modules/**`
  - `**/.git/**`
  - `**/logs/**`
  - `**/*.log`
- Any future sensitive tier must be **excluded from default retrieval** unless explicitly authorized.

---

## Early-stop criteria (practical)
Stop additional retrieval passes when:
- top results converge on the same facts (duplicate meaning across chunks)
- OR enough evidence exists to answer (≥2 independent snippets)

---

## Open questions (to resolve later)
- Exact scoring function and normalization method used by memory-core
- Whether we can expose retrieval confidence + thresholds via config
- How to store retrieval telemetry for recall tracking (Phase 3 milestone #3)
