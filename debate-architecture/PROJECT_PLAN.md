# Debate Architecture Project Plan (Ops Deck)

Owner: Gordon (Development Architect role)
Repo/workspace: `~/.openclaw/workspace/`
Goal: Implement a multi-model debate + consensus architecture (Proponent/Critic/Fact-Checker/Executor[/Judge]) that improves plan quality and robustness, with auditable traces and safe defaults.

## Guiding Principles
- Traceable: every debate round is logged and linkable.
- Local-first: artifacts saved in `workspace/debate-architecture/`.
- Cost-aware: early stopping + /compact between rounds.
- Safe by default: avoid leaking sensitive context; support redaction and optional encryption.

## Current-State Assessment (baseline)
### What exists today
- Role prompts present in `AGENTS.md` for:
  - Debate Proponent
  - Debate Critic
  - Debate Fact-Checker
  - Debate Executor
- OpenClaw tooling available:
  - `sessions_spawn`, `sessions_send`, `sessions_history`, `sessions_list`
  - `/compact` (session compaction)
  - Workspace file ops (read/write/edit)

### Current gaps
- No dedicated orchestrator skill to reliably run debates end-to-end.
- No persisted debate transcript format or storage convention.
- No consensus layer / scoring / confidence weighting.
- No early-stop policy based on stability.
- No integration hook to invoke debate for “high-stakes” tasks.
- No tests, benchmarks, or documentation set.

### Baseline risks
- Token/cost blowups without compaction and early-stop.
- Low reproducibility if transcripts aren’t persisted.
- Hallucination risk without an explicit fact-check round and citations.

## Phases (one milestone per turn)

### Phase 1: Plan and detailed spec (100%)
- [x] Expand this plan into a detailed spec: artifact formats, orchestrator API, round structure, and storage layout.
  - Evidence: `debate-architecture/spec.md`

### Phase 2: Role prompts and workspace conventions (100%)
- [x] Define per-role prompt wrappers and how each role should cite evidence.
  - Evidence: `debate-architecture/templates/role-prompts.md`
- [x] Define transcript schema + filenames + redaction rules.
  - Evidence: `debate-architecture/templates/transcript-conventions.md`

### Phase 3: Implement Debate Orchestrator skill (in progress)
- [x] Create `skills/debate-orchestrator/` with SKILL.md and runnable scripts.
  - Evidence: `skills/debate-orchestrator/SKILL.md`, `skills/debate-orchestrator/scripts/debate.py`
- [x] Implement artifact persistence utilities (transcript writer + conventions).
  - Evidence: `skills/debate-orchestrator/scripts/artifacts.py` + `debate.py` initializes `debate-architecture/runs/<run_id>/meta.json` (verified 2026-02-25: `debate-20260225-135402Z-189e3c57/meta.json`)
- [ ] Implement orchestration: spawn roles, run 2–4 rounds, compact each round, persist artifacts.
  - Heartbeat evidence (scaffold run created run dir): `debate-architecture/runs/debate-20260304-132820Z-91a2549a/`

### Phase 4: Consensus + early-stopping (0%)
- [ ] Implement consensus synthesis and stability-based early stopping.

### Phase 5: Integration with planner + memory (0%)
- [ ] Add a simple trigger policy (manual command + optional auto-trigger for specific task tags).
- [ ] Store final consensus summary in long-term memory tier(s) (via Lucidity policy).

### Phase 6: Testing + documentation + self-validation (0%)
- [ ] Add test prompts and expected outcomes.
- [ ] Run at least 3 sample tasks and record improvements + costs.

### Phase 7: Hardening + privacy (0%)
- [ ] Add redaction mode and optional encryption for debate traces.
- [ ] Add guardrails for external actions and sensitive info.

### Phase 8: Final audit and handover (0%)
- [ ] Write HANDOVER.md and operating guide.
- [ ] Final end-to-end run and acceptance checklist.

## Change Log
- 2026-02-20: init debate architecture PROJECT_PLAN.md + baseline assessment
- 2026-02-20: spec: add detailed debate architecture spec (storage layout, transcript schema, orchestrator API, round structure)
- 2026-02-20: prompts: add role prompt wrappers + transcript conventions (filenames/frontmatter/redaction)
