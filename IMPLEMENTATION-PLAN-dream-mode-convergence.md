# Lucidity implementation plan — Dream Mode convergence

Date: 2026-03-14

Companion goal:

> Converge Lucidity into a **safe-autonomous Dream Mode memory system** without sacrificing auditability, reversibility, or operator trust.

This plan translates the audit memo into an execution sequence.

---

## 0) Outcome definition

This convergence pass is successful when all of the following are true:

1. A new reader can understand Lucidity’s main product story in under 2 minutes.
2. The installer presents **Dream Mode** as the primary path.
3. Automatic memory commitment happens only through explicit, documented safety gates.
4. Docs, installer behavior, cron behavior, and changelog all describe the same default experience.
5. Advanced/manual workflows still exist, but are clearly secondary.

---

## 1) Product decisions to lock first

These decisions should be treated as blockers for implementation churn.

### D1. Primary identity
**Decision:** Lucidity is primarily a **safe-autonomous Dream Mode memory system**.

Implication:
- all top-level copy should reinforce this
- architecture language becomes supporting detail, not the headline

### D2. Primary install path
**Decision:** The installer should offer:
- **Dream Mode** (default/recommended)
- **Advanced / Custom** (secondary)

Implication:
- fewer equal-weight prompts up front
- less “toolkit menu” feel

### D3. Reporting posture
**Decision:** Dream Mode should be **quiet by default**.

Implication:
- normal maintenance runs do not spam chat
- surfaced reporting should be intentional (errors, summaries, or explicit opt-in)

### D4. Safety posture for promotion
**Decision:** Autonomous promotion is allowed only when confidence gates pass.

Implication:
- Dream Mode can be autonomous
- but not every staged item should become canonical memory automatically

---

## 2) Scope of the convergence pass

### In scope
- installer/default-path redesign
- safe autonomous promotion policy
- cron/install behavior cleanup
- doc convergence
- stable vs experimental framing
- repo/product positioning updates

### Out of scope
- major new retrieval engine work
- plugin/upstream extraction
- full Anima implementation
- deep runtime-profile integration
- broad refactors unrelated to Dream Mode convergence

These can follow after product convergence.

---

## 3) Proposed implementation phases

## Phase 1 — Define Dream Mode precisely

### Goal
Produce a crisp, non-ambiguous definition of what Dream Mode does.

### Deliverables
- short Dream Mode spec doc
- explicit list of installed jobs
- explicit reporting behavior
- explicit promotion behavior
- explicit failure/rollback posture

### Questions to answer
- Does Dream Mode install backup + dream + reflect + dedupe + apply?
- Is `apply` enabled by default in Dream Mode, or staged behind a maturity flag?
- Should `dream` and `reflect` both exist, or should they be conceptually collapsed in docs?
- What events should break silence and notify the user?

### Recommendation
Start with this default Dream Mode composition:
- backup: on
- dream/daily processing: on
- reflection: on
- dedupe: on
- auto-apply: on **only for high-confidence candidates under explicit policy**
- reporting: silent by default

### Exit criteria
A one-page Dream Mode definition exists and can be referenced by all subsequent edits.

---

## Phase 2 — Formalize safe autonomous promotion policy

### Goal
Make automatic commitment of memory concrete, safe, and explainable.

### Deliverables
- promotion policy doc
- explicit criteria for autonomous canonical writes
- list of categories that remain staging-only by default
- audit/rollback expectations for every autonomous write path

### Policy areas to define
#### A) Allowed to auto-promote
Candidates that are:
- durable
- non-time-bound
- strongly evidenced
- low-risk
- non-sensitive
- high-confidence under current apply heuristics

Examples:
- stable user preference
- durable SOP/procedure
- long-lived project fact
- confirmed identity/configuration fact

#### B) Not allowed to auto-promote by default
Candidates that are:
- episodic
- ambiguous
- emotionally volatile
- highly contextual
- under-evidenced
- potentially sensitive

Examples:
- one-off conversation details
- speculative interpretations
- unresolved decisions
- emotional states from a single session

#### C) Safety mechanisms that must remain in force
- backup before apply
- write manifests for every auto-apply run
- idempotent repeated runs
- dry-run/debug path always available
- rollback path documented and tested

### Exit criteria
There is a policy doc that makes “autonomous but safe” operationally legible.

---

## Phase 3 — Installer redesign around Dream Mode

### Goal
Make the installer feel like a product, not a bag of knobs.

### Deliverables
- redesigned `install.sh` interaction flow
- Dream Mode as recommended/default path
- Advanced/Custom as secondary path
- cleaner prompt structure

