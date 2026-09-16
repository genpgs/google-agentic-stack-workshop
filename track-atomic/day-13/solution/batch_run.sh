#!/usr/bin/env bash
set -euo pipefail
# track-atomic/day-13/solution/batch_run.sh
# Day 13 Solution: Batch runner that captures per-task exit codes and stops on first failure.

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"

TASKS=("task-a" "task-b" "task-c")
FAILED=()

for TASK in "${TASKS[@]}"; do
  RESULT=$(agy batch --task "$TASK" --headless --json) || { FAILED+=("$TASK"); break; }
  echo "$RESULT" | jq -e '.status == "COMPLETED"' > /dev/null
done

if [[ ${#FAILED[@]} -gt 0 ]]; then
  echo "{\"summary\": \"FAILED\", \"failed_tasks\": $(printf '%s' "${FAILED[@]}" | jq -R . | jq -s .)}" >&2
  exit 1
fi

echo '{"summary": "COMPLETED", "status": "COMPLETED"}'
