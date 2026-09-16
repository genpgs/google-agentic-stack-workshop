#!/usr/bin/env bats
# BUG: checks stdout pattern instead of exit code
setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}
@test "agy with no args produces error output" {
  run agy
  # BUG: only checks stdout, not exit code
  [[ "$output" == *"agy"* ]]
}
