# Dream Mode specification (draft)

Date: 2026-03-14

## Purpose

Dream Mode is the **primary Lucidity experience**.

It is designed to make memory maintenance feel:
- autonomous
- quiet
- safe
- reviewable when needed

Dream Mode should let a companion maintain its memory with minimal routine operator intervention while still preserving auditability, reversibility, and trust.

---

## Product definition

Dream Mode is:

> a safe-autonomous nightly Lucidity pipeline that captures, distills, reflects on, deduplicates, and selectively commits durable memory while keeping receipts, backups, and rollback available.

Dream Mode is **not**:
- unbounded autonomous memory writing
- a promise that every remembered thing becomes canonical memory
- a replacement for operator review in ambiguous or risky cases

---

## Core principles

### 1) Autonomous by default
Routine memory maintenance should happen without requiring constant human babysitting.

### 2) Quiet by default
Dream Mode should avoid chat noise during normal healthy operation.
It should surface only when:
- explicitly configured to report
- something fails
- a meaningful summary is requested
- the operator asks for status

### 3) Staging-first by design
Dream Mode can be autonomous, but it should still preserve the distinction between:
- staged memory candidates
- canonical memory

Not every staged item should become canonical automatically.

### 4) Safe commitment, not reckless commitment
Canonical writes should happen only when confidence gates pass.

### 5) Auditability and reversibility are mandatory
Every autonomous write path must preserve:
- backups
- manifests/receipts
- repeatability / idempotency
- rollback path

---

## Dream Mode pipeline

The Dream Mode pipeline should be understood as one coherent nightly system:

1. **Backup**
   - take a workspace backup before destructive operations

2. **Dream ingestion / daily processing**
   - process daily logs and relevant transcript-derived material into staged candidates

3. **Reflection**
   - optionally use an LLM reflection step to propose higher-level semantic/procedural candidates into staging
   - this is part of Dream Mode, not a separate “expert-only” concept

4. **Dedupe / canonicalize staging**
   - reduce redundancy and improve quality before any promotion

5. **Autonomous promotion**
   - commit only high-confidence, policy-compliant candidates into canonical memory

6. **Receipts / manifests / telemetry**
   - persist evidence of what happened and why

In docs and installer UX, these should read as one mode, not as a scattered set of unrelated jobs.

---

## Default Dream Mode composition

The recommended Dream Mode installation should enable:

- **backup**: on
- **dream/daily processing**: on
- **reflection**: on
- **dedupe**: on
- **autonomous promotion**: on, but only under explicit safety policy
- **reporting**: silent by default

This is the intended “memory should work, not become work” path.

---

## Job-level intent

### Backup
Purpose:
- ensure rollback and recovery safety before write-capable maintenance steps

Expected behavior:
- run nightly
- keep retention policy in place
- remain boring and dependable

### Dream processing
Purpose:
- transform raw daily/session material into structured staged candidates

Expected behavior:
- catch up gracefully if days were missed
- operate deterministically where possible
- avoid unnecessary noise in staged output

### Reflection
Purpose:
- synthesize durable semantic/procedural candidates that deterministic extraction may miss

Expected behavior:
- propose candidates into staging only
- preserve evidence discipline
- never bypass later safety gates for canonical promotion

### Dedupe
Purpose:
- collapse redundancy and improve signal before promotion

Expected behavior:
- run after staging-generation steps
- keep outputs stable across repeated runs

### Autonomous promotion
Purpose:
- selectively commit durable, high-confidence semantic and procedural memory into canonical files while preserving episodic memory in lower tiers

Expected behavior:
- respect promotion policy
- promote semantic and procedural candidates when confidence gates pass
- preserve episodic candidates as searchable lower-tier context unless they distill into durable insight
- skip ambiguous, under-evidenced, contradictory, or sensitive candidates
- emit manifests for every write-capable run

---

## Reporting behavior

### Default
Dream Mode should be **silent during normal healthy operation**.

### Report when
The system should have a path to surface information when:
- backup fails
- reflection/promotional steps fail unexpectedly
- rollback may be required
- repeated errors accumulate
- the operator explicitly enables announcements
- the operator explicitly requests a summary/status

### Why silence matters
If Dream Mode is chatty, it will feel like maintenance overhead.
If it is too silent, it will feel untrustworthy.
The right balance is:
- quiet by default
- inspectable on demand
- interruptive only for meaningful issues

---

## Relationship to manual/advanced mode

Dream Mode is the **primary path**.

Advanced / Custom mode exists for:
- debugging
- calibration
- dry-run-heavy operators
- experimentation
- conservative deployments

Advanced mode should be presented as:
- useful
- powerful
- secondary

It should not overshadow Dream Mode in the first-run experience.

---

## Success criteria for Dream Mode

Dream Mode is succeeding when:
- backups continue reliably
- staged outputs remain high-signal
- canonical memory improves over time without obvious pollution
- the operator is rarely required to intervene
- receipts/manifests make the system inspectable
- rollback remains available if needed

Dream Mode is failing when:
- it produces excessive chat/reporting noise
- it requires constant review to be useful
- it over-promotes low-confidence material
- it becomes so conservative that memory upkeep stalls
- docs and installer do not clearly describe what it does

---

## Non-goals

Dream Mode does not aim to:
- make every memory decision perfect
- eliminate all manual review forever
- store everything indefinitely
- replace higher-level identity portability efforts such as Anima

Its role is narrower and stronger:
- maintain memory well
- commit only what is safe to commit
- remain locally auditable and reversible

---

## Design implications for the convergence pass

This specification implies the following repo changes:
- installer should present Dream Mode as the default/recommended path
- docs should stop treating dream/reflect/apply as equal-weight disconnected concepts
- promotion policy must be made explicit
- reporting defaults should remain quiet
- advanced/manual controls should still exist, but as a secondary path

---

## Short product sentence

If Lucidity is described in one line, Dream Mode should make this sentence true:

> Lucidity is a safe-autonomous Dream Mode memory system for OpenClaw companions.
