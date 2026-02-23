# Productionization — Require-Review Mode (First 7 Days)

Goal: make new installs safe by default by requiring a human review before any canonical write.

## Modes
- `dry-run`: never writes; generates manifest + suggested diffs
- `require-review`: generates diff bundle and exits non-zero unless an explicit approval token is present
- `write`: performs merge writes

## Suggested mechanism
- `apply_staging.py --require-review` generates:
  - `memory/staging/review-bundles/<ts>/manifest.json`
  - `memory/staging/review-bundles/<ts>/patches/*.diff`
- User approves by:
  - running `apply_staging.py --write --approve <bundle-id>`

## Default policy for new installs
- For the first 7 days after install:
  - run nightly distill+dedupe
  - run apply in `--require-review` mode
- After 7 days (or manual override), switch cron to `--write`

## Config
- Add to `memory-architecture/config/auto-merge.json`:
  - `install.createdAt`
  - `install.reviewDays`

(Implementation pending.)
