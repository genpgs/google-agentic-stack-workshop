#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_FILENAME}")" rev-parse --show-toplevel)"
  if [ -d "${REPO_ROOT}/.venv/bin" ]; then
    export PATH="${REPO_ROOT}/mock-bin:${REPO_ROOT}/.venv/bin:${PATH}"
  else
    export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  fi
}

@test "solution: parameters include type and description" {
  run bash -c "python3 \"${REPO_ROOT}/track-atomic/day-27/solution/gen_capabilities.py\" | jq -e '.parameters.query.type and .parameters.query.description'"
  [ "$status" -eq 0 ]
}

@test "starter: parameters are empty objects, missing type" {
  run bash -c "python3 \"${REPO_ROOT}/track-atomic/day-27/starter/gen_capabilities.py\" | jq -e '.parameters.query == {}'"
  [ "$status" -eq 0 ]
}
