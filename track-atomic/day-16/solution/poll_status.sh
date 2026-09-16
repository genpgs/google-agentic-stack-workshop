#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
TASK_ID="${1:-mock-task-1001}"
MAX_RETRIES=10
SLEEP_SEC=1
for ((i=1; i<=MAX_RETRIES; i++)); do
  STATUS=$(agy status --task "$TASK_ID" --headless --json | jq -r '.metadata.status')
  if [[ "$STATUS" == "COMPLETED" ]]; then
    echo '{"status": "COMPLETED", "attempts": '"$i"'}'
    exit 0
  fi
  sleep "$SLEEP_SEC"
done
echo '{"status": "TIMEOUT"}' >&2
exit 1
