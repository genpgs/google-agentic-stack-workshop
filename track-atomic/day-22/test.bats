#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: all output lines are valid JSON with severity" {
  run bash "$BATS_TEST_DIRNAME/solution/telemetry.sh"
  while IFS= read -r line; do
    echo "$line" | jq -e '.severity and .message' > /dev/null
  done <<< "$output"
}

@test "starter: output contains plain text, fails jq parse" {
  FIRST_LINE=$(bash "$BATS_TEST_DIRNAME/starter/telemetry.sh" | head -1)
  run jq . <<< "$FIRST_LINE"
  [ "$status" -ne 0 ]
}
