# Memory Architecture Project Plan (Ops Deck priority)

Owner: Gordon (Memory Architect role)
Repo/workspace: `~/.openclaw/workspace/`
Goal: Implement a tiered, local-first, auditable memory architecture with measurable recall and token efficiency improvements.

## Productionization Addendum (post-MVP)
Now that the architecture is built, additional work is recommended before enabling this broadly as a turnkey production feature for other agents.
This addendum tracks that work.

## Robustness Addendum (full production hardening)
The following items are required for a truly robust, widely distributed production package (ClawHub + security + ops maturity).
This addendum tracks those items.

## Guiding Principles
- Markdown remains source of truth.
- Everything is reversible.
- Default behavior is safe and cost-aware.
- Sensitive data is isolated and encrypted.

## Current-State Assessment (baseline)
### What exists today
- Workspace memory files:
  - `MEMORY.md` (curated long-term)
  - `memory/YYYY-MM-DD.md` (daily notes)
- Memory plugin status (from `openclaw status --deep`): memory-core enabled with vector + FTS ready.
- Compaction: agent defaults are set to `safeguard`.
- Tooling: can read/write workspace files, run shell commands, use cron, use web_fetch/web_search/browser.

### Current gaps
- No explicit tier separation beyond daily notes vs MEMORY.md.
- No standardized schemas for episodic vs semantic vs procedural memory.
- No automated tier transitions (distillation, compression, archiving).
- No recall tracking or evaluation harness.
- No encryption or sensitive-tier handling.
- No documented RAG injection policy for prompts.

### Baseline risks
- Token bloat when daily notes or MEMORY.md grow.
- Recall errors due to missing dedupe and inconsistent naming.
- Privacy risk if sensitive details are placed in broadly-loaded files.

## Phases (one milestone per turn)

### Phase 1: Plan and baseline (100%)
- [x] Create this PROJECT_PLAN.md and record a detailed current-state assessment.
- [x] Define success metrics and a minimal evaluation harness (`memory-architecture/eval-harness.md`).

### Phase 2: Tiered structure design (100%)
- [x] Specify tiers T0 to T4 and file layout (`memory-architecture/tier-design.md`).
- [x] Specify episodic, semantic, procedural formats and naming (`memory-architecture/memory-schemas.md`).
- [x] Define thresholds and promotion/demotion rules (`memory-architecture/tier-rules.md`).
  - Evidence: `memory-architecture/tier-rules.md` created with size/time/recall thresholds + promotion/demotion receipts.

### Phase 3: Hybrid retrieval (100%)
- [x] Confirm memory-core indexing inputs (`memory-architecture/indexing-inputs.md`).
- [x] Add hybrid retrieval policy: semantic + FTS with query expansion and early-stop (`memory-architecture/hybrid-retrieval-policy.md`).
- [x] Add recall tracking data model (`memory-architecture/recall-tracking-model.md`).
  - Evidence: `recall-tracking-model.md` defines event types + JSONL storage + derived metrics + privacy rules.

### Phase 4: Compression and tier transitions (100%)
- [x] Implement distillation pipelines (daily -> topic -> long-term).
  - Evidence: `memory-architecture/distillation-pipeline.md` + `memory-architecture/scripts/distill_daily.py` staging into `memory/staging/` with receipts.
- [x] Implement dedupe and canonicalization.
  - Evidence: `memory-architecture/dedupe-canonicalization.md` + `memory-architecture/scripts/dedupe_staging.py` producing `memory/staging/deduped/` and `memory/staging/reports/dedupe-report.json`.

### Phase 5: RAG injection and integration (100%)
- [x] Define prompt injection policy: what to inject, where, and budgets (`memory-architecture/prompt-injection-policy.md`).
- [x] Integrate with sessions_history and /compact routines (`memory-architecture/integration-sessions-compact.md`).

### Phase 6: Automation (100%)
- [x] Add heartbeat or cron jobs for background maintenance (`memory-architecture/automation-jobs.md`).
- [x] Add pruning without data loss (`memory-architecture/pruning-policy.md`).

### Phase 7: Testing, docs, security (100%)
- [x] Add test scenarios and record results (`memory-architecture/test-scenarios.md`, `memory-architecture/test-results.md`).
- [x] Add documentation under `workspace/memory-architecture/` (`memory-architecture/README.md`).
- [x] Add sensitive tier design and encryption approach (`memory-architecture/sensitive-tier-encryption.md`).

### Phase 8: Final audit and handover (100%)
- [x] End-to-end validation plan with cross-session recall procedure (`memory-architecture/final-validation.md`).
- [x] Token efficiency comparison vs baseline (`memory-architecture/token-efficiency.md`).
- [x] Handover checklist and operating guidelines (`memory-architecture/HANDOVER.md`).

## Success Metrics
- Recall: relevant memory retrieved for 8 of 10 test queries across sessions.
- Token efficiency: reduce injected memory tokens by 30% vs baseline for the same tasks.
- Safety: no secrets placed in always-loaded tiers; sensitive tier encrypted.
- Auditability: every memory transform leaves a receipt (source -> output links).

