# Lucidity - Gateway cron installation

OpenClaw has a built-in cron scheduler managed by the Gateway.

Using Gateway cron (instead of OS crontab) has two benefits:
- Jobs are visible via `openclaw cron list`.
- Run history can be inspected via `openclaw cron runs`.

## Install (recommended)

```bash
cd skills/lucidity
./gateway-cron-install.sh
```

The installer will prompt for:
- workspace root (defaults to `~/.openclaw/workspace`)
- schedule timezone (defaults to the host timezone when detectable)
- verbosity (announce to chat vs silent)

## What it creates

By default it creates these Gateway cron jobs:
- `lucidity.backup` (03:45 daily)
- `lucidity.distill` (04:05 daily, deterministic "pending distill" - catches up any unprocessed days)
- `lucidity.dedupe` (04:15 daily)

Apply is intentionally not scheduled by default.

## Verify

```bash
openclaw cron list | grep lucidity
```

Run a job immediately (debug):

```bash
openclaw cron run --name lucidity.backup
```

## Uninstall

```bash
openclaw cron rm --name lucidity.backup
openclaw cron rm --name lucidity.distill
openclaw cron rm --name lucidity.dedupe
```

## Notes

- These jobs run as an isolated agent turn (`--session isolated`) using agent id `main` by default.
- The message payload instructs the agent to run the local Lucidity scripts with `--workspace`.
- OS crontab installation is intentionally not supported; Lucidity uses Gateway cron for scheduled jobs.
