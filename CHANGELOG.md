# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]

### Added

### Changed

### Fixed

### Security

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
