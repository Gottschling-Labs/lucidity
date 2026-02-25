# Installing Lucidity

This guide covers installation, reinstallation, and uninstall.

Lucidity uses **OpenClaw Gateway cron** for scheduled jobs.

## Install (Gateway cron)

From the repo root:

```bash
cd skills/lucidity
./install.sh
```

The installer derives job names from:
- agent id (default: `main`)
- workspace label (derived from the workspace folder name)

This prevents collisions when you install Lucidity for multiple workspaces.

The installer prompts for:
- Workspace root (defaults to `~/.openclaw/workspace`)
- Timezone (auto-detected when possible)
- Verbosity (announce to chat by default)
- Optional: enable Dream Reflection (LLM reflection into staging)

Verify:

```bash
openclaw cron list | grep lucidity
openclaw cron status
openclaw status --deep
```

The installer can also run this verification automatically if you answer "yes" when prompted.

## Reinstall (repair / refresh)

If you want to refresh schedules, workspace path, timezone, verbosity, or the job payloads after upgrading the repo:

```bash
cd skills/lucidity
./uninstall.sh
./install.sh
```

Why this matters:
- Gateway cron jobs store a message payload.
- If Lucidity releases a new version that changes which script the job should run (e.g., switching distill to deterministic `distill_pending.py`), reinstalling ensures your existing cron jobs pick up the latest payload.

## Uninstall

```bash
cd skills/lucidity
./uninstall.sh
```

Notes:
- Uninstall removes scheduled jobs, but does not delete your workspace memory files.
- Your memory remains under `~/.openclaw/workspace/memory/`.
