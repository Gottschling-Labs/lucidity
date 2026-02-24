#!/usr/bin/env bash
set -euo pipefail

say() { printf "\n[%s] %s\n" "lucidity" "$*"; }

die() { echo "Error: $*" >&2; exit 1; }

command -v openclaw >/dev/null 2>&1 || die "openclaw CLI not found"

say "Removing Gateway cron jobs..."

AGENT_DEFAULT="main"
read -r -p "Agent id for uninstall? [$AGENT_DEFAULT]: " AGENT_ID
AGENT_ID="${AGENT_ID:-$AGENT_DEFAULT}"

WORKSPACE_ROOT_DEFAULT="${WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"
read -r -p "Workspace root for uninstall (used to derive label)? [$WORKSPACE_ROOT_DEFAULT]: " WORKSPACE_ROOT_IN
WORKSPACE_ROOT_IN="${WORKSPACE_ROOT_IN:-$WORKSPACE_ROOT_DEFAULT}"

WORKSPACE_BASENAME="$(basename "$WORKSPACE_ROOT_IN")"
WORKSPACE_LABEL="$(echo "$WORKSPACE_BASENAME" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"
if [[ -z "$WORKSPACE_LABEL" ]]; then
  WORKSPACE_LABEL="workspace"
fi

SHORT_HASH="$(python3 - <<PY
import hashlib
print(hashlib.sha1("$WORKSPACE_ROOT_IN".encode("utf-8")).hexdigest()[:8])
PY
)"

BASE_PREFIX="lucidity.${AGENT_ID}.${WORKSPACE_LABEL}"
ALT_PREFIX="${BASE_PREFIX}-${SHORT_HASH}"

# NOTE: `openclaw cron rm` expects a job id.
ids=$(openclaw cron list | awk -v p1="$BASE_PREFIX" -v p2="$ALT_PREFIX" '$2 ~ ("^"p1"\\.") || $2 ~ ("^"p2"\\.") {print $1}')
if [[ -z "${ids}" ]]; then
  say "No jobs found for prefixes: $BASE_PREFIX.* or $ALT_PREFIX.*"
  exit 0
fi

for id in $ids; do
  openclaw cron rm "$id" >/dev/null
  say "Removed job id: $id"
done

say "Done."
