#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"

log() {
  local severity="$1"
  local message="$2"
  printf '{"severity":"%s","message":"%s"}\n' "$severity" "$message"
}

log INFO "Starting agent execution"
OUTPUT=$(agy run --headless --json)
STATUS=$(echo "$OUTPUT" | jq -r '.metadata.status')
if [[ "$STATUS" != "COMPLETED" ]]; then
  log ERROR "Task failed with status: $STATUS"
  exit 1
fi
log INFO "Cleanup complete"
