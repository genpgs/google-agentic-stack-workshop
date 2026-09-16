#!/usr/bin/env bats
# track-atomic/day-02/test.bats
# Automated grader for Day 02: Headless Output Deserialization with jq.

setup() {
  # Resolve the repo root from the location of this test file so that the
  # PATH fix applies even when bats is invoked from a different directory.
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_FILENAME}")" rev-parse --show-toplevel)"
  export REPO_ROOT
  # Prepend mock-bin so the workshop agy binary is available to all tests.
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

# ---------------------------------------------------------------------------
# Test 1 — solution/run.sh must exit 0 and print '"COMPLETED"' (the jq
#           JSON-encoded string, including surrounding double-quotes).
# ---------------------------------------------------------------------------
@test "solution: exits 0" {
  run bash "${REPO_ROOT}/track-atomic/day-02/solution/run.sh"
  [ "$status" -eq 0 ]
}

@test "solution: output is \"COMPLETED\"" {
  run bash "${REPO_ROOT}/track-atomic/day-02/solution/run.sh"
  [ "$status" -eq 0 ]
  # jq prints strings with surrounding double-quotes; strip trailing whitespace.
  trimmed="$(echo "$output" | tr -d '[:space:]')"
  [ "$trimmed" = '"COMPLETED"' ]
}

# ---------------------------------------------------------------------------
# Test 2 — starter/run.sh must either fail (exit non-zero due to missing PATH)
#           OR produce output that is not the correct '"COMPLETED"' string
#           (demonstrating the broken grep/head/cut parsing).
# ---------------------------------------------------------------------------
@test "starter: fails or produces incorrect status (bug must be present)" {
  # Strip mock-bin from PATH so the starter truly lacks access to the agy binary.
  local CLEAN_PATH
  CLEAN_PATH="$(echo "$PATH" | tr ':' '\n' | grep -v 'mock-bin' | tr '\n' ':' | sed 's/:$//')"

  # Allow the command to fail; we evaluate the outcome manually below.
  PATH="$CLEAN_PATH" run bash "${REPO_ROOT}/track-atomic/day-02/starter/run.sh" || true

  if [ "$status" -eq 0 ]; then
    # Script exited 0 — verify output is NOT the correct jq-encoded value.
    trimmed="$(echo "$output" | tr -d '[:space:]')"
    [ "$trimmed" != '"COMPLETED"' ]
  fi
  # If status != 0 the bug is confirmed (binary not found); test passes.
}