## Productionization Addendum Checklist

- [x] Improve distiller output to scaffold high-confidence procedural promotion (adds `trigger` + `verification` placeholders).
- [x] Implement `apply_staging.py` semantic merge into `MEMORY.md` (T4) with stricter gates (evidence + non-time-bound + safety blocks) and block-level merge receipts.
- [x] Implement optional `--require-review` mode spec (generate diff + require confirm) for first 7 days of a new install (`memory-architecture/require-review.md`).
- [x] Wire recall tracking telemetry emission (JSONL event emission for maintenance/apply runs; stored at `workspace/state/memory-recall-events.jsonl`).
- [x] Expand test suite to 10 queries across multiple topics and record PASS/FAIL (`memory-architecture/test-scenarios.md`, `memory-architecture/test-results.md`).
- [x] Add configuration surface in a skill bundle (defaults + docs) and verify on a fresh agent workspace (`skills/lucidity`).
- [x] Add installer to create Gateway cron job(s) for a new agent with sane defaults (skill: `skills/lucidity/gateway-cron-install.sh`).
- [x] (Optional) Add `memorySearch.extraPaths` installer helper for meta-awareness indexing, with safe allowlist (skill doc: `skills/lucidity/extra-paths.md`).
- [x] (Optional) Implement T-S encryption tooling using GPG (initial scripts in skill: `skills/lucidity/scripts/sensitive_store_gpg.py`, `skills/lucidity/scripts/sensitive_get_gpg.py`).

## ClawHub-Ready Shipping Plan (Prioritized)

Target: publish as a **private** repo under Gottschling-Labs first, then flip public once RC criteria are met.

### Release Candidate gates
RC0 (private): repo bootstrapped + installer works + docs coherent.
RC1: idempotent apply (no duplicates) + regression tests.
RC2: observability (`/memory-stats`) + consent/PII minimization.
RC3: versioning + changelog + CI snippet + checklist alignment docs.
RC4 (public-ready): sandboxing plan implemented (or clearly documented constraints) + perf benchmarks recorded.

### Execution order (what we do next)
1) Fix auto-merge duplicates (idempotency) and add regression tests.
2) Add `/memory-stats` observability hook.
3) Add explicit install consent + PII minimization defaults.
4) Benchmarking (both corpora): latency + recall quality + token efficiency; produce reproducible reports.
5) Release engineering: version pinning + CHANGELOG.md + GH Actions snippet + checklist compliance.
6) Best-effort local hardening now; sandboxing before first public release.

## Robustness Addendum Checklist (Full Production)

### Quality & correctness
- [x] QA test plan: include duplicate-prevention tests for auto-merge + idempotency across repeated runs (`memory-architecture/qa-test-plan.md`).
- [x] Fix auto-merge duplicate behavior (idempotent across runs; stable block key ignores generated_at) and add regression test (`memory-architecture/scripts/test_apply_idempotency.py`).

### Backup & rollback
- [x] Automated daily backup with 7/30/90-day retention (workspace-bundled; script: `memory-architecture/scripts/backup_memory.py`, policy: `backup-policy.md`, cron: 03:45 ET).
- [x] Rollback command using merge receipts/manifests (restore dest files from latest pre-apply backup) (`memory-architecture/scripts/rollback_apply.py`).

### Observability
- [x] Observability dashboard hook (e.g. `/memory-stats`): implemented as local stats script `memory-architecture/scripts/memory_stats.py` (JSON/text) reporting last apply/backup, staging sizes, telemetry counts.

### Privacy & consent
- [x] Explicit user consent and PII minimization on install (install-time prompt + safe defaults; `skills/lucidity/gateway-cron-install.sh`).

### Release engineering
- [x] Version pinning + `CHANGELOG.md` (skill bundle: `skills/lucidity/VERSION`, `skills/lucidity/CHANGELOG.md`).
- [x] Full ClawHub 13-point checklist compliance (bundle: `skills/lucidity/CLAWHUB_CHECKLIST.md`, SKILL.md frontmatter + required sections).
- [x] Alignment with OpenClaw security checklist (doc: `skills/lucidity/OPENCLAW_SECURITY_ALIGNMENT.md`).
- [x] CI/CD publishing snippet for GitHub Actions (skill bundle includes `.github/workflows/*` + `skills/lucidity/CI_CD.md`).

### Security hardening
- [x] Best-effort local hardening + explicit disclaimer that sandboxing is required before public release (bundle: `skills/lucidity/HARDENING.md`; scripts refuse root + require workspace root).
- [x] Sandboxed execution guidance for all scripts (doc + required sandbox image prerequisites) (`skills/lucidity/SANDBOXING.md`).

### Performance
- [x] Performance benchmarks: measure recall latency (p50/p90/p99) on demo corpus + real private corpus.
  - **Public repo:** commit **demo/sanitized** results only.
  - **Private corpus results:** must remain **local-only** (do not commit).
