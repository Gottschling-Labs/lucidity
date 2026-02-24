#!/usr/bin/env bash
set -euo pipefail

# Back-compat wrapper (deprecated). Use ./install.sh
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$DIR/install.sh" "$@"
