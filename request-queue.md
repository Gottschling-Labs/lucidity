# Request Queue and Wish List

Purpose: capture proposed improvements that need Brandon approval before implementation.

## Pending approval

### 0) Enable web_search for NIGHTSHIFT research
- Proposal: configure Brave Search API key for the Gateway so `web_search` works during nightshift.
- Why: research loop currently runs blind without live sources.
- Risk: low (key management), but needs owner approval.

### 0b) Git remote + branch conventions for Ops Deck work
- Proposal: add the correct git remote, create/push an `ops-deck-ui` branch, and clarify where `mission-control/` should live (subdir in this repo vs separate repo).
- Why: current workspace repo has no remote, so nightshift cannot push changes.
- Risk: low.

### 1) "Distilled notes sync" pipeline
- Proposal: create a small CLI script that takes a local raw note from `~/.openclaw/workspace/notes/` and generates a distilled markdown entry under `mission-control/ops-notes/`.
- Why: keeps raw notes private and messy, while making distilled notes reviewable and versioned.
- Risk: low.

### 2) Ops Deck UI: markdown viewer and note index
- Proposal: add a Research UI that lists distilled notes, renders markdown, supports tags, search, and "create issue draft" actions.
- Why: turns Ops Deck into the actual home for research.
- Risk: low.

### 3) Ops Deck UI: Agent Activity receipts store
- Proposal: define a local JSONL schema for run receipts and a viewer in Ops Deck. Later, sync distilled summaries into repo.
- Why: audit trail, cost control, approvals queue.
- Risk: medium (privacy considerations), but local-first.

### 4) Multi-model routing policy
- Proposal: formalize model routing rules: cheap model for routine tasks, stronger model only when needed, with explicit budget limits.
- Why: reduce token burn.
- Risk: medium (quality regressions if routing is too aggressive).

### 5) Memory hygiene architecture
- Proposal: explicit cadence and tooling for distillation from daily notes to curated memory, plus a "forget by default" stance on volatile details.
- Why: keeps context lean and accurate.
- Risk: medium (could drop useful nuance if done too bluntly).

### 6) VPS migration hardening plan
- Proposal: write a short plan and checklist for VPS move: network exposure, SSH hardening, secrets storage, and browser separation.
- Why: avoid surprises when we go remote.
- Risk: medium.

## Approved and in progress
- None yet.

## Completed
- None yet.
