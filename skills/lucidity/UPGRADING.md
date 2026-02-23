# Upgrading Lucidity

Lucidity does not auto-update itself. See `INSTALL.md` for install/reinstall/uninstall.

## Check for updates

```bash
cd ~/code/gottschling-labs/lucidity
python3 skills/lucidity/scripts/check_update.py
```

If an update is available, the script exits with code 10 and prints recommended commands.

## Upgrade

```bash
cd ~/code/gottschling-labs/lucidity
git pull --ff-only

# Refresh cron job block if needed
cd skills/lucidity
./gateway-cron-install.sh
```

## Optional: weekly update check via cron (notification-only)

Example line (writes JSON to a local file):

```cron
0 9 * * 1 cd ~/code/gottschling-labs/lucidity && python3 skills/lucidity/scripts/check_update.py > ~/.openclaw/workspace/state/lucidity-update-check.json 2>&1
```

Notes:
- This does not update code.
- It requires `gh` to be authenticated if using the GitHub API via `gh api`.
