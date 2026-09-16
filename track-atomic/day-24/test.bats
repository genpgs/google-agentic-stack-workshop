#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: rejects spec missing autograder block" {
  run bash -c "python3 \"$BATS_TEST_DIRNAME/solution/validate_manifest.py\" | jq -e '.valid == false and (.errors | length > 0)'"
  [ "$status" -eq 0 ]
}

@test "starter: incorrectly accepts spec missing autograder" {
  run bash -c "python3 \"$BATS_TEST_DIRNAME/starter/validate_manifest.py\" | jq -e '.valid == true'"
  [ "$status" -eq 0 ]
}
