#!/usr/bin/env bats
# track-atomic/day-15/test.bats
# Tests for Day 15: Gemini Spark Tool Call Serialization

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  if [ -d "${REPO_ROOT}/.venv/bin" ]; then
    export PATH="${REPO_ROOT}/mock-bin:${REPO_ROOT}/.venv/bin:${PATH}"
  else
    export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  fi
  export AGY_OFFLINE_MODE=1
}

@test "solution: serializes tool call using camelCase schema keys" {
  run python3 "$BATS_TEST_DIRNAME/solution/serialize_tool.py"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.functionName and .inputSchema.parameterType and .inputSchema.parameterDescription'
}

@test "solution: round-trip invariance holds" {
  run python3 "$BATS_TEST_DIRNAME/solution/serialize_tool.py"
  [ "$status" -eq 0 ]
}

@test "starter: uses snake_case keys — lacks required camelCase API keys (the bug)" {
  run python3 "$BATS_TEST_DIRNAME/starter/serialize_tool.py"
  [ "$status" -eq 0 ]
  # Assert camelCase functionName is absent in starter output
  run bash -c "python3 \"$BATS_TEST_DIRNAME/starter/serialize_tool.py\" | jq -e '.functionName'"
  [ "$status" -ne 0 ]
  # Assert snake_case function_name is present (confirming the bug)
  run bash -c "python3 \"$BATS_TEST_DIRNAME/starter/serialize_tool.py\" | jq -e '.function_name'"
  [ "$status" -eq 0 ]
}
