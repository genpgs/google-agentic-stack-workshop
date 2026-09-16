#!/usr/bin/env bats
# SOLUTION: full offline boundary assertions
setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  export AGY_OFFLINE_MODE=1
  unset GEMINI_API_KEY 2>/dev/null || true
}
@test "agy resolves to mock-bin/agy" {
  AGY_PATH="$(which agy)"
  [[ "$AGY_PATH" == */mock-bin/agy ]]
}
@test "agy runs offline and returns valid JSON" {
  run agy version --headless --json
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.metadata.headless == true'
}
@test "no real network binary is referenced" {
  AGY_PATH="$(which agy)"
  [[ "$AGY_PATH" != /usr/bin/agy ]] && [[ "$AGY_PATH" != /usr/local/bin/agy ]]
}