### Suggested installer flow
1. Workspace root
2. Timezone
3. Mode selection:
   - Dream Mode (recommended)
   - Advanced / Custom
4. If Dream Mode:
   - explain what gets installed
   - explain quiet-by-default behavior
   - explain autonomous promotion safety rails
   - optional surfaced reporting toggle
5. If Advanced:
   - expose per-job and per-reporting controls

### Implementation notes
- avoid leading with separate prompts for every feature
- prefer one concept-first decision followed by a concise summary
- print installed job summary at end

### Exit criteria
A new install makes the primary intended Lucidity experience obvious.

---

## Phase 4 — Doc convergence pass

### Goal
Make the repo speak with one voice.

### Files to update
- `README.md`
- `skills/lucidity/README.md`
- `skills/lucidity/INSTALL.md`
- `skills/lucidity/GATEWAY_CRON.md`
- `skills/lucidity/DOCUMENTATION.md`
- `skills/lucidity/SKILL.md`
- `CHANGELOG.md`
- optionally `MAINTAINERS.md`

### Required doc outcomes
- one clear top-level product sentence
- Dream Mode described as the primary path
- advanced/manual mode clearly secondary
- promotion safety rules documented consistently
- stable vs experimental boundaries visible

### Important cleanup targets
- remove conflicting default descriptions
- stop mixing “architecture” language with “default install story” at the top
- ensure apply behavior is described consistently everywhere

### Exit criteria
There are no meaningful contradictions between docs, installer, and intended behavior.

---

## Phase 5 — Stable vs experimental framing

### Goal
Prevent future meandering by making boundaries explicit.

### Stable / supported
- Dream Mode core pipeline
- backup / dream / reflect / dedupe / apply safety rails
- manifests / rollback / observability
- Markdown workspace as source of truth

### Experimental / roadmap
- Anima portability interface
- runtime/retrieval profiles
- upstream/plugin candidates
- more advanced cross-host portability semantics

### Deliverables
- small roadmap/framing section in docs
- explicit labels where needed

### Exit criteria
New contributors can tell what they can rely on today versus what is aspirational.

---

## Phase 6 — Verification and re-audit

### Goal
Ensure convergence actually improved clarity and behavior.

### Checks
- installer path walkthrough
- cron jobs created match Dream Mode spec
- direct script sanity checks still pass
- apply idempotency test still passes
- backup/rollback assumptions still hold
- docs match behavior

### Re-audit questions
- Can a new user explain Lucidity after reading only the README?
- Is Dream Mode obviously the main path?
- Is autonomous promotion clearly safe-bounded rather than vague?
- Does the repo feel less like a toolkit and more like a product?

### Exit criteria
A post-pass audit says Lucidity is now converged enough to move into community-readiness work.

---

## 4) Concrete next milestone

## Milestone A — Dream Mode spec + promotion policy

This should be the immediate next milestone because it unlocks everything else.

### Deliverables
- `DREAM_MODE.md` or equivalent design note
- `AUTO_PROMOTION_POLICY.md` or equivalent design note
- short decision summary in README/INSTALL draft notes

### Why this first
Without these decisions, installer and doc edits will keep oscillating.

---

## 5) Suggested work order

1. Write Dream Mode spec
2. Write autonomous promotion policy
3. Redesign installer flow around those decisions
4. Sync docs
5. Run verification/tests
6. Re-audit and then package for PR/community-readiness

---

## 6) Risks to watch

### Risk 1: Overcorrecting into excessive autonomy
Mitigation:
- keep strong confidence gates
- preserve manifests and rollback
- do not auto-promote ambiguous/episodic data

### Risk 2: Remaining too conservative
Mitigation:
- Dream Mode must still feel autonomous in practice
- avoid requiring routine human review for normal operation

### Risk 3: Too many concepts remain visible
Mitigation:
- concept-first installer
- primary/secondary path distinction
- stable/experimental labeling

### Risk 4: Docs drift again
Mitigation:
- convergence pass should update all core docs in one PR
- avoid staggered behavioral changes without doc sync

---

## 7) Definition of done for the convergence pass

This pass is done when:
- Dream Mode is clearly the product’s primary path
- autonomous promotion rules are explicit and safe
- installer/docs/defaults all agree
- advanced/manual mode exists without overshadowing Dream Mode
- a fresh audit says the project feels coherent rather than meandering

---

## 8) Immediate next action

**Next action:** author the two anchor docs:
1. Dream Mode specification
2. Safe autonomous promotion policy

Everything else should follow from those.
