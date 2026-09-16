#!/usr/bin/env bash
set -euo pipefail
# track-atomic/day-13/starter/batch_run.sh
# Day 13 Starter: Buggy batch runner that swallows per-task exit codes.

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"

TASKS=("task-a" "task-b" "task-c")

for TASK in "${TASKS[@]}"; do
  # BUG: exit code of agy is swallowed; no early exit on failure
  agy batch --task "$TASK" --headless --json || true
done

echo '{"summary": "done"}'
