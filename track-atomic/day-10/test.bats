#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_DIRNAME}")" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: captures stderr and logs structured JSON on failure" {
  run bash -c "track-atomic/day-10/solution/run_with_log.py 2> /tmp/agy_err.log"
  [ "$status" -ne 0 ]
  cat /tmp/agy_err.log | jq -e '.event == "agy_subprocess_failed"'
}

@test "starter: swallows stderr, no structured log on failure" {
  run bash -c "track-atomic/day-10/starter/run_with_log.py 2> /tmp/starter_err.log"
  [ "$status" -ne 0 ]
  run bash -c "jq . /tmp/starter_err.log 2>/dev/null | grep -q '\"event\"'"
  [ "$status" -ne 0 ]
}