- [x] Benchmark harness: run on (a) real private workspace corpus and (b) sanitized demo corpus committed to repo (bundle: `skills/lucidity/memory-architecture/scripts/bench_memory_search.py`, `benchmarks/`, `demo-workspace/`).
- [x] Token efficiency benchmark: snippet injection proxy vs naive baseline on both corpora (commit demo results only).
- [x] Recall quality benchmark: PASS/FAIL suite on both corpora with reproducible query sets (commit demo results only).

## Change Log
- 2026-02-19: init plan and baseline assessment (memory-architecture)
- 2026-02-19: eval: add memory evaluation harness and scoring rubric
- 2026-02-19: design: tiered memory layout T0-T4
- 2026-02-19: design: add episodic/semantic/procedural memory schemas
- 2026-02-19: design: add tier thresholds and promotion/demotion rules
- 2026-02-19: retrieval: confirm memory-core indexing inputs via local sqlite inspection
- 2026-02-19: retrieval: define hybrid retrieval policy (vector + FTS) with early-stop and query expansion
- 2026-02-19: retrieval: define recall tracking event model (local-first JSONL)
- 2026-02-19: compression: implement non-destructive daily distillation pipeline with staged outputs
- 2026-02-19: compression: implement staged dedupe + canonicalization tools and reporting
- 2026-02-19: rag: define prompt injection policy and budgets (retrieval-driven injection)
- 2026-02-19: rag: integrate policy with /compact + pre-compaction memory flush + session-memory hook behavior
- 2026-02-19: automation: add nightly cron for staging-only distill + dedupe maintenance
- 2026-02-19: automation: add staging archive/prune tool with manifests (no data loss)
- 2026-02-19: testing: add test scenarios + initial test results for retrieval and pipelines
- 2026-02-19: docs: add README index and operating guide for memory-architecture folder
- 2026-02-19: security: define sensitive tier (T-S) and encryption-at-rest approach
- 2026-02-19: audit: add final validation + handover checklist doc (Phase 8 scaffold)
- 2026-02-19: audit: add token efficiency comparison vs baseline (snippet vs full-file injection)
- 2026-02-19: audit: add handover checklist and operating guide
- 2026-02-19: production: add configurable auto-merge (apply staging) + update nightly cron to include it
- 2026-02-19: production: distiller scaffolds procedural candidates for auto-merge confidence gates
- 2026-02-19: production: apply staging can merge semantic candidates into MEMORY.md with strict gating + manifests
- 2026-02-19: production: define require-review mode spec for safe first-week installs
- 2026-02-19: testing: expand retrieval suite to 10 queries (PASS/FAIL) and record results
- 2026-02-19: production: emit JSONL telemetry events for apply/maintenance runs
- 2026-02-19: production: package lucidity skill bundle (defaults+docs+scripts) and verify on fresh workspace
- 2026-02-19: production: add lucidity install script to create cron job and initialize workspace dirs
- 2026-02-19: production: add safe extraPaths guidance doc for optional meta-awareness indexing
- 2026-02-19: security: add minimal GPG-based sensitive tier scripts to lucidity bundle
- 2026-02-19: robustness: add full hardening addendum + QA test plan scaffold
- 2026-02-19: robustness: add workspace-bundled backup script + retention policy + daily cron
- 2026-02-19: robustness: add rollback tool restoring dest files from pre-apply backup via apply manifest
- 2026-02-19: robustness: reprioritize roadmap for ClawHub-ready shipping (private-first RC gates)
- 2026-02-19: robustness: add dual-corpus benchmark requirements (real + sanitized demo) and reprioritize execution order
- 2026-02-19: robustness: add /memory-stats observability script for Lucidity health snapshot
- 2026-02-19: robustness: make apply_staging idempotent (stable key ignores generated_at) + add regression test
- 2026-02-19: robustness: add explicit install consent + PII minimization defaults to installer
- 2026-02-19: release: add VERSION + CHANGELOG to skill bundle (private pre-release)
- 2026-02-19: release: add GitHub Actions CI + release packaging snippets to skill bundle
- 2026-02-20: security: add best-effort local hardening doc + root refusal guardrails (sandboxing required before public)
- 2026-02-20: security: add OpenClaw security alignment mapping doc for Lucidity
- 2026-02-20: release: update SKILL.md for ClawHub frontmatter/sections + add 13-point checklist doc
- 2026-02-20: benchmarks: add dual-corpus benchmark harness + sanitized demo workspace corpus
- 2026-02-20: benchmarks: run and record latency results for demo + private corpus (p50/p90/p99)
- 2026-02-20: benchmarks: add and run token efficiency benchmark (demo + private corpus)
- 2026-02-20: benchmarks: add and run recall quality PASS/FAIL benchmark (demo + private corpus)
- 2026-02-20: security: add sandboxing setup guidance for Lucidity bundle
