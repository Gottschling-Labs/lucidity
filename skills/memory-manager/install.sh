#!/usr/bin/env bash
set -euo pipefail

# Lucidity installer (cron-based default)
# Safe-by-default: staging-first, backups enabled.

WORKSPACE_ROOT="${WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

say() { printf "\n[%s] %s\n" "lucidity" "$*"; }

die() { echo "Error: $*" >&2; exit 1; }

command -v python3 >/dev/null 2>&1 || die "python3 not found"
command -v crontab >/dev/null 2>&1 || die "crontab not found"

say "Workspace root: $WORKSPACE_ROOT"

say "Consent + privacy"
read -r -p "Enable Lucidity maintenance jobs for this workspace? (yes/no): " CONSENT
if [[ "$CONSENT" != "yes" ]]; then
  say "Aborted (no changes made)."
  exit 0
fi

say "Initializing directories"
mkdir -p "$WORKSPACE_ROOT/memory/staging" \
         "$WORKSPACE_ROOT/memory/staging/deduped" \
         "$WORKSPACE_ROOT/memory/staging/reports" \
         "$WORKSPACE_ROOT/state" \
         "$WORKSPACE_ROOT/backups"

say "Installing cron jobs"
# NOTE: We keep the commands simple and workspace-relative.
# You can edit schedules in: skills/memory-manager/memory-architecture/automation-jobs.md

CRON_MARK_BEGIN="# BEGIN lucidity"
CRON_MARK_END="# END lucidity"

CURRENT_CRON="$(crontab -l 2>/dev/null || true)"
# Remove old block if present
STRIPPED="$(printf "%s\n" "$CURRENT_CRON" | awk -v b="$CRON_MARK_BEGIN" -v e="$CRON_MARK_END" '
  $0==b{in=1;next}
  $0==e{in=0;next}
  !in{print}
')"

# Default schedules (ET assumed by system cron):
# - 03:45 daily backups
# - 04:05 daily staging distill+dedupe (non-destructive)
# Apply is NOT enabled by default.

NEW_BLOCK=$(cat <<EOF
$CRON_MARK_BEGIN
45 3 * * * WORKSPACE_ROOT="$WORKSPACE_ROOT" python3 "$SKILL_DIR/memory-architecture/scripts/backup_memory.py" --workspace "$WORKSPACE_ROOT" >/dev/null 2>&1
5 4 * * * WORKSPACE_ROOT="$WORKSPACE_ROOT" python3 "$SKILL_DIR/memory-architecture/scripts/distill_daily.py" --workspace "$WORKSPACE_ROOT" --staging-only >/dev/null 2>&1
15 4 * * * WORKSPACE_ROOT="$WORKSPACE_ROOT" python3 "$SKILL_DIR/memory-architecture/scripts/dedupe_staging.py" --workspace "$WORKSPACE_ROOT" >/dev/null 2>&1
$CRON_MARK_END
EOF
)

printf "%s\n%s\n" "$STRIPPED" "$NEW_BLOCK" | crontab -

say "Done."
say "Next steps:"
say "- Review docs: $SKILL_DIR/memory-architecture/README.md"
say "- Run a first pass manually (optional):"
say "  python3 $SKILL_DIR/memory-architecture/scripts/distill_daily.py --workspace $WORKSPACE_ROOT --staging-only"
say "  python3 $SKILL_DIR/memory-architecture/scripts/dedupe_staging.py --workspace $WORKSPACE_ROOT"
