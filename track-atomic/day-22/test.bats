#!/usr/bin/env bats
# track-atomic/day-22/test.bats
# Tests for Day 22: Headless Failure Telemetry Formatter
#
# Fix for silent-pass bug: old test used `while read` on $output which silently
# passes if output is empty. Replaced with explicit line count check + per-line validation.

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION="${REPO_ROOT}/track-atomic/day-22/solution/telemetry.sh"
  STARTER="${REPO_ROOT}/track-atomic/day-22/starter/telemetry.sh"
}

@test "solution: produces at least 2 output lines" {
  run bash "$SOLUTION"
  [ "$status" -eq 0 ]
  local line_count
  line_count=$(echo "$output" | grep -c .)
  [ "$line_count" -ge 2 ]
}

@test "solution: every output line is valid JSON with severity and message fields" {
  run bash "$SOLUTION"
  [ "$status" -eq 0 ]
  # Verify each non-empty line parses as JSON with required fields
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    echo "$line" | jq -e '.severity and .message' > /dev/null \
      || { echo "Line failed jq check: $line" >&2; return 1; }
  done <<< "$output"
}

@test "starter: first output line is plain text (not JSON)" {
  FIRST_LINE=$(bash "$STARTER" | head -1)
  # Plain text should fail jq parsing
  run bash -c "echo $(printf '%q' "$FIRST_LINE") | jq ."
  [ "$status" -ne 0 ]
}

@test "solution: uses log() function for structured output" {
  grep -q 'log()' "$SOLUTION"
  grep -q 'severity' "$SOLUTION"
}
