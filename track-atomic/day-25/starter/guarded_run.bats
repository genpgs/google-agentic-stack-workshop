#!/usr/bin/env bats
# BUG: no timeout wrapper — agy deadlock would hang the entire CI suite
setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}
@test "agy runs" {
  run agy version --headless --json
  [ "$status" -eq 0 ]
}
