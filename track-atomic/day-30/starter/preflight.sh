#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
# BUG: set -e causes exit on first failure, results not aggregated
for DAY_DIR in "${REPO_ROOT}"/track-atomic/day-*/; do
  bats "${DAY_DIR}test.bats"
done
echo '{"status": "done"}'
