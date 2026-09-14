#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
export AGY_OFFLINE_MODE=1
OUTPUT=$(AGY_OFFLINE_MODE=1 agy run --headless --json)
STATUS=$(echo "$OUTPUT" | jq -r '.metadata.status')
echo "$STATUS"
