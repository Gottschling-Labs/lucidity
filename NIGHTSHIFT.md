# NIGHTSHIFT (overnight work queue)

Purpose: keep Gordon moving without Brandon interaction.

## Guardrails
- No public posting.
- No irreversible actions.
- No widening network exposure.
- No secrets changes.
- If anything needs approval, add it to request-queue.md and stop that branch.

## Work items (execute in order)

### A) Ops Deck build loop
1) Implement Research: index and render `mission-control/ops-notes/distilled/*.md`
2) Add tag filter and simple search
3) Add “distill template” generator (creates a new markdown file locally, not committed)
4) Ensure lint and build pass after each change

### B) Research loop
1) Continue r/openclaw token, cost, and memory research
2) Distill findings into `mission-control/ops-notes/distilled/`
3) Update Ops Deck UI if a new pattern emerges

### C) Documentation and receipts
1) Record meaningful changes in request-queue.md (if approval needed) or as repo docs/commits (if implemented)
2) Keep commit messages crisp
