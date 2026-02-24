# Phase 4 - Distillation Pipeline (Daily → Topic → Long-term)

This document defines and implements the **non-destructive** distillation flow that moves information from:
- **T2** daily logs (`memory/YYYY-MM-DD.md`)
→ to **T3** topic briefs (`memory/topics/<topic>.md`)
→ to **T4** curated long-term (`MEMORY.md`)

Key constraints:
- Markdown remains source of truth.
- No data loss: raw T2 remains append-only.
- Distillation outputs are staged and require explicit promotion.
- Every output includes receipts pointing back to source file + heading + date.

---

## Output locations (staging-first)
Distillation never writes directly into canonical memory files on first pass.

- Staging folder: `memory/staging/`
  - `memory/staging/topics/<topic>.md` (candidate T3 updates)
  - `memory/staging/MEMORY.candidates.md` (candidate T4 inserts)
  - `memory/staging/receipts/<date>.json` (machine-readable receipts)

After review, a second step can apply staged changes into `memory/topics/` and `MEMORY.md`.

---

## Pipeline steps

### Step A: Parse daily log (T2)
Input: `memory/YYYY-MM-DD.md`

Extract:
- headings (`## ...`)
- bullet blocks
- explicit `type:` metadata if present (per `memory-schemas.md`)

### Step B: Classify into (episodic | semantic | procedural)
Heuristics (until LLM-based classifier is wired):

Prefer explicit markers in your daily logs:
- Procedural markers: `Steps:`, numbered lists (`1) ...`), `Procedure:`, `How to:`
- Semantic markers: `Decision:`, `Policy:`, `Preference:`, `Fact:`, `Rule:`, `Canonical:`

Fallback:
- If a section contains steps/numbered instructions → procedural
- If it contains an explicit semantic marker line → semantic candidate(s)
- The remainder is treated as episodic context (retrievable, not auto-promoted)

### Step C: Map to topic
Heuristics:
- Use `context:` field if present
- Else derive from keywords (openclaw/memory/telegram/gateway/etc.)

### Step D: Distill
- Episodic: keep in T2; optionally produce short "what changed" for topic file
- Procedural: produce/merge a procedure section in a topic candidate
- Semantic (high-confidence): add to `MEMORY.candidates.md` with evidence

### Step E: Emit receipts
Write receipts as JSON:
- source file
- source heading
- output target
- hashes of source excerpt and output excerpt

---

## Implementation artifact
The initial implementation is a lightweight local script:
- `memory-architecture/scripts/distill_daily.py`

This first version is intentionally conservative:
- it only writes into `memory/staging/`
- it does not overwrite existing canonical memory files

---

## Promotion (manual for now)
A separate apply step (future milestone) will:
- merge staged topic candidates into `memory/topics/`
- propose diffs for `MEMORY.md`

Until then, staged outputs provide a safe, inspectable workflow.
