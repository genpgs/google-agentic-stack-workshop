#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
FILE_A="${1:-}"
FILE_B="${2:-}"
[[ -z "$FILE_A" || -z "$FILE_B" ]] && { echo '{"error": "Usage: assess_diff.sh <file_a> <file_b>"}' >&2; exit 2; }
if diff -q "$FILE_A" "$FILE_B" > /dev/null 2>&1; then
  echo '{"identical": true, "lines_changed": 0, "status": "IDENTICAL"}' >&2
  exit 1  # FIX: non-zero when identical (it's a bug if starter == solution)
fi
CHANGED=$(diff "$FILE_A" "$FILE_B" | grep -c '^[<>]' || true)
echo "{\"identical\": false, \"lines_changed\": ${CHANGED}, \"status\": \"DIFFERS\"}"
