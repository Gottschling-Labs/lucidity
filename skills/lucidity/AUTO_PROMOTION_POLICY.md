# Safe autonomous promotion policy (draft)

Date: 2026-03-14

## Purpose

This document defines when Lucidity may **autonomously commit staged candidates into canonical memory** during Dream Mode.

The goal is to enable memory commitment that is:
- autonomous in routine cases
- conservative in ambiguous cases
- auditable in every case
- reversible when needed

---

## Policy summary

Lucidity may auto-promote a staged candidate into canonical memory only when it is:

- **durable**
- **non-episodic**
- **well-evidenced**
- **low-risk**
- **non-sensitive by default**
- **high-confidence under current merge/apply heuristics**

If a candidate fails any of those expectations, it should remain in staging unless explicitly reviewed and approved through a more manual flow.

Lucidity should treat **semantic, procedural, and episodic** memory as first-class memory classes, but with different default promotion behavior:
- **semantic**: often eligible for canonical promotion when durable and well-evidenced
- **procedural**: often eligible for canonical promotion when actionable, stable, and low-risk
- **episodic**: preserved and searchable by default, but usually not promoted directly into canonical long-term memory unless distilled into durable semantic/procedural insight

---

## Promotion classes

### Class A — Auto-promotable by default
These are the candidates Dream Mode should be willing to commit automatically.

#### A1. Stable preferences
Examples:
- durable user preference
- long-standing tool or workflow preference
- recurring presentation/communication preference

Requirements:
- appears stable rather than one-off
- is not contradicted by more recent evidence
- is expressed concretely enough to be useful later

#### A2. Durable procedures / SOPs
Examples:
- repeatable maintenance procedure
- known workflow steps
- verification checklist
- operational runbook fragments

Requirements:
- actionable and specific
- not obviously obsolete
- safe to retain as procedural memory

#### A3. Long-lived project facts and decisions
Examples:
- chosen repository path
- stable project naming/positioning decisions
- confirmed architecture boundaries
- durable integration constraints

Requirements:
- framed as settled or substantially settled
- not merely speculative
- likely to remain useful beyond a single session

#### A4. Identity/configuration facts
Examples:
- assistant identity name
- timezone
- workspace conventions
- deployment-specific operating constraints

Requirements:
- clear and factual
- low ambiguity
- safe to keep in canonical memory

---

## Class B — Staging-only by default
These should **not** be auto-promoted in Dream Mode without explicit additional review or stronger future policy.

### B1. Episodic details
Examples:
- one-off events
- transient daily happenings
- temporary frustrations or moods
- isolated conversational details

Reason:
- high risk of noise and temporal brittleness

### B2. Ambiguous or unresolved material
Examples:
- ideas under active debate
- speculative interpretations
- tentative plans
- unconfirmed assumptions

Reason:
- canonical memory should not harden ambiguity into fact

### B3. Emotionally volatile or highly interpersonal interpretations
Examples:
- inferred motives
- unconfirmed emotional conclusions
- socially delicate interpretations from a single exchange

Reason:
- too easy to overfit or misremember

### B4. Sensitive information
Examples:
- secrets
- credentials
- highly private personal data
- unnecessarily intimate facts that do not need always-on recall

Reason:
- even correct memory can be wrong to store in canonical always-retrievable form

### B5. Contradictory candidates
Examples:
- a new preference that conflicts with a prior stable preference
- a project fact contradicted by newer context
- mixed evidence about whether something is still true

Reason:
- contradiction requires resolution, not silent canonical overwrite

---

## Evidence requirements

Auto-promotion should favor candidates with stronger evidence signatures.

### Strong evidence indicators
- explicit markers such as `Decision:`, `Preference:`, `Policy:`, `Canonical:`
- repeated mention across time
- procedural structure such as `Steps:` and `Verify:`
- clear source attribution or obvious supporting context
- low ambiguity and precise phrasing

### Weak evidence indicators
- inferred summaries without explicit grounding
- single vague mention
- emotionally charged but under-specified statements
- context that depends on ephemeral timing
- summaries that could plausibly mean multiple things

