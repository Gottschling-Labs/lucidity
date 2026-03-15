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
- installation mode:
  - `dream` (recommended) — quiet-by-default Dream Mode
  - `custom` — advanced/custom setup
- reporting mode (`silent` by default, `announce` optional)
- verification (run a quick health check at the end)

## What it creates

In **Dream Mode** (recommended), it creates these Gateway cron jobs using a prefix derived from agent id + workspace label:

- `lucidity.<agent>.<workspace>.backup` (03:45 daily)
- `lucidity.<agent>.<workspace>.reflect` (04:00 daily, Dream Reflection - LLM proposes stronger semantic/procedural candidates into staging)
- `lucidity.<agent>.<workspace>.distill` (04:05 daily, deterministic catch-up for missed daily files and lower-tier episodic preservation)
- `lucidity.<agent>.<workspace>.dedupe` (04:15 daily)
- `lucidity.<agent>.<workspace>.apply` (04:25 daily, autonomous promotion of durable high-confidence semantic/procedural memory)

In **Custom** mode, reflection and autonomous promotion are still configurable via prompts.

If there is a naming collision, the installer automatically appends a short hash suffix to the workspace label.

Episodic memory is preserved in lower tiers/searchable outputs by default; autonomous promotion is intended for durable semantic/procedural memory, not direct canonization of raw episodic context.

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
