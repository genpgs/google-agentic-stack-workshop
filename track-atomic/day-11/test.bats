#!/usr/bin/env bats
# track-atomic/day-11/test.bats
# Tests for Day 11: Deterministic Response Fixture Parser

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  if [ -d "${REPO_ROOT}/.venv/bin" ]; then
    export PATH="${REPO_ROOT}/mock-bin:${REPO_ROOT}/.venv/bin:${PATH}"
  else
    export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  fi
  export AGY_OFFLINE_MODE=1
}

@test "solution: parses NDJSON stream and outputs completed status" {
  run python3 "$BATS_TEST_DIRNAME/solution/parse_stream.py"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.status == "COMPLETED" and .chunks == 3'
}

@test "starter: crashes on NDJSON stream (JSONDecodeError)" {
  run python3 "$BATS_TEST_DIRNAME/starter/parse_stream.py"
  [ "$status" -ne 0 ]
}
