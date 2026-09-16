#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_FILENAME}")" rev-parse --show-toplevel)"
  if [ -d "${REPO_ROOT}/.venv/bin" ]; then
    export PATH="${REPO_ROOT}/mock-bin:${REPO_ROOT}/.venv/bin:${PATH}"
  else
    export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  fi
}

@test "solution: verifies local deps without network" {
  run bash -c "python3 \"${REPO_ROOT}/track-atomic/day-29/solution/verify_deps.py\" | jq -e '.results[\"pkg:pytest\"].installed == true'"
  [ "$status" -eq 0 ]
}

@test "starter: uses pip index (network call) — grep confirms bug" {
  run bash -c "grep -q 'pip.*index.*versions\|pip index' \"${REPO_ROOT}/track-atomic/day-29/starter/verify_deps.py\""
  [ "$status" -eq 0 ]
  echo 'remote call confirmed'
}
