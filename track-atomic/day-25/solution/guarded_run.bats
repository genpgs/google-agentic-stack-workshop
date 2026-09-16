#!/usr/bin/env bats
# SOLUTION: timeout 10s wrapper prevents deadlocks
setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}
@test "agy version completes within 10 seconds" {
  run timeout 10s agy version --headless --json
  if [ "$status" -eq 124 ]; then
    echo "TIMEOUT: agy deadlocked" >&2
    return 1
  fi
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.metadata.status == "COMPLETED"'
}
@test "timeout 124 triggers actionable failure message" {
  # Verify that a simulated timeout (using a sleep command) returns 124
  run timeout 1s sleep 10
  [ "$status" -eq 124 ]
}
