#!/usr/bin/env bats
# track-atomic/day-23/test.bats
# Tests for Day 23: Mock CLI Fixture Override Mechanism
#
# Fix: added [ "$status" -ne 0 ] fallback guard and explicit assertion that
# starter output does NOT match the custom fixture (proving it hardcoded its path).

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION="${REPO_ROOT}/track-atomic/day-23/solution/use_fixture.sh"
  STARTER="${REPO_ROOT}/track-atomic/day-23/starter/use_fixture.sh"
}

@test "solution: respects custom AGY_FIXTURE_PATH" {
  TMP_FIXTURE="$(mktemp)"
  printf '{"custom": true, "status": "FIXTURE_OVERRIDE"}' > "$TMP_FIXTURE"
  export AGY_FIXTURE_PATH="$TMP_FIXTURE"
  run bash "$SOLUTION"
  rm -f "$TMP_FIXTURE"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.custom == true'
}

@test "starter: hardcodes fixture path — ignores AGY_FIXTURE_PATH (the bug)" {
  TMP_FIXTURE="$(mktemp)"
  printf '{"custom": true, "status": "FIXTURE_OVERRIDE"}' > "$TMP_FIXTURE"
  export AGY_FIXTURE_PATH="$TMP_FIXTURE"
  # Starter overwrites AGY_FIXTURE_PATH with its hardcoded path, so custom fixture is ignored.
  # Either the script fails (hardcoded path doesn't exist) or output lacks .custom == true.
  run bash "$STARTER"
  rm -f "$TMP_FIXTURE"
  # Either exit non-zero OR output does not have .custom == true
  if [ "$status" -eq 0 ]; then
    run bash -c "echo $(printf '%q' "$output") | jq -e '.custom == true'"
    [ "$status" -ne 0 ] || fail "starter unexpectedly served the custom fixture"
  fi
  true
}

@test "starter: contains hardcoded AGY_FIXTURE_PATH assignment (the bug)" {
  grep -q 'AGY_FIXTURE_PATH=' "$STARTER"
  # It must NOT check if already set (that's the fix)
  run grep -q '\${AGY_FIXTURE_PATH:-\}' "$STARTER"
  [ "$status" -ne 0 ]
}

@test "solution: only sets AGY_FIXTURE_PATH if not already set (the fix)" {
  grep -q '\${AGY_FIXTURE_PATH:-}' "$SOLUTION"
}
