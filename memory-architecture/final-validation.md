# Phase 8 — Final Validation + Handover

This document records end-to-end validation steps and results.

## Validation goals
- Cross-session recall works (memory_search returns correct snippets after session reset)
- Token efficiency: memory injection remains bounded
- Safety: no secrets in always-loaded tiers; sensitive tier design exists

---

## V8.1 Cross-session recall (manual procedure)

1) In main chat, ask the assistant: "What environment is OpenClaw running in?".
   - Expect memory_search to cite `MEMORY.md#L1-L9`.
2) Run `/new` to start a new session.
3) Ask the same question again.
   - Expect same citation.

Result: (pending)

---

## V8.2 Token efficiency sanity check

Check that the assistant does not inject whole memory files and respects budgets.

Procedure:
- Ask a question requiring memory.
- Observe that the answer cites small snippets, not full file dumps.

Result: (pending)

---

## V8.3 Automation sanity check

Verify cron job exists:
- `memory-nightly-distill-dedupe (staging-only)` scheduled 04:15 ET.

Result: PASS (job id recorded in project docs and cron scheduler)

---

## V8.4 Safety sanity check

- Confirm sensitive tier design exists: `memory-architecture/sensitive-tier-encryption.md`
- Confirm scripts are staging-only (no canonical mutation)

Result: PASS (design + scripts are staging-first)

---

## Handover checklist
- [ ] Review README
- [ ] Confirm cron schedule time is desired
- [ ] Decide whether to enable session transcript indexing (optional)
- [ ] Decide whether to implement T-S encryption tooling (age/gpg)
