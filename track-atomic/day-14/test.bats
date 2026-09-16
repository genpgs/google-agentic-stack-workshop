#!/usr/bin/env bats
# track-atomic/day-14/test.bats
# Tests for Day 14: Environment Isolation & Sandbox — mktemp vs CWD temp files
#
# Test 1 – solution: exits 0, returns COMPLETED JSON, and leaves NO temp file in CWD.
# Test 2 – starter: exits 0 but creates temp file in CWD (the bug confirmed by file presence).

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION="${REPO_ROOT}/track-atomic/day-14/solution/sandboxed_run.sh"
  STARTER="${REPO_ROOT}/track-atomic/day-14/starter/sandboxed_run.sh"
  # Run from a known temp directory to detect CWD pollution
  TESTDIR="$(mktemp -d)"
}

teardown() {
  rm -rf "$TESTDIR"
}

@test "solution: exits 0 and outputs COMPLETED JSON" {
  run bash "$SOLUTION"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.metadata.status == "COMPLETED"'
}

@test "solution: does NOT leave temp files in CWD (uses mktemp sandbox)" {
  cd "$TESTDIR"
  bash "$SOLUTION" > /dev/null
  # No agy_session_*.json files should exist in CWD
  local count
  count=$(find . -maxdepth 1 -name 'agy_session_*.json' | wc -l)
  [ "$count" -eq 0 ]
}

@test "starter: contains the CWD temp file bug (./agy_session_\$\$.json)" {
  grep -q 'agy_session_' "$STARTER"
  # The starter writes to ./ not mktemp
  grep -q '\./agy_session' "$STARTER"
}

@test "solution: uses mktemp -d for sandboxed execution" {
  grep -q 'mktemp -d' "$SOLUTION"
  grep -q 'trap.*EXIT' "$SOLUTION"
}
