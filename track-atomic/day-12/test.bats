#!/usr/bin/env bats
# track-atomic/day-12/test.bats
# Tests for Day 12: JSON Schema Validation for Spark Artifacts

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  if [ -d "${REPO_ROOT}/.venv/bin" ]; then
    export PATH="${REPO_ROOT}/mock-bin:${REPO_ROOT}/.venv/bin:${PATH}"
  else
    export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  fi
  export AGY_OFFLINE_MODE=1
}

@test "solution: validates schema and outputs VALID status" {
  run python3 "$BATS_TEST_DIRNAME/solution/validate_artifact.py"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.status == "VALID"'
}

@test "solution: rejects invalid artifact missing required fields" {
  run python3 -c "
import sys
sys.path.insert(0, '$BATS_TEST_DIRNAME/solution')
from validate_artifact import validate_and_save
validate_and_save({'name': 'incomplete'})
"
  [ "$status" -ne 0 ]
}

@test "starter: lacks schema validation before saving (the bug)" {
  # Starter does not validate schema — grep confirms missing validation
  run grep -q 'jsonschema' "$BATS_TEST_DIRNAME/starter/validate_artifact.py"
  [ "$status" -ne 0 ]
}
