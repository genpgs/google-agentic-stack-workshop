#!/usr/bin/env bats
# track-atomic/day-04/test.bats
# Tests for Day 04: Antigravity CLI Config Initialization (Python)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
REPO_ROOT="$(git -C "$(dirname "$BATS_TEST_FILENAME")" rev-parse --show-toplevel)"
DAY04_DIR="${REPO_ROOT}/track-atomic/day-04"

# ---------------------------------------------------------------------------
# Test 1: Solution — exits 0 from /tmp and outputs valid JSON
# ---------------------------------------------------------------------------
@test "day-04 solution: exits 0 when run from /tmp (absolute path resolution)" {
  # Run from /tmp to prove cwd does not matter
  run bash -c "cd /tmp && python3 '${DAY04_DIR}/solution/config_loader.py'"
  echo "status: $status"
  echo "output: $output"
  [ "$status" -eq 0 ]
}

@test "day-04 solution: output is valid JSON containing headless_default=true" {
  run bash -c "cd /tmp && python3 '${DAY04_DIR}/solution/config_loader.py'"
  [ "$status" -eq 0 ]
  # Output must be parseable JSON
  echo "$output" | python3 -c "import sys, json; d=json.load(sys.stdin); assert d['headless_default'] is True, 'headless_default must be True'; assert d['status'] == 'VALID', 'status must be VALID'"
}

@test "day-04 solution: output JSON contains status key equal to VALID" {
  run bash -c "cd /tmp && python3 '${DAY04_DIR}/solution/config_loader.py'"
  [ "$status" -eq 0 ]
  [[ "$output" == *'"status"'* ]]
  [[ "$output" == *'"VALID"'* ]]
}

# ---------------------------------------------------------------------------
# Test 2: Starter — fails when run from /tmp (relative path breaks)
# ---------------------------------------------------------------------------
@test "day-04 starter: exits non-zero when run from /tmp (relative path bug)" {
  # /tmp/agy.config.json does not exist, so open() will raise FileNotFoundError
  run bash -c "cd /tmp && python3 '${DAY04_DIR}/starter/config_loader.py'"
  echo "status: $status"
  echo "output: $output"
  [ "$status" -ne 0 ]
}

@test "day-04 starter: succeeds when run from its own directory (relative path resolves)" {
  # When cwd is the starter directory, 'agy.config.json' resolves correctly
  run bash -c "cd '${DAY04_DIR}/starter' && python3 config_loader.py"
  [ "$status" -eq 0 ]
  [[ "$output" == *"headless_default: True"* ]]
}
