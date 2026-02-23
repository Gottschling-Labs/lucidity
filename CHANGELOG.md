# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]

### Added

### Changed

### Fixed

### Security

## [0.1.7] - 2026-02-23

### Added
- Chat command cheat sheet (`skills/lucidity/CHAT_COMMANDS.md`).
- Deterministic helper wrapper (`skills/lucidity/scripts/lucidity_chat.py`).

## [0.1.6] - 2026-02-23

### Fixed
- Gateway cron uninstall script now removes jobs by id (compatible with current OpenClaw CLI).
- Gateway cron install now uses deterministic catch-up distill (`distill_pending.py`) by default.

### Docs
- INSTALL guide explains why reinstalling refreshes Gateway cron payloads.

## [0.1.5] - 2026-02-23

### Added
- Deterministic catch-up distill (`distill_pending.py`) to process any unprocessed daily logs.

### Changed
- Gateway cron distill job now uses pending distill to avoid missing days.

## [0.1.4] - 2026-02-23

### Added
- Comparisons and compatibility section (OpenClaw memory-core / "Elite LTM", mem0, other RAG stacks).

## [0.1.3] - 2026-02-23

### Changed
- Removed OS crontab installer. Lucidity now uses Gateway cron only for scheduled jobs.

## [0.1.2] - 2026-02-23

### Added
- Gateway cron installer (`skills/lucidity/gateway-cron-install.sh`) so jobs show up in `openclaw cron list`.

### Changed
- Documentation now recommends Gateway cron by default.

## [0.1.1] - 2026-02-23

### Added
- Update notification script (`skills/lucidity/scripts/check_update.py`) and repo `VERSION` file.

## [0.1.0] - 2026-02-23

### Added
- Initial public-ready packaging of the Lucidity skill under `skills/lucidity/`.
- Tier architecture documentation (T0-T4) and retrieval dependencies.
- Local-first scripts for distill, dedupe, apply, backup, rollback, prune, and stats.
- CI workflow that compiles scripts and runs the idempotency regression test.
- Governance docs: `CONTRIBUTING.md`, `SECURITY.md`, and this changelog.
- GPL-3.0-or-later licensing.
