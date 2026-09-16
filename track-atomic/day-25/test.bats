#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution bats: all tests pass with timeout guard" {
  run bats "$BATS_TEST_DIRNAME/solution/guarded_run.bats"
  [ "$status" -eq 0 ]
}

@test "starter bats: lacks timeout — grep confirms bug" {
  run bash -c "grep -v 'timeout' \"$BATS_TEST_DIRNAME/starter/guarded_run.bats\" | grep -q 'run agy'"
  [ "$status" -eq 0 ]
}
