# Phase 5 — Prompt Injection Policy (RAG)

This document defines **what memory gets injected into prompts**, **where**, and **under what budgets**, so we get strong recall without token bloat.

Core principle: **Index broadly enough to retrieve; inject narrowly enough to stay cheap and safe.**

---

## Definitions
- **Injection**: proactively placing memory text into the model prompt before the model responds.
- **Retrieval**: searching memory stores and returning *snippets* (with citations) to optionally inject.

---

## Default injection set (baseline)
### Always injected (T0)
Small, stable identity + operating rules:
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `AGENTS.md`
- `TOOLS.md`

Constraints:
- Keep each file compact.
- No secrets.

### Conditionally injected (T1)
Working context is injected only if it is present and small.
- `HEARTBEAT.md`: injected only on heartbeat turns
- `workspace/state/*.json`: only **selected keys** may be injected (see below)

---

## Retrieval-driven injection (T2/T3/T4)
T2/T3/T4 are **not** injected wholesale.
Instead we retrieve snippets and inject only the minimum needed to answer.

Priority order for retrieved snippet injection:
1) **T3** (`memory/topics/*.md`) — best signal-to-size
2) **T4** (`MEMORY.md`) — curated durability
3) **T2** (`memory/YYYY-MM-DD.md`) — raw episodic evidence

---

## Budgets (defaults)
These are soft caps; the system should degrade gracefully.

- Max injected memory snippets per turn: **6**
- Max total injected memory tokens per turn (retrieved snippets): **1,200**
- Max per-snippet size: **350 tokens** (truncate with a citation)

Early stop:
- If we already have **2 independent snippets** that support the answer, do not inject more.

---

## “State injection” policy (`workspace/state/*.json`)
We want meta-awareness without leaking noise.

Rules:
- Only inject a **curated projection** of state.
- Prefer a single file: `workspace/state/agent-state.json` (future)

Allowed keys examples:
- lastChecks timestamps
- lastSuccessfulDistillation date
- currentPhase milestone pointer

Forbidden keys:
- auth tokens
- API keys
- message contents
- raw logs

---

## Citation format (required)
Injected snippets must carry a citation so the model can answer with provenance.

Format:
- `Source: <path>#L<start>-L<end>` (or equivalent)

---

## Safety constraints
- Never inject secrets.
- If sensitive tier is introduced later, it is excluded from default injection.
- When in doubt: retrieve and summarize; do not paste.

---

## Interaction with compaction (/compact)
Compaction should:
- preserve citations in summaries
- avoid summarizing secrets into always-loaded tiers
- prefer moving stable facts to T4 and procedures to T3

---

## Open questions (for integration milestone)
- Exact hook points inside OpenClaw agent prompt builder
- Whether injection budgets are per-agent config or global
- How to expose “why was this injected?” receipts to the Control UI
