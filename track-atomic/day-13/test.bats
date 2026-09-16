#!/usr/bin/env bats
# track-atomic/day-13/test.bats
# Tests for Day 13: Batch Job Dispatcher — per-task exit code capture
#
# Test 1 – solution: verifies solution/batch_run.sh exits 0 and prints COMPLETED summary.
# Test 2 – starter: verifies starter/batch_run.sh exits 0 but prints "done" (bug: swallows errors).

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION="${REPO_ROOT}/track-atomic/day-13/solution/batch_run.sh"
  STARTER="${REPO_ROOT}/track-atomic/day-13/starter/batch_run.sh"
}

@test "solution: exits 0 and outputs COMPLETED status" {
  run bash "$SOLUTION"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.status == "COMPLETED"'
}

@test "starter: outputs plain 'done' instead of structured status (bug: swallows errors)" {
  run bash "$STARTER"
  [ "$status" -eq 0 ]
  # The buggy starter emits {"summary":"done"} not {"status":"COMPLETED"}
  echo "$output" | jq -e '.summary == "done"'
}

@test "solution: contains per-task failure tracking (FAILED array)" {
  grep -q 'FAILED' "$SOLUTION"
}

@test "starter: uses '|| true' to swallow exit codes (the bug)" {
  grep -q '|| true' "$STARTER"
}
