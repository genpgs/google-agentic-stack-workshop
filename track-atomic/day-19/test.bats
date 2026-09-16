#!/usr/bin/env bats
# track-atomic/day-19/test.bats
# Tests for Day 19: BATS Mock Verification for Network Egress Block
#
# The key spec requirement: starter bats file LACKS offline isolation assertions.
# False-negative fix: instead of running the starter (which passes because mock-bin is
# on PATH regardless), use grep to confirm the starter is MISSING the required checks.

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  export AGY_OFFLINE_MODE=1
  SOLUTION_BATS="${REPO_ROOT}/track-atomic/day-19/solution/check_offline.bats"
  STARTER_BATS="${REPO_ROOT}/track-atomic/day-19/starter/check_offline.bats"
}

@test "solution bats: contains 'which agy' path assertion" {
  grep -q 'which agy' "$SOLUTION_BATS"
}

@test "solution bats: asserts mock-bin path is used" {
  grep -q 'mock-bin/agy' "$SOLUTION_BATS"
}

@test "solution bats: unsets GEMINI_API_KEY" {
  grep -q 'unset GEMINI_API_KEY' "$SOLUTION_BATS"
}

@test "starter bats: does NOT contain AGY_OFFLINE_MODE export (the bug)" {
  run grep -q 'AGY_OFFLINE_MODE' "$STARTER_BATS"
  [ "$status" -ne 0 ]
}

@test "starter bats: does NOT unset GEMINI_API_KEY (offline isolation missing)" {
  run grep -q 'unset GEMINI_API_KEY' "$STARTER_BATS"
  [ "$status" -ne 0 ]
}

@test "agy resolves to mock-bin/agy in test environment" {
  AGY_PATH="$(which agy)"
  [[ "$AGY_PATH" == */mock-bin/agy ]]
}
