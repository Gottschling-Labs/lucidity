# Upgrading Lucidity

Lucidity does not auto-update itself. See `INSTALL.md` for install/reinstall/uninstall.

## Check for updates

```bash
cd /path/to/lucidity
python3 skills/lucidity/scripts/check_update.py
```

If an update is available, the script exits with code 10 and prints recommended commands.

## Upgrade

```bash
cd /path/to/lucidity
git pull --ff-only

# Refresh Gateway cron jobs/payloads if needed
cd skills/lucidity
./gateway-cron-install.sh
```

## Optional: weekly update check via cron (notification-only)

Example line (writes JSON to a local file):

```cron
0 9 * * 1 cd /path/to/lucidity && python3 skills/lucidity/scripts/check_update.py > ~/.openclaw/workspace/state/lucidity-update-check.json 2>&1
```

Notes:
- This does not update code.
- It requires `gh` to be authenticated if using the GitHub API via `gh api`.
