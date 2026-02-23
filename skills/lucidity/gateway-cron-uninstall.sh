#!/usr/bin/env bash
set -euo pipefail

say() { printf "\n[%s] %s\n" "lucidity" "$*"; }

die() { echo "Error: $*" >&2; exit 1; }

command -v openclaw >/dev/null 2>&1 || die "openclaw CLI not found"

say "Removing Gateway cron jobs..."

# NOTE: `openclaw cron rm` expects a job id, not a name.

ids=$(openclaw cron list | awk '$2 ~ /^lucidity\./ {print $1}')
if [[ -z "${ids}" ]]; then
  say "No lucidity.* jobs found."
  exit 0
fi

for id in $ids; do
  openclaw cron rm "$id" >/dev/null
  say "Removed job id: $id"
done

say "Done."
