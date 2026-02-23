# Lucidity - Critical Repo Review (Pre-Public)

This is a maintainers' review of the repository with recommended additions/edits before making the repo public.

## What looks solid

- Clear skill packaging under `skills/lucidity/`
- Staging-first design and non-destructive defaults
- Backups + rollback tooling present
- CI sanity + idempotency regression present
- Governance basics present: `CONTRIBUTING.md`, `SECURITY.md`
- License present: GPL-3.0-or-later

## Gaps / recommended additions before going public

### 1) CODE_OF_CONDUCT.md (recommended)
Add a standard Contributor Covenant. This is not strictly required but is common for public repos.

### 2) Release versioning + changelog
Currently the repo has a skill version in `skills/lucidity/SKILL.md`, but public users will expect:
- `CHANGELOG.md` at repo root, or at least a release section in `README.md`
- A git tag, e.g. `v0.1.0`

### 3) Clarify what is "OpenClaw-specific" vs "portable"
Add a short section explaining:
- Which parts assume OpenClaw tools (`memory_search`, `memory_get`)
- Which parts are just scripts operating on Markdown files

### 4) Add a "Public safe defaults" section
Make it extremely obvious that:
- cron installs staging-only distill + dedupe by default
- apply is optional and should be human-reviewed for new installs

### 5) Provide a demo corpus + demo benchmark outputs (optional but helpful)
To help users verify the system without touching private data:
- include a tiny sanitized demo workspace (`demo-workspace/`)
- commit demo benchmark outputs only

### 6) Script UX improvements (nice-to-have)
Consider adding:
- `--help` output examples in the docs
- consistent `--workspace` argument support across scripts (verify already consistent)
- a single wrapper command (e.g., `lucidity run --staging-only`) to reduce cognitive load

## Notes on dash/typography policy

Repo was scrubbed to remove em dashes/en dashes in favor of ASCII hyphens for consistency.

## Suggested next PR scope

Small, public-ready PR:
- add `CODE_OF_CONDUCT.md`
- add root `CHANGELOG.md`
- add a short "safe defaults" section to root README
- optionally add demo corpus + demo benchmark outputs
