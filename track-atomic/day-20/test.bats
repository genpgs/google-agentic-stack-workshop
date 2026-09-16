#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$BATS_TEST_DIRNAME" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
}

@test "solution: passes metacharacter input safely as list arg" {
  run python3 "$BATS_TEST_DIRNAME/solution/sanitize_args.py"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.status == "COMPLETED"'
}

@test "starter: uses shell=True — grep confirms the bug" {
  run grep -q 'shell=True' "$BATS_TEST_DIRNAME/starter/sanitize_args.py"
  [ "$status" -eq 0 ]
  echo "BUG confirmed"
}
