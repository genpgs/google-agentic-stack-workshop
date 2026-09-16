#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_DIRNAME}")" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: payload is valid JSON with role tag" {
  run bash -c "track-atomic/day-08/solution/build_prompt.py | jq -e '.prompt'"
  [ "$status" -eq 0 ]
}

@test "starter: raw f-string produces invalid JSON" {
  run bash -c "track-atomic/day-08/starter/build_prompt.py | jq ."
  [ "$status" -ne 0 ]
}
