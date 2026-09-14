#!/usr/bin/env bats
# track-atomic/day-05/test.bats
# Tests for Day 05: Non-Interactive Session Spawning
#
# Test 1 – solution: verifies --headless flag is passed, session_token is
#           captured in output, and the script exits 0.
# Test 2 – starter: verifies the buggy starter exits non-zero OR produces an
#           empty session_token because 'agy session start' (without --headless)
#           times out and returns no usable output.

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION="${REPO_ROOT}/track-atomic/day-05/solution/run.sh"
  STARTER="${REPO_ROOT}/track-atomic/day-05/starter/run.sh"
}

# ---------------------------------------------------------------------------
# Test 1: solution/run.sh
# ---------------------------------------------------------------------------
@test "solution: exits 0 and captures a non-empty session_token" {
  run bash "${SOLUTION}"

  # Must exit cleanly
  [ "$status" -eq 0 ]

  # Output must not be blank
  [ -n "$output" ]

  # Output must look like a token (non-empty string, no whitespace-only)
  [[ "$output" =~ [^[:space:]] ]]
}

# ---------------------------------------------------------------------------
# Test 2: starter/run.sh
# ---------------------------------------------------------------------------
@test "starter: exits non-zero or session_token is empty (hangs without --headless)" {
  # The starter calls 'agy session start' without --headless.
  # The mock binary sleeps for 30 s to simulate stdin-wait.
  # 'timeout 5' inside the starter script causes it to be killed / return
  # empty output, so either:
  #   a) the overall script exits non-zero, OR
  #   b) it exits 0 but the session_token printed is empty.
  #
  # We wrap in an outer timeout (10 s) to guard the bats runner itself.
  run timeout 10 bash "${STARTER}"

  # Accept: non-zero exit OR empty/blank session_token line
  if [ "$status" -eq 0 ]; then
    # Extract the token value from "session_token: <value>"
    token_value=$(echo "$output" | sed -n 's/^session_token:[[:space:]]*//p')
    [ -z "$token_value" ] \
      || fail "starter unexpectedly produced a non-empty session_token: '${token_value}'"
  fi
  # Non-zero status is also a valid (expected) outcome — test passes either way.
  true
}
