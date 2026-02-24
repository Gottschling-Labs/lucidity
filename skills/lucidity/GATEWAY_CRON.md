# Lucidity - Gateway cron installation

OpenClaw has a built-in cron scheduler managed by the Gateway.

Using Gateway cron (instead of OS crontab) has two benefits:
- Jobs are visible via `openclaw cron list`.
- Run history can be inspected via `openclaw cron runs`.

## Install (recommended)

```bash
cd skills/lucidity
./install.sh
```

The installer will prompt for:
- workspace root (defaults to `~/.openclaw/workspace`)
- schedule timezone (defaults to the host timezone when detectable)
- verbosity (announce to chat vs silent)
- verification (run a quick health check at the end)

## What it creates

By default it creates these Gateway cron jobs using a prefix derived from agent id + workspace label:

- `lucidity.<agent>.<workspace>.backup` (03:45 daily)
- `lucidity.<agent>.<workspace>.distill` (04:05 daily, deterministic "pending distill" - catches up any unprocessed days)
- `lucidity.<agent>.<workspace>.dedupe` (04:15 daily)

If there is a naming collision, the installer automatically appends a short hash suffix to the workspace label.

Apply is intentionally not scheduled by default.

## Verify

```bash
openclaw cron list | grep lucidity
```

Run a job immediately (debug):

1) Get the job id:

```bash
openclaw cron list | grep lucidity.backup
```

2) Run by id:

```bash
openclaw cron run <job-id>
```

## Uninstall

Use the uninstall script (recommended):

```bash
cd skills/lucidity
./uninstall.sh
```

Or remove jobs manually by id:

```bash
openclaw cron list | grep lucidity
openclaw cron rm <job-id>
```

## Notes

- These jobs run as an isolated agent turn (`--session isolated`) using agent id `main` by default.
- The message payload instructs the agent to run the local Lucidity scripts with `--workspace`.
- OS crontab installation is intentionally not supported; Lucidity uses Gateway cron for scheduled jobs.
