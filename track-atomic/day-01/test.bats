#!/usr/bin/env bats
# track-atomic/day-01/test.bats
# Automated grader for Day 01: Antigravity CLI Binary Path & Version Probe.

setup() {
  # Resolve the repo root from the location of this test file so that the
  # PATH fix applies even when bats is invoked from a different directory.
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_FILENAME}")" rev-parse --show-toplevel)"
  export REPO_ROOT
  # Prepend mock-bin so the workshop agy binary is available to all tests.
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

# ---------------------------------------------------------------------------
# Test 1 — solution/run.sh must exit 0 and emit valid JSON with
#           metadata.status == "COMPLETED"
# ---------------------------------------------------------------------------
@test "solution: exits 0 and outputs valid JSON" {
  run bash "${REPO_ROOT}/track-atomic/day-01/solution/run.sh"
  [ "$status" -eq 0 ]
}

@test "solution: output is valid JSON" {
  run bash "${REPO_ROOT}/track-atomic/day-01/solution/run.sh"
  [ "$status" -eq 0 ]
  # jq will exit non-zero if the input is not valid JSON
  echo "$output" | jq empty
}

@test "solution: metadata.status equals COMPLETED" {
  run bash "${REPO_ROOT}/track-atomic/day-01/solution/run.sh"
  [ "$status" -eq 0 ]
  result="$(echo "$output" | jq -r '.metadata.status')"
  [ "$result" = "COMPLETED" ]
}

# ---------------------------------------------------------------------------
# Test 2 — starter/run.sh must either fail (exit non-zero) OR produce output
#           that is NOT valid JSON with metadata.status == "COMPLETED".
#           Both conditions indicate the bug is present and unfixed.
# ---------------------------------------------------------------------------
@test "starter: fails or produces non-headless output (bug must be present)" {
  # Remove mock-bin from PATH so the starter truly has no access to the mock
  # agy binary — mirroring the buggy environment described in the README.
  local CLEAN_PATH
  CLEAN_PATH="$(echo "$PATH" | tr ':' '\n' | grep -v 'mock-bin' | tr '\n' ':' | sed 's/:$//')"

  # Run the starter under the stripped PATH. We accept either:
  #   a) non-zero exit code (binary not found / command failed), OR
  #   b) exit 0 but metadata.status != "COMPLETED" (wrong output format)
  PATH="$CLEAN_PATH" run bash "${REPO_ROOT}/track-atomic/day-01/starter/run.sh" || true

  if [ "$status" -eq 0 ]; then
    # Script somehow exited 0 — verify the output is NOT the expected JSON
    result="$(echo "$output" | jq -r '.metadata.status' 2>/dev/null || echo "INVALID")"
    [ "$result" != "COMPLETED" ]
  fi
  # If status != 0 the bug is confirmed; test passes implicitly.
}
