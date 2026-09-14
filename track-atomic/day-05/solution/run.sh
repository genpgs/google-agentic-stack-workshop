#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
OUTPUT=$(agy session start --headless --json)
SESSION_TOKEN=$(echo "$OUTPUT" | jq -r '.session_token')
echo "$SESSION_TOKEN"
