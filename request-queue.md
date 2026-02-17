# Request Queue and Wish List

Purpose: capture proposed improvements that need Brandon approval before implementation.

## Pending approval

### 8) Fix web research plumbing (keys plus browser tool)
- Observation: `web_search` is currently blocked by `missing_brave_api_key`, and the `browser` tool cannot reach the browser control service (timeout).
- Proposal: set up either Brave or Perplexity keys, then restart the gateway to bring `web_search` back. Also investigate why the browser control service is unreachable.
- Why: NIGHTSHIFT research work is crippled without search or a working browser.
- Risk: low to medium (touches keys and gateway restart, but reversible).

### 4) Multi-model routing policy
- Proposal: formalize model routing rules: cheap model for routine tasks, stronger model only when needed, with explicit budget limits.
- Why: reduce token burn.
- Risk: medium (quality regressions if routing is too aggressive).

### 5) Memory hygiene architecture
- Proposal: explicit cadence and tooling for distillation from daily notes to curated memory, plus a "forget by default" stance on volatile details.
- Why: keeps context lean and accurate.
- Risk: medium (could drop useful nuance if done too bluntly).

### 7) Git remote and push target for Ops Deck work
- Observation: this workspace repo currently has no git remote configured, so I cannot actually push `ops-deck-ui`.
- Proposal: define the canonical remote URL and whether this repo is the Ops Deck UI repo or just the notes repo.
- Why: nightshift needs a safe, repeatable push path.
- Risk: low (mostly process), but mispointing the remote would be ugly.

## Approved and in progress

### 0) Use browser relay for research
- Approved: use the Chrome Relay browser for research tasks.

### 0b) Git remote plus branch conventions for Ops Deck work
- Approved: standardize repo locations and branch conventions so nightshift pushes cleanly.

### 1) Distilled notes sync pipeline
- Approved: build tooling to distill local raw notes into repo versioned notes.

### 2) Ops Deck UI: markdown viewer and note index
- Approved: implement index and markdown rendering for distilled notes, with tags and search.

### 3) Ops Deck UI: Agent Activity receipts store
- Approved: design a receipts schema and build an Activity viewer.

### 6) VPS migration hardening plan
- Approved: draft a VPS migration plan and checklist.

## Completed
- None yet.
