#!/usr/bin/env bats
# track-atomic/day-07/test.bats
# Tests for Day 07: BATS Exit Code Assertion
#
# Avoids nested bats calls (bats-in-bats is fragile).
# Instead:
#   Test 1 – solution: verifies the solution bats file contains proper exit-code assertion.
#   Test 2 – starter: verifies the starter bats file ONLY checks stdout pattern (the bug).
#   Test 3 – direct: runs agy with no args and asserts exit code 2 (ground truth).

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION_BATS="${REPO_ROOT}/track-atomic/day-07/solution/check_exit.bats"
  STARTER_BATS="${REPO_ROOT}/track-atomic/day-07/starter/check_exit.bats"
}

@test "solution check_exit.bats: asserts exit status -eq 2" {
  grep -q '\[ "\$status" -eq 2 \]' "$SOLUTION_BATS"
}

@test "solution check_exit.bats: checks stderr for INVALID_ARGUMENT" {
  grep -q 'INVALID_ARGUMENT' "$SOLUTION_BATS"
}

@test "starter check_exit.bats: only checks stdout pattern — missing exit code assertion (the bug)" {
  # Starter should NOT contain the status assertion
  run grep -q '\[ "\$status" -eq 2 \]' "$STARTER_BATS"
  [ "$status" -ne 0 ]
}

@test "agy with no args actually exits 2 (ground truth)" {
  run agy
  [ "$status" -eq 2 ]
}
