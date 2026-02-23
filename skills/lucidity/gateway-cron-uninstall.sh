#!/usr/bin/env bash
set -euo pipefail

say() { printf "\n[%s] %s\n" "lucidity" "$*"; }

die() { echo "Error: $*" >&2; exit 1; }

command -v openclaw >/dev/null 2>&1 || die "openclaw CLI not found"

say "Removing Gateway cron jobs..."

for name in lucidity.backup lucidity.distill lucidity.dedupe; do
  if openclaw cron list | grep -q "\b${name}\b"; then
    openclaw cron rm --name "$name" >/dev/null
    say "Removed: $name"
  else
    say "Not found: $name"
  fi
done

say "Done."
