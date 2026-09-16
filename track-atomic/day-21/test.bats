#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: preserves all 3 turns including tool result" {
  run bash -c "python3 \"$BATS_TEST_DIRNAME/solution/state_reducer.py\" | jq -e '.turns | length == 3'"
  [ "$status" -eq 0 ]
}

@test "starter: drops history, only 1 turn remains" {
  run bash -c "python3 \"$BATS_TEST_DIRNAME/starter/state_reducer.py\" | jq -e '.turns | length == 1'"
  [ "$status" -eq 0 ]
}
