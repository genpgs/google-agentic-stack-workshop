#!/usr/bin/env bats
# SOLUTION: correctly asserts exit code 2 and structured error JSON
setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}
@test "agy with no args exits with status 2" {
  run agy
  [ "$status" -eq 2 ]
}
@test "agy with no args emits INVALID_ARGUMENT on stderr" {
  bats_require_minimum_version 1.5.0
  run --separate-stderr agy
  echo "$stderr" | jq -e '.code == "INVALID_ARGUMENT"'
}
