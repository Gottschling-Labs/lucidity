# Phase 5 — Integration: `sessions_history` + `/compact`

This document specifies how the memory architecture integrates with:
- `sessions_history` (session transcript access)
- `/compact` (manual compaction)
- auto-compaction (pre-compaction memory flush)

Goal: make sure important decisions and durable facts make it into **Markdown memory tiers** *before* context is compacted or lost.

---

## What exists in OpenClaw today (baseline)
From OpenClaw docs:
- OpenClaw sessions persist transcripts in JSONL and maintain a session store (`sessions.json`).
- Before auto-compaction, OpenClaw can run a **silent pre-compaction memory flush** turn, controlled by `agents.defaults.compaction.memoryFlush`.
- `/compact` forces a compaction pass.
- A bundled hook `session-memory` can save session context to a memory daily file when `/new` is issued.

Sources:
- `/concepts/memory` (memory flush + memory search)
- `/reference/session-management-compaction` (flush behavior, session store)
- `/cli/hooks` (session-memory hook)

---

## Integration policy (high level)

### 1) Pre-compaction memory flush → T2 (daily log)
When the gateway triggers a memory flush:
- The assistant should write:
  - **episodic decisions & outcomes** → `memory/YYYY-MM-DD.md` (T2)
  - pointers to any new procedures/facts → staged candidates (future) or direct T3/T4 if confident

Important: memory flush turns should be silent:
- respond with `NO_REPLY` unless there is urgent user-visible info

### 2) `/compact` instructions should align to tier rules
When the user runs `/compact <instructions>`:
- the compaction summary should:
  - preserve *decisions* and *open questions*
  - preserve citations where possible
  - avoid copying large blocks of memory into the summary

### 3) `sessions_history` as evidence, not as source-of-truth
Session transcripts are useful for:
- reconstructing what happened
- extracting facts to write into Markdown tiers

But **Markdown remains source of truth**:
- do not treat transcripts as the long-term memory store

Optional future enhancement:
- enable session transcript indexing via memorySearch experimental flags, but keep Markdown as canonical.

---

## Recommended configuration (documented; do not apply automatically)

### A) Compaction memory flush prompt
Set `agents.defaults.compaction.memoryFlush.prompt` to explicitly follow our schemas.

Example prompt:

> Write durable notes now.
> - Append episodic events to `memory/YYYY-MM-DD.md`.
> - If a stable fact/preference emerged, add it to `MEMORY.md` **only if high confidence** and cite the daily log heading.
> - If a reusable procedure emerged, add/update a topic brief under `memory/topics/`.
> Reply with NO_REPLY.

### B) Enable the session-memory hook (optional)
If desired, enable `session-memory` to ensure `/new` triggers a final writeout.

This is complementary to pre-compaction flush.

---

## Operational workflow (what “good” looks like)

1) Normal conversation proceeds.
2) When session nears compaction, gateway triggers silent flush:
   - agent writes T2 daily notes
   - agent replies `NO_REPLY`
3) Auto-compaction runs.
4) Later, distillation pipeline (Phase 4) can compress T2 into staged T3/T4 candidates.

---

## Risks + mitigations

- Risk: flush prompts accidentally cause user-visible spam
  - Mitigation: ensure prompt includes `NO_REPLY` guidance

- Risk: copying secrets into always-loaded tiers
  - Mitigation: flush prompt explicitly forbids secrets; sensitive tier design in Phase 7

- Risk: repeated facts copied into compaction summaries
  - Mitigation: injection policy + hybrid retrieval policy prioritize snippet retrieval with budgets

---

## Verification checklist (for Phase 7/8)
- Trigger a controlled `/compact` and confirm:
  - T2 daily log is updated before compaction
  - compaction summary remains short
- Run a long chat until auto-compaction triggers and confirm:
  - silent flush occurs once per compaction cycle
  - daily log updated
  - no user-visible message delivered
