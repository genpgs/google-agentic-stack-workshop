#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: matches command with trailing whitespace" {
  run python3 "$BATS_TEST_DIRNAME/solution/interceptor.py"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.status == "COMPLETED"'
}

@test "starter: returns NO MATCH due to whitespace bug" {
  OUTPUT=$(python3 "$BATS_TEST_DIRNAME/starter/interceptor.py")
  [ "$OUTPUT" = "NO MATCH" ]
}
