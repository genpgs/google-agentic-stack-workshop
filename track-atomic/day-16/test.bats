#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: exits 0 with COMPLETED status" {
  run timeout 30 bash "$BATS_TEST_DIRNAME/solution/poll_status.sh"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.status == "COMPLETED"'
}

@test "starter: would loop forever — grep confirms the bug" {
  run grep "while true" "$BATS_TEST_DIRNAME/starter/poll_status.sh"
  [ "$status" -eq 0 ]
  run grep -q "MAX_RETRIES" "$BATS_TEST_DIRNAME/starter/poll_status.sh"
  [ "$status" -ne 0 ]
}
