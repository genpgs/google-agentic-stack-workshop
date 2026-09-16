#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
# FIX: respect AGY_FIXTURE_PATH if already set, else use default
if [[ -z "${AGY_FIXTURE_PATH:-}" ]]; then
  export AGY_FIXTURE_PATH="${REPO_ROOT}/track-atomic/day-23/fixtures/default.json"
fi
OUTPUT=$(agy version --headless --json)
echo "$OUTPUT"
