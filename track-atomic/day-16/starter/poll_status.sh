#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
TASK_ID="${1:-mock-task-1001}"
# BUG: unbounded loop, no sleep, no max retries — hangs CI
while true; do
  STATUS=$(agy status --task "$TASK_ID" --headless --json | jq -r '.status')
  if [[ "$STATUS" == "COMPLETED" ]]; then
    echo "COMPLETED"
    break
  fi
done
