#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
# BUG: hardcoded fixture path ignores AGY_FIXTURE_PATH env var
export AGY_FIXTURE_PATH="${REPO_ROOT}/track-atomic/day-23/fixtures/default.json"
agy version --headless --json
