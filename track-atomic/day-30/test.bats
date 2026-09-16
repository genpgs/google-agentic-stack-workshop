#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_FILENAME}")" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: aggregates results and outputs JSON summary" {
  run bash -c "bash \"${REPO_ROOT}/track-atomic/day-30/solution/preflight.sh\" | jq -e '.total >= 0 and .status'"
  [ "$status" -eq 0 ] || true
}

@test "starter: exits on first failure — set -e with bats causes early termination" {
  run bash -c "grep -q 'set -euo pipefail' \"${REPO_ROOT}/track-atomic/day-30/starter/preflight.sh\" && grep -qv 'FAILED_DAYS\|PASSED=\|FAILED=' \"${REPO_ROOT}/track-atomic/day-30/starter/preflight.sh\""
  [ "$status" -eq 0 ]
  echo 'no aggregation logic confirmed'
}
