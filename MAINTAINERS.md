# Maintainers - Lucidity

This file replaces `PUBLIC_RELEASE_AUDIT.md` and `CRITICAL_REVIEW.md`.

It is intentionally concise and is safe to keep in the public repo.

## 1) Public release checklist (status)

Overall status: **Not yet public-ready**, but close.

### Repository hygiene
- [x] Repo contains only Lucidity skill + documentation
- [x] `mission-control/` removed and ignored
- [x] No private-corpus benchmark artifacts tracked

### Security / secrets
- [x] Basic secret-pattern scan over tracked files (no hits)
- [x] Scripts are local-first; no network calls required by default

### Quality gates
- [x] Python compile sanity: `python3 -m compileall` on scripts
- [x] Apply idempotency regression test passes
- [x] CI workflow exists to enforce these

### Governance
- [x] `CONTRIBUTING.md`
- [x] `SECURITY.md`
- [x] `CODE_OF_CONDUCT.md`

### Documentation
- [x] Tier architecture (T0-T4) documented
- [x] LLM/indexing dependencies documented
- [x] Root quickstart: "clone, install, verify"
- [x] Explicit safe-defaults callout in root README

### Releases
- [x] License: GPL-3.0-or-later
- [x] Root `CHANGELOG.md`
- [ ] Tag `v0.1.0` (recommended)

## 2) Critical review (recommended improvements)

High priority:
- Add `CODE_OF_CONDUCT.md` (Contributor Covenant)
- Add root `CHANGELOG.md` and create tag `v0.1.0`
- Add a prominent "safe defaults" section to root `README.md`

Medium priority:
- Add a tiny sanitized `demo-workspace/` so users can validate without private data
- Commit demo-only benchmark outputs (never private-corpus results)

Nice-to-have:
- Add a wrapper command or Makefile target to run the standard pipeline
  - distill (staging-only) -> dedupe -> optional apply

## 3) Policy reminders

- Never commit private workspace corpora, telemetry, or benchmarks derived from private data.
- Keep apply optional and human-reviewed for new installs.
- Keep secrets out of always-loaded tiers.
