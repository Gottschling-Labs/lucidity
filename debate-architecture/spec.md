# Debate Architecture — Detailed Spec (v0)

Status: draft spec for Phase 1.

## 1) Storage layout (local-first)

All debate artifacts live under:

- `workspace/debate-architecture/`
  - `runs/`
    - `<runId>/`
      - `meta.json` — run metadata (task, timestamps, config, models)
      - `inputs.md` — sanitized user task + constraints
      - `round-01/` .. `round-N/`
        - `proponent.md`
        - `critic.md`
        - `fact-checker.md`
        - `executor.md`
        - `judge.md` (optional)
        - `synthesis.md` (orchestrator synthesis for that round)
        - `compact.md` (optional: post-round compaction summary)
      - `consensus.md` — final consensus output (plan + risks + open questions)
      - `trace.jsonl` — machine-readable event trace
      - `redaction.md` — what was removed/hashed (if redaction enabled)
      - `attachments/` — optional local-only links or file copies
  - `templates/` — prompt templates and schemas
  - `README.md` — operating guide (later phase)

### Run identifiers
- `runId` = `debate-<YYYYMMDD>-<HHMMSS>-<slug>-<rand4>`
- Slug = 2–5 words from task title, lowercase, hyphenated.

## 2) Transcript / artifact formats

### Markdown artifacts (`*.md`)
Each role output uses a common header for auditability:

```md
---
role: proponent|critic|fact-checker|executor|judge|orchestrator
run_id: <runId>
round: <int>
created_at: <ISO-8601>
model: <string>
inputs_ref: ../inputs.md
---

# Summary
...

# Arguments / Findings
...

# Evidence / Citations
- <url or file:line> ...

# Open Questions
...
```

### Machine trace (`trace.jsonl`)
Append-only JSONL with one event per line:
- `run_created`
- `round_started`
- `agent_spawned`
- `agent_message_sent`
- `agent_response_saved`
- `round_compacted`
- `round_synthesized`
- `early_stop_triggered`
- `consensus_written`

Minimal event schema:
```json
{"ts":"2026-02-20T09:00:00Z","type":"round_started","runId":"...","round":1,"details":{}}
```

## 3) Orchestrator API (skill surface)

Provide a skill `debate-orchestrator` with a single entrypoint script (bash or node):

### CLI
- `debate run --task "..." [--rounds 3] [--roles proponent,critic,fact-checker,executor] [--judge] [--compact] [--budgetTokens 8000] [--redact] [--encrypt] [--output <path>]`

### Behavior
1. Create run folder + write `meta.json` + `inputs.md`.
2. Spawn role sessions via `sessions_spawn` (isolated) using role-specific prompts.
3. For each round:
   - Send the same shared context + prior synthesis to each role.
   - Collect responses via `sessions_history`.
   - Write role outputs to `round-XX/<role>.md`.
   - Run orchestrator synthesis for the round → `round-XX/synthesis.md`.
   - Optional: compact each role session and store `round-XX/compact.md`.
4. Apply early-stop if stability is met (see §5).
5. Write `consensus.md` and return it to the main session.

### Inputs and context contract
- Orchestrator must pass:
  - user task
  - constraints (time, budget, tools allowed)
  - known facts (explicit list)
  - required output format (plan / checklist / decision)
- Orchestrator must NOT pass:
  - raw secrets by default (redaction mode enabled by default for “unknown sensitivity” tasks)

## 4) Round structure (default)

Default: 3 rounds, roles: Proponent, Critic, Fact-Checker, Executor.

- **Round 1 (Generate + critique):**
  - Proponent: propose high-level approach and options.
  - Critic: identify failure modes, missing constraints.
  - Fact-Checker: verify factual claims, request sources, flag uncertainties.
  - Executor: translate into steps, dependencies, time/cost estimates.
  - Orchestrator: synthesize into Round 1 synthesis.

- **Round 2 (Refine):**
  - All roles respond specifically to Round 1 synthesis and gaps.
  - Orchestrator tightens plan, adds risk mitigations.

- **Round 3 (Finalize):**
  - Fact-Checker focuses on any remaining unverifiable claims.
  - Executor produces final action plan.
  - Orchestrator produces final consensus + open questions.

## 5) Consensus & scoring (placeholder for later phases)

Consensus output (`consensus.md`) must include:
- Recommended plan (ordered steps)
- Alternatives considered + why rejected
- Risks + mitigations
- Confidence ratings per major claim (High/Med/Low)
- Explicit “What would change my mind” triggers
- Open questions to ask the user (max 3)

Stability-based early-stop (initial heuristic):
- If Round N synthesis differs from Round N-1 only by:
  - wording, reordering, or clarifications
  - and no new risks/open questions are introduced
  - and Fact-Checker has no new “blocking” flags
Then stop early.

## 6) Redaction + encryption (hooks for Phase 7)

- Redaction mode:
  - Hash or replace with tokens: `[REDACTED:EMAIL]`, `[REDACTED:API_KEY]`
  - Maintain `redaction.md` mapping locally (never injected into other sessions).
- Optional encryption:
  - Encrypt `runs/<runId>/` at rest (GPG) when enabled.

## 7) Integration hooks (for Phase 5)

- Manual trigger: user command `/debate <task>` (mapped to skill).
- Auto-trigger (optional): if task tagged `high-stakes`, `external-send`, `money`, `security`, or `health`.
- Memory integration: store only final `consensus.md` summary + key decisions in long-term memory; keep full transcripts local.
