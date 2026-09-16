#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  export AGY_OFFLINE_MODE=1
}

@test "solution bats: all offline assertions pass" {
  run bats "$BATS_TEST_DIRNAME/solution/check_offline.bats"
  [ "$status" -eq 0 ]
}

@test "starter bats: runs but skips offline verification" {
  run bats "$BATS_TEST_DIRNAME/starter/check_offline.bats"
  [ "$status" -eq 0 ]
  run grep -q "which agy" "$BATS_TEST_DIRNAME/starter/check_offline.bats"
  [ "$status" -ne 0 ]
}
