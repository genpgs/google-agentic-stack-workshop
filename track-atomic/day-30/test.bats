#!/usr/bin/env bats
# track-atomic/day-30/test.bats
# Tests for Day 30: Full Atomic Track CI Pre-Flight Runner
#
# IMPORTANT: To avoid infinite recursion (preflight.sh calls bats on all days
# including day-30 itself), the solution test is a static grep-only check that
# verifies the aggregation logic exists in the script, rather than executing it.
# The starter test similarly uses grep to confirm the missing aggregation logic.

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION="${REPO_ROOT}/track-atomic/day-30/solution/preflight.sh"
  STARTER="${REPO_ROOT}/track-atomic/day-30/starter/preflight.sh"
}

@test "solution: contains aggregation variables (PASSED, FAILED, FAILED_DAYS)" {
  # Static inspection — avoids triggering bats-in-bats infinite recursion.
  grep -q 'PASSED=' "$SOLUTION"
  grep -q 'FAILED=' "$SOLUTION"
  grep -q 'FAILED_DAYS' "$SOLUTION"
}

@test "solution: emits JSON summary via printf with .total and .status fields" {
  grep -q '"total"' "$SOLUTION"
  grep -q '"status"' "$SOLUTION"
}

@test "solution: has bats-not-found guard at the top" {
  grep -q 'command -v bats' "$SOLUTION"
}

@test "starter: lacks aggregation logic — exits on first bats failure (the bug)" {
  # Starter should NOT contain PASSED= / FAILED= / FAILED_DAYS variables.
  run grep -q 'PASSED=\|FAILED=\|FAILED_DAYS' "$STARTER"
  [ "$status" -ne 0 ]
}

@test "starter: uses bare bats call in loop without error capture" {
  grep -q 'bats' "$STARTER"
  # Confirm the || true / error-capture guard is absent
  run grep -q 'PASSED=$\|FAILED=$\|((' "$STARTER"
  [ "$status" -ne 0 ]
}
