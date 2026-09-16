#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: respects custom AGY_FIXTURE_PATH" {
  TMP_FIXTURE=$(mktemp)
  echo '{"custom": true}' > "$TMP_FIXTURE"
  export AGY_FIXTURE_PATH="$TMP_FIXTURE"
  run bash "$BATS_TEST_DIRNAME/solution/use_fixture.sh"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.custom == true' > /dev/null
  rm -f "$TMP_FIXTURE"
}

@test "starter: hardcodes path, ignores AGY_FIXTURE_PATH override" {
  TMP_FIXTURE=$(mktemp)
  echo '{"custom": true}' > "$TMP_FIXTURE"
  export AGY_FIXTURE_PATH="$TMP_FIXTURE"
  run bash "$BATS_TEST_DIRNAME/starter/use_fixture.sh"
  echo "$output" | jq -e '.metadata.version == "2.0.0-mock"' > /dev/null
  rm -f "$TMP_FIXTURE"
}
