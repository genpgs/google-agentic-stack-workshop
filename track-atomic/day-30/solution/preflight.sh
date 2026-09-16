#!/usr/bin/env bash
set -euo pipefail

if ! command -v bats &>/dev/null; then
  echo '{"error": "bats not found"}' >&2
  exit 1
fi

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"

PASSED=0
FAILED=0
FAILED_DAYS=()

for DAY_DIR in "${REPO_ROOT}"/track-atomic/day-*/; do
  DAY=$(basename "$DAY_DIR")
  BATS_FILE="${DAY_DIR}test.bats"
  [[ ! -f "$BATS_FILE" ]] && continue
  
  if bats "$BATS_FILE" > /dev/null 2>&1; then
    PASSED=$((PASSED + 1))
  else
    FAILED=$((FAILED + 1))
    FAILED_DAYS+=("$DAY")
  fi
done

TOTAL=$((PASSED + FAILED))
SUMMARY=$(printf '{"total": %d, "passed": %d, "failed": %d, "failed_days": %s, "status": "%s"}' \
  "$TOTAL" "$PASSED" "$FAILED" \
  "$(printf '%s\n' "${FAILED_DAYS[@]:-}" | jq -R . | jq -s . 2>/dev/null || echo '[]')" \
  "$([ "$FAILED" -eq 0 ] && echo COMPLETED || echo FAILED)")

echo "$SUMMARY"
[ "$FAILED" -eq 0 ] || exit 1
