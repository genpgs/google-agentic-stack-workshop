#!/usr/bin/env bash
set -euo pipefail
# BUG: Missing --headless flag - this will cause agy to hang waiting for stdin
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
# BUG: no --headless flag - will hang indefinitely
OUTPUT=$(timeout 5 agy session start --json || true)
SESSION_TOKEN=$(echo "$OUTPUT" | jq -r '.session_token // empty')
echo "session_token: $SESSION_TOKEN"
