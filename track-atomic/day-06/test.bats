#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_DIRNAME}")" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: mock-bin/agy is used and returns valid JSON" {
  run track-atomic/day-06/solution/run.py
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.metadata.status == "COMPLETED"'
}

@test "starter: fails without mock-bin on PATH" {
  export PATH="${PATH//${REPO_ROOT}\/mock-bin:/}"
  run track-atomic/day-06/starter/run.py
  [ "$status" -ne 0 ]
}
