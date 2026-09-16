#!/usr/bin/env bats

setup() {
  REPO_ROOT="$(git -C "$(dirname "${BATS_TEST_FILENAME}")" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  
  echo "content" > "${BATS_TMPDIR}/identical_a.txt"
  echo "content" > "${BATS_TMPDIR}/identical_b.txt"
  echo "content_a" > "${BATS_TMPDIR}/different_a.txt"
  echo "content_b" > "${BATS_TMPDIR}/different_b.txt"
}

@test "solution: returns non-zero when files are identical" {
  run bash "${REPO_ROOT}/track-atomic/day-28/solution/assess_diff.sh" "${BATS_TMPDIR}/identical_a.txt" "${BATS_TMPDIR}/identical_b.txt"
  [ "$status" -ne 0 ]
}

@test "solution: returns 0 and JSON when files differ" {
  run bash "${REPO_ROOT}/track-atomic/day-28/solution/assess_diff.sh" "${BATS_TMPDIR}/different_a.txt" "${BATS_TMPDIR}/different_b.txt"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.identical == false'
}

@test "starter: returns 0 even when files are identical" {
  run bash "${REPO_ROOT}/track-atomic/day-28/starter/assess_diff.sh" "${BATS_TMPDIR}/identical_a.txt" "${BATS_TMPDIR}/identical_b.txt"
  [ "$status" -eq 0 ]
}
