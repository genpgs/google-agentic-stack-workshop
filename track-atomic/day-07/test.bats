#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_DIRNAME}")" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution check_exit.bats: exit code assertion passes" {
  run bats track-atomic/day-07/solution/check_exit.bats
  [ "$status" -eq 0 ]
}

@test "starter check_exit.bats: regex-only check is weaker than exit code" {
  run bats track-atomic/day-07/starter/check_exit.bats
  run agy
  [ "$status" -eq 2 ]
}
