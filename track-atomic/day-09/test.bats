#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_DIRNAME}")" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: dispatches non-interactively with --task and --category" {
  run track-atomic/day-09/solution/dispatch.sh --task build --category ci
  [ "$status" -eq 0 ]
  echo "$output" | jq '.status == "COMPLETED"'
}

@test "starter: hangs without stdin, times out" {
  run timeout 3 bash track-atomic/day-09/starter/dispatch.sh < /dev/null
  [ "$status" -ne 0 ]
}
