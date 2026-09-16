#!/usr/bin/env bats
# BUG: no offline isolation assertion, no mock-bin check
setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}
@test "agy runs" {
  run agy version --headless --json
  [ "$status" -eq 0 ]
  # BUG: does not assert offline mode or that mock-bin/agy was used
}
