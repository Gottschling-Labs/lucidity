# Maintainers - Lucidity

This file replaces `PUBLIC_RELEASE_AUDIT.md` and `CRITICAL_REVIEW.md`.

It is intentionally concise and is safe to keep in the public repo.

## 1) Public release checklist (status)

Overall status: **Public**.

### Repository hygiene
- [x] Repo contains only Lucidity skill + documentation
- [x] `mission-control/` removed and ignored
- [x] No private-corpus benchmark artifacts tracked

### Security / secrets
- [x] Basic secret-pattern scan over tracked files (no hits)
- [x] Scripts are local-first; no network calls required by default
- [x] Hardening guide (`skills/lucidity/HARDENING.md`)
- [x] Sandboxing guide (`skills/lucidity/SANDBOXING.md`)

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
- [x] Root quickstart: "clone, install, verify" (Gateway cron)
- [x] Explicit safe-defaults callout in root README
- [x] Demo workspace committed (sanitized)
- [x] Apply (promotion) guide (manual + automation maturity model)
- [x] Gateway cron guide (`skills/lucidity/GATEWAY_CRON.md`)
- [x] Upgrade guide (`skills/lucidity/UPGRADING.md`)

### Releases
- [x] License: GPL-3.0-or-later
- [x] Root `CHANGELOG.md`
- [x] Tags published (v0.1.0+)

## 2) Ongoing improvements (post-public)

Nice-to-have (future):
- Add a wrapper command or Makefile target to run the standard pipeline
  - distill -> dedupe -> optional apply
- Add a demo-only benchmark harness + committed demo outputs (never private-corpus results)
- Add CI smoke test that runs the demo pipeline with `--workspace demo-workspace`

## 3) Versioning policy (SemVer)

Lucidity follows SemVer with practical guidance:

- Patch (0.1.x -> 0.1.(x+1))
  - Docs/typos, CI tweaks, internal refactors that do not change behavior
  - Bug fixes that do not change interfaces or defaults

- Minor (0.x -> 0.(x+1))
  - New features that are backward compatible
  - Changes to scheduling/installers that remain backward compatible (wrappers and legacy uninstall supported)
  - Meaningful new capabilities that users will rely on

- Major (1.x -> 2.0.0)
  - Breaking changes: removed/renamed commands without compatibility shims
  - Default behavior becomes more destructive (e.g., apply --write enabled by default)
  - Incompatible changes to canonical file layout or manifest formats

## 4) Policy reminders

- Never commit private workspace corpora, telemetry, or benchmarks derived from private data.
- Keep apply optional and human-reviewed for new installs.
- Keep secrets out of always-loaded tiers.
