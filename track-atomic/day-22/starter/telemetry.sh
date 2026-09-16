#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
# BUG: emits plain text logs, breaks jq consumers
echo "INFO: Starting agent execution"
agy run --headless --json > /dev/null
echo "ERROR: Task failed unexpectedly"
echo "INFO: Cleanup complete"
