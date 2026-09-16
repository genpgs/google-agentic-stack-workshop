#!/usr/bin/env bats
# track-atomic/day-09/test.bats
# Tests for Day 09: Headless Agent Dispatcher Script
#
# Fix 1: Use absolute path ($BATS_TEST_DIRNAME) instead of relative path
#         "track-atomic/day-09/..." which fails if bats is run from any directory
#         other than the repo root.
# Fix 2: REPO_ROOT uses $BATS_TEST_DIRNAME directly (not dirname of dirname).
# Fix 3: solution test uses jq -e so a false return value from jq fails the test.

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION="${REPO_ROOT}/track-atomic/day-09/solution/dispatch.sh"
  STARTER="${REPO_ROOT}/track-atomic/day-09/starter/dispatch.sh"
}

@test "solution: dispatches non-interactively with --task and --category" {
  run bash "$SOLUTION" --task build --category ci
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.status == "COMPLETED"'
}

@test "starter: hangs without stdin — timeout kills it (the bug)" {
  run timeout 3 bash "$STARTER" < /dev/null
  # Either timeout (exit 124) or read failure (non-zero) — both are non-zero
  [ "$status" -ne 0 ]
}
