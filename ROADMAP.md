# Lucidity Roadmap to 1.0

This roadmap is intentionally opinionated. It describes a plausible path from the current Dream Mode convergence work to a coherent `1.0` release.

## North Star

Lucidity should become:

> a local-first, auditable Dream Mode memory system for OpenClaw companions

That means:
- safe autonomous nightly memory maintenance
- strong auditability and reversibility
- useful long-term continuity across semantic, procedural, and episodic memory
- clear user-facing observability
- a clean boundary with future portability/identity layers such as Anima

---

## 0.4.x — Dream Mode convergence

Status: recently converged

Focus:
- make Dream Mode the primary product path
- align installer/docs/defaults
- codify autonomous promotion policy
- explicitly support semantic/procedural/episodic memory classes
- establish Lucidity ↔ Anima interface boundary

Exit criteria:
- repo tells one consistent story
- installer behavior matches docs
- autonomous promotion is bounded and explainable

---

## 0.5.x — Real dream orchestration

Theme: **nightly consolidation becomes a first-class pipeline**

Planned work:
- add a real Dream Mode orchestration entrypoint
- transcript-aware ingestion in addition to daily-log ingestion
- one nightly receipt/report covering all sub-steps
- simpler cron surface area
- clear failure handling and resumability

Why it matters:
- closes the gap where important context never made it into daily logs
- makes Dream Mode feel like a real product behavior instead of a set of adjacent jobs

Potential deliverables:
- `dream.py` or equivalent orchestration script
- unified nightly manifest/report
- docs for transcript-aware ingestion and retention boundaries

---

## 0.6.x — Recall quality and memory hygiene

Theme: **better memory quality, less noise**

Planned work:
- stronger heuristics for semantic/procedural extraction
- better episodic compression/summarization
- contradiction detection and review pathways
- stronger topic-brief hygiene
- benchmarked recall quality improvements

Potential deliverables:
- retrieval/quality benchmarks
- contradiction review mode
- staging quality reports

---

## 0.7.x — Anima-aligned portability foundations

Theme: **portable continuity, without pretending runtimes are portable**

Planned work:
- formalize export/import boundaries for curated memory + identity files
- manifest shape for portable Lucidity-compatible bundles
- restore semantics and recovery docs
- durable profile hints for constrained runtimes

Potential deliverables:
- Lucidity-side export manifest draft
- documented restore workflow
- compatibility notes for future Anima bundles

---

## 0.8.x — UI / observability layer

Theme: **make memory operations legible to humans**

Planned work:
- expose Dream Mode runs, receipts, manifests, and promotion summaries in a human-friendly UI
- show recent nightly activity, skips, promotions, and warnings
- let users inspect why something was promoted or left staged

### Nerve UI integration concept

Target: integrate Lucidity into **OpenClaw Nerve UI**
- Repo: <https://github.com/daggerhashimoto/openclaw-nerve>

Conceptual Lucidity panels/widgets:
- **Dream Mode status**
  - last run
  - next run
  - success/failure
  - quiet/announce mode
- **Promotion activity**
  - semantic promoted
  - procedural promoted
  - episodic retained lower-tier
  - skipped/blocked items
- **Receipts & manifests browser**
  - inspect manifests by run
  - filter by memory class or action
- **Memory health**
  - staging volume
  - contradiction warnings
  - recall quality indicators
- **Anima / portability readiness**
  - whether core identity + curated memory are export-ready

Possible integration path:
1. start with a read-only status/receipts API contract
2. render nightly summaries and manifests in Nerve
3. later add safe operator actions (rerun, dry-run, open manifest, rollback guidance)

---

## 0.9.x — Hardening and operator trust

Theme: **production confidence**

Planned work:
- redaction/sensitive memory controls
- optional encryption for selected tiers or artifacts
- stronger CI/demo verification
- resilient recovery from partial nightly failures
- clearer operator controls for conservative vs aggressive behavior

Potential deliverables:
- hardened sensitive-memory guidance
- recovery playbooks
- improved CI smoke/integration tests

---

## 1.0.0 — Production-ready Lucidity

Theme: **trusted continuity system**

A 1.0 release should mean:
- Dream Mode is coherent, stable, and well-documented
- transcript-aware consolidation is real
- autonomous promotion is bounded, auditable, and trusted
- observability exists (including UI integration or at least a stable UI-facing contract)
- restore/recovery/portability boundaries are clear
- repo/release hygiene is mature

### 1.0 bar
- stable installer and operational model
- reproducible verification path
- CI + demo corpus confidence
- strong docs for operators and contributors
- no major ambiguity about what Lucidity is or is not

---

## Explicit non-goals for 1.0

Lucidity 1.0 does **not** need to:
- solve full companion identity portability end-to-end by itself
- replace retrieval/index systems such as memory-core
- perfectly automate every memory judgment
- provide rich editing UI for every memory artifact on day one

It does need to be:
- coherent
- trustworthy
- inspectable
- useful every day
