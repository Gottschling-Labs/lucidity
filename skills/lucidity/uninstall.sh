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

# NOTE: use JSON output because the human list output truncates long names.
ids=$(openclaw cron list --json | python3 -c 'import json,sys; obj=json.load(sys.stdin); p1=sys.argv[1]; p2=sys.argv[2]; ids=[j["id"] for j in obj.get("jobs",[]) if j.get("name","" ).startswith(p1+".") or j.get("name","" ).startswith(p2+".")]; print("\n".join(ids))' "$BASE_PREFIX" "$ALT_PREFIX")

# Back-compat: older installers used global names (no agent/workspace prefix)
legacy_ids=$(openclaw cron list --json | python3 -c 'import json,sys; obj=json.load(sys.stdin); names={"lucidity.backup","lucidity.distill","lucidity.dedupe"}; ids=[j["id"] for j in obj.get("jobs",[]) if j.get("name") in names]; print("\n".join(ids))')

if [[ -z "${ids}" ]] && [[ -z "${legacy_ids}" ]]; then
  say "No jobs found for prefixes: $BASE_PREFIX.* or $ALT_PREFIX.* (and no legacy lucidity.* jobs found)"
  exit 0
fi

for id in $ids; do
  openclaw cron rm "$id" >/dev/null
  say "Removed job id: $id"
done

if [[ -n "${legacy_ids}" ]]; then
  say "Removing legacy lucidity.* jobs (from older installers)"
  for id in $legacy_ids; do
    openclaw cron rm "$id" >/dev/null
    say "Removed legacy job id: $id"
  done
fi

say "Done."