Policy rule:
- weakly evidenced candidates should remain staged, not canonical.

---

## Risk checks before autonomous write

Before canonical promotion, the system should effectively pass these checks:

### 1. Durability check
Will this likely remain useful and true beyond the immediate moment?

### 2. Specificity check
Is the candidate concrete enough to be recalled later without distortion?

### 3. Sensitivity check
Would storing this canonically create unnecessary privacy or safety risk?

### 4. Ambiguity check
Is this clearly a fact/preference/procedure, rather than a guess or unresolved thread?

### 5. Contradiction check
Does this conflict with existing canonical memory or other high-confidence staged material?

If any of these checks fail, the candidate should not be auto-promoted.

---

## Canonical destinations

### `MEMORY.md`
Use for:
- durable facts
- stable preferences
- settled decisions
- identity/configuration truths

### `memory/topics/*.md`
Use for:
- procedural knowledge
- project-specific long-lived context
- operating guidance that is useful but more scoped than top-level curated memory

### Keep in staging
Use for:
- candidates needing more evidence
- ambiguous material
- recent episodic material
- anything not yet safe for canonical promotion

---

## Required safety mechanisms

Auto-promotion is only acceptable if these remain in force:

### 1. Backup before apply
Every write-capable autonomous promotion path should rely on backups being present before canonical changes.

### 2. Manifests / receipts
Every autonomous promotion run should leave a manifest or equivalent receipt that answers:
- what changed
- what was skipped
- why it was eligible
- when it happened

### 3. Idempotency
Repeated runs should not duplicate canonical memory.

### 4. Rollback path
A documented, functional rollback route must remain available.

### 5. Dry-run/manual path
Operators must still be able to inspect behavior without committing changes.

---

## Silence vs escalation

Auto-promotion should not normally produce chat noise.

### Stay silent for
- ordinary healthy nightly promotions
- skipped low-confidence candidates
- routine no-op runs

### Escalate / surface when
- backup is missing or fails
- apply/merge fails unexpectedly
- rollback may be needed
- contradiction rates become abnormal
- promotion repeatedly skips everything due to policy mismatch
- operator explicitly asks for summaries

---

## Policy stance on episodic memory

Default stance:
- episodic memory may remain searchable in lower tiers
- episodic memory should not be auto-promoted into canonical memory by default

This preserves useful recall without polluting top-level durable memory.

---

## Policy stance on sensitive memory

Default stance:
- if a memory is both sensitive and non-essential for always-on recall, do not auto-promote it
- sensitivity should bias toward staging-only or more deliberate storage patterns

Dream Mode should optimize for trusted continuity, not maximum retention.

---

## Policy stance on contradiction

If new candidates conflict with canonical memory:
- do not silently overwrite by default
- prefer staging + review-oriented handling
- preserve provenance where possible

Canonical memory should converge carefully, not flip-flop automatically.

---

## Examples

### Example: should auto-promote
> "Preferred location for git repos/clones: `~/code/gottschling-labs/`."

Why:
- durable
- explicit
- low-risk
- configuration-like
- useful later

### Example: should not auto-promote
> "Brandon seemed frustrated tonight about X."

Why not:
- episodic
- emotionally volatile
- too context-bound
- weakly durable

### Example: should usually auto-promote
> "Lucidity should be positioned as the memory engine; Anima should be the portable identity layer."

Why:
- architecture-level project decision
- durable enough to guide future work
- low ambiguity if repeatedly reinforced

### Example: should remain staged
> "We might maybe turn reflection off by default depending on how it feels."

Why:
- unresolved
- speculative
- not settled enough for canonical memory

---

## Design implications

This policy implies:
- Dream Mode can safely include autonomous promotion
- but installer/docs must explain that promotion is selective, not unconditional
- apply behavior must align with these rules
- future heuristic or schema changes should be evaluated against this policy, not against convenience alone

---

## Short policy sentence

If expressed briefly, the policy is:

> Lucidity may autonomously commit only durable, low-risk, well-evidenced memory; everything ambiguous, episodic, contradictory, or sensitive stays staged by default.
