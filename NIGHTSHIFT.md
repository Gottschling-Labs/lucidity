# NIGHTSHIFT (overnight work queue)

Purpose: keep Gordon moving without Brandon interaction.

## Guardrails
- No public posting.
- No irreversible actions.
- No widening network exposure.
- No secrets changes.
- If anything needs approval, add it to request-queue.md and stop that branch.

## Work items (execute in order)

### 0) Triage and queue hygiene (every hour)
1) Open `request-queue.md` and reconcile status
   - For each item under "Approved and in progress":
     - If work started: add a short "Progress" note (1 to 3 bullets) with timestamp
     - If blocked: add "Blocked" plus what is needed
     - If finished: move it to "Completed" with a completion note and relevant commit links
   - For each item under "Pending approval": only update with clarifying info, do not start.
2) If any "Approved and in progress" items remain incomplete: continue working them in priority order.
3) If all approved items are complete: pivot to the Ops Deck GitHub Kanban
   - Board: https://github.com/orgs/Gottschling-Labs/projects/1
   - Pull the next highest priority card
   - When starting a card: mark it "In progress" and note what branch/commit will contain the change
   - When done: move to "Done" and link the PR/commit

### A) Ops Deck build loop
1) Implement Research: index and render `mission-control/ops-notes/distilled/*.md`
2) Add tag filter and simple search
3) Add “distill template” generator (creates a new markdown file locally, not committed)
4) Ensure lint and build pass after each change

Path guardrail:
- If working directory is `.../mission-control/ops-deck`, paths start at `src/...`, not `ops-deck/src/...`.
- If running `git add`, prefer running from repo root `.../mission-control` using paths like `ops-deck/src/...`.

Tooling guardrail:
- Do not assume `rg` (ripgrep) exists. Use `grep -RIn` instead.
   - Run: `cd ~/code/gottschling-labs/mission-control/ops-deck && pnpm verify`
   - If using the WSL service (`ops-deck.service`), restart it after changes: `systemctl --user restart ops-deck.service`
   - Confirm the new route in the browser (example: `/capabilities`)

### B) Research loop (read-only unless approved)
1) Continue r/openclaw token, cost, and memory research
2) Distill findings into `mission-control/ops-notes/distilled/`
3) Update Ops Deck UI if a new pattern emerges

### C) Documentation and receipts
1) Repo rule: only run git commands inside real repos (usually `~/code/gottschling-labs/mission-control`). Never run git inside `~/.openclaw/workspace`.
2) Record meaningful changes in request-queue.md (if approval needed) or as repo docs/commits (if implemented)
3) Keep commit messages crisp
