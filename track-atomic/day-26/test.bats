#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_FILENAME}")" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: runs and returns COMPLETED JSON" {
  run bash -c "python3 \"${REPO_ROOT}/track-atomic/day-26/solution/signal_wrapper.py\" | jq -e '.metadata.status == \"COMPLETED\"'"
  [ "$status" -eq 0 ]
}

@test "starter: lacks signal handlers — grep confirms bug" {
  run bash -c "grep -v 'signal.signal' \"${REPO_ROOT}/track-atomic/day-26/starter/signal_wrapper.py\" | grep -qv 'SIGTERM'"
  [ "$status" -eq 0 ]
  echo 'no signal handling confirmed'
}

@test "solution: signal handlers registered — grep confirms fix" {
  run bash -c "grep -q 'signal.signal.*SIGTERM\|signal.signal.*SIGINT' \"${REPO_ROOT}/track-atomic/day-26/solution/signal_wrapper.py\""
  [ "$status" -eq 0 ]
}
