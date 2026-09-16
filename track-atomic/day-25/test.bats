#!/usr/bin/env bats
# track-atomic/day-25/test.bats
# Tests for Day 25: BATS Execution Timeout & Deadlock Guard
#
# Avoids nested bats calls. Instead uses grep to verify the timeout guard exists
# in the solution and is absent in the starter.

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION_BATS="${REPO_ROOT}/track-atomic/day-25/solution/guarded_run.bats"
  STARTER_BATS="${REPO_ROOT}/track-atomic/day-25/starter/guarded_run.bats"
}

@test "solution bats: wraps agy call with 'timeout Ns'" {
  grep -q 'timeout.*agy' "$SOLUTION_BATS"
}

@test "solution bats: checks for exit status 124 (timeout signal)" {
  grep -q '124' "$SOLUTION_BATS"
}

@test "starter bats: 'run agy' is not wrapped with timeout on the same line (the bug)" {
  # Check that a 'run agy' line exists without 'timeout' — confirms the missing guard.
  # Using grep -E to match lines containing 'run agy' but NOT 'timeout'.
  run grep -E '^[^#]*run agy' "$STARTER_BATS"
  [ "$status" -eq 0 ]   # there IS a 'run agy' line
  # That line must NOT contain 'timeout'
  result=$(grep -E '^[^#]*run agy' "$STARTER_BATS" | grep 'timeout' || true)
  [ -z "$result" ]
}

@test "timeout command exits 124 on expiry (ground truth)" {
  run timeout 1s sleep 10
  [ "$status" -eq 124 ]
}

@test "agy version with mock-bin completes well within 10s" {
  run timeout 10s agy version --headless --json
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.metadata.status == "COMPLETED"'
}
