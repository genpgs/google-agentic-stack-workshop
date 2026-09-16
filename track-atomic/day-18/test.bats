#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: produces valid JSON with timestamp" {
  run python3 "$BATS_TEST_DIRNAME/solution/generate_manifest.py"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.monorepo_version and .timestamp'
}

@test "starter: raises TypeError — exits non-zero" {
  run python3 "$BATS_TEST_DIRNAME/starter/generate_manifest.py"
  [ "$status" -ne 0 ]
}
