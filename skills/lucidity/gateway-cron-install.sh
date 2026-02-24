#!/usr/bin/env bash
set -euo pipefail

# Install Lucidity maintenance as OpenClaw Gateway cron jobs.
# This creates VISIBLE jobs in the Gateway scheduler (openclaw cron list).

say() { printf "\n[%s] %s\n" "lucidity" "$*"; }

die() { echo "Error: $*" >&2; exit 1; }

command -v openclaw >/dev/null 2>&1 || die "openclaw CLI not found"
command -v python3 >/dev/null 2>&1 || die "python3 not found"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT_DEFAULT="${WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"

TZ_DEFAULT=""
if command -v timedatectl >/dev/null 2>&1; then
  TZ_DEFAULT="$(timedatectl show -p Timezone --value 2>/dev/null || true)"
fi
if [[ -z "$TZ_DEFAULT" ]] && [[ -f /etc/timezone ]]; then
  TZ_DEFAULT="$(cat /etc/timezone | tr -d ' \t\n\r')"
fi

say "Gateway cron install"
say "Repo root: $REPO_ROOT"
say "Skill dir: $SKILL_DIR"

# Agent id controls which OpenClaw agent/session runs the cron job.
AGENT_DEFAULT="main"
read -r -p "Agent id to run these jobs as? [$AGENT_DEFAULT]: " AGENT_ID
AGENT_ID="${AGENT_ID:-$AGENT_DEFAULT}"

read -r -p "Workspace root to maintain? [$WORKSPACE_ROOT_DEFAULT]: " WORKSPACE_ROOT_IN
WORKSPACE_ROOT_IN="${WORKSPACE_ROOT_IN:-$WORKSPACE_ROOT_DEFAULT}"

# Derive a readable workspace label from the folder name.
WORKSPACE_BASENAME="$(basename "$WORKSPACE_ROOT_IN")"
WORKSPACE_LABEL="$(echo "$WORKSPACE_BASENAME" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"
if [[ -z "$WORKSPACE_LABEL" ]]; then
  WORKSPACE_LABEL="workspace"
fi

# If multiple workspaces share the same label for the same agent, append a stable short hash.
SHORT_HASH="$(python3 - <<PY
import hashlib
print(hashlib.sha1("$WORKSPACE_ROOT_IN".encode("utf-8")).hexdigest()[:8])
PY
)"

JOB_PREFIX="lucidity.${AGENT_ID}.${WORKSPACE_LABEL}"
if openclaw cron list | awk '{print $2}' | grep -qx "${JOB_PREFIX}.backup"; then
  JOB_PREFIX="${JOB_PREFIX}-${SHORT_HASH}"
fi

say "Job prefix: ${JOB_PREFIX}.*"

read -r -p "Timezone for schedules (IANA). Leave blank to use Gateway default. [$TZ_DEFAULT]: " TZ_IN
TZ_IN="${TZ_IN:-$TZ_DEFAULT}"

say "Cron verbosity"
say "- announce: send a short summary to chat each run (default)"
say "- silent: do not announce"
read -r -p "Announce to chat? (announce/silent) [announce]: " VERB
VERB="${VERB:-announce}"

ANNOUNCE_FLAG=""
if [[ "$VERB" == "announce" ]]; then
  ANNOUNCE_FLAG="--announce"
elif [[ "$VERB" == "silent" ]]; then
  ANNOUNCE_FLAG="--no-deliver"
else
  die "Invalid verbosity: $VERB"
fi

# Schedules (local timezone via --tz when set)
# - backup: 03:45 daily
# - distill: 04:05 daily (staging-only)
# - dedupe: 04:15 daily

say "Initializing workspace directories"
mkdir -p "$WORKSPACE_ROOT_IN/memory/staging" \
         "$WORKSPACE_ROOT_IN/memory/staging/deduped" \
         "$WORKSPACE_ROOT_IN/memory/staging/reports" \
         "$WORKSPACE_ROOT_IN/state" \
         "$WORKSPACE_ROOT_IN/backups"

say "Creating Gateway cron jobs..."

COMMON=(
  --session isolated
  --agent "$AGENT_ID"
  $ANNOUNCE_FLAG
  --name
)

TZ_ARGS=()
if [[ -n "$TZ_IN" ]]; then
  TZ_ARGS=(--tz "$TZ_IN")
fi

# Backup
openclaw cron add \
  --name "${JOB_PREFIX}.backup" \
  --description "Lucidity nightly backup (agent=$AGENT_ID workspace=$WORKSPACE_ROOT_IN)" \
  --cron "45 3 * * *" \
  "${TZ_ARGS[@]}" \
  --session isolated \
  --agent "$AGENT_ID" \
  $ANNOUNCE_FLAG \
  --message "Run Lucidity backup for workspace '$WORKSPACE_ROOT_IN'. Execute: python3 '$SKILL_DIR/memory-architecture/scripts/backup_memory.py' --workspace '$WORKSPACE_ROOT_IN' --write. Then print the JSON output." \
  >/dev/null

# Distill (deterministic catch-up)
openclaw cron add \
  --name "${JOB_PREFIX}.distill" \
  --description "Lucidity nightly distill (deterministic catch-up) (agent=$AGENT_ID workspace=$WORKSPACE_ROOT_IN)" \
  --cron "5 4 * * *" \
  "${TZ_ARGS[@]}" \
  --session isolated \
  --agent "$AGENT_ID" \
  $ANNOUNCE_FLAG \
  --message "Run Lucidity pending distill for workspace '$WORKSPACE_ROOT_IN'. Execute: python3 '$SKILL_DIR/memory-architecture/scripts/distill_pending.py' --workspace '$WORKSPACE_ROOT_IN' --limit 7. If it exits 2 (no pending), report that as OK." \
  >/dev/null

# Dedupe
openclaw cron add \
  --name "${JOB_PREFIX}.dedupe" \
  --description "Lucidity nightly dedupe (agent=$AGENT_ID workspace=$WORKSPACE_ROOT_IN)" \
  --cron "15 4 * * *" \
  "${TZ_ARGS[@]}" \
  --session isolated \
  --agent "$AGENT_ID" \
  $ANNOUNCE_FLAG \
  --message "Run Lucidity dedupe for workspace '$WORKSPACE_ROOT_IN'. Execute: python3 '$SKILL_DIR/memory-architecture/scripts/dedupe_staging.py' --workspace '$WORKSPACE_ROOT_IN' --write. Then print the JSON report." \
  >/dev/null

say "Done."

read -r -p "Run installation verification now? (yes/no) [yes]: " VERIFY
VERIFY="${VERIFY:-yes}"
if [[ "$VERIFY" == "yes" ]]; then
  say "Verification: listing installed jobs"
  openclaw cron list | grep "${JOB_PREFIX}" || true
  say "Verification: gateway cron status"
  openclaw cron status || true
  say "Verification: memory-core health (best effort)"
  openclaw status --deep || true
  say "Verification complete."
else
  say "Skipped verification. You can verify later with: openclaw cron list | grep ${JOB_PREFIX}"
fi
