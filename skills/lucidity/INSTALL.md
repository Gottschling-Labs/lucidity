# Installing Lucidity

This guide covers installation, reinstallation, and uninstall.

Lucidity uses **OpenClaw Gateway cron** for scheduled jobs.

## Install (Gateway cron)

From the repo root:

```bash
cd skills/lucidity
./gateway-cron-install.sh
```

The installer prompts for:
- Workspace root (defaults to `~/.openclaw/workspace`)
- Timezone (auto-detected when possible)
- Verbosity (announce to chat by default)

Verify:

```bash
openclaw cron list | grep lucidity
```

## Reinstall (repair / refresh)

If you want to refresh schedules, workspace path, timezone, or verbosity:

```bash
cd skills/lucidity
./gateway-cron-uninstall.sh
./gateway-cron-install.sh
```

## Uninstall

```bash
cd skills/lucidity
./gateway-cron-uninstall.sh
```

Notes:
- Uninstall removes scheduled jobs, but does not delete your workspace memory files.
- Your memory remains under `~/.openclaw/workspace/memory/`.
