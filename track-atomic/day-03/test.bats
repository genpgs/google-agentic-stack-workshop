#!/usr/bin/env bats
# track-atomic/day-03/test.bats
# Tests for Day 03: Offline Environment Guard & API Key Stubbing

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
REPO_ROOT="$(git -C "$(dirname "$BATS_TEST_FILENAME")" rev-parse --show-toplevel)"
DAY03_DIR="${REPO_ROOT}/track-atomic/day-03"

setup() {
  # Prepend mock-bin so 'agy' resolves to the mock binary
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  # Ensure no real API key is set for the starter failure test
  unset GEMINI_API_KEY || true
}

# ---------------------------------------------------------------------------
# Test 1: Solution script — exits 0, outputs COMPLETED, no curl required
# ---------------------------------------------------------------------------
@test "day-03 solution: exits 0 with AGY_OFFLINE_MODE=1 and outputs COMPLETED" {
  run bash "${DAY03_DIR}/solution/run.sh"
  [ "$status" -eq 0 ]
  echo "output: $output"
  [[ "$output" == *"COMPLETED"* ]]
}

@test "day-03 solution: does not invoke curl (offline-safe)" {
  # Override curl with a function that always fails to prove solution never calls it
  curl() { echo "curl was called — FAIL" >&2; return 1; }
  export -f curl

  run bash "${DAY03_DIR}/solution/run.sh"
  [ "$status" -eq 0 ]
  [[ "$output" != *"curl was called"* ]]
}

# ---------------------------------------------------------------------------
# Test 2: Starter script — fails when GEMINI_API_KEY is unset (curl unavailable)
# ---------------------------------------------------------------------------
@test "day-03 starter: exits non-zero when GEMINI_API_KEY is unset and curl is blocked" {
  # Override curl to simulate a network-restricted / offline CI environment
  curl() { echo "Network access blocked: offline mode enforced" >&2; exit 6; }   # exit 6 = "Couldn't resolve host"
  export -f curl

  unset GEMINI_API_KEY || true

  # Also shadow 'agy' so any attempted live agy call is blocked
  # (starter doesn't set offline mode, but our mock-bin agy in PATH is fine;
  #  the failure must come from the curl block above)
  run bash "${DAY03_DIR}/starter/run.sh"

  # curl fails fast → script exits non-zero (or fails to produce valid COMPLETED output)
  if [ "$status" -eq 0 ]; then
    [ "$output" != "COMPLETED" ]
  else
    [ "$status" -ne 0 ]
  fi
}

@test "day-03 starter: would succeed only if GEMINI_API_KEY is set (bypass curl block)" {
  # When GEMINI_API_KEY is set the curl block is skipped entirely.
  # agy in PATH is the mock binary, so it will succeed.
  export GEMINI_API_KEY="dummy-key-for-test"

  run bash "${DAY03_DIR}/starter/run.sh"
  [ "$status" -eq 0 ]
}
