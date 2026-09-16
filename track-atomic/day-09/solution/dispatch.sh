#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
TASK=""
CATEGORY=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --task) TASK="$2"; shift 2 ;;
    --category) CATEGORY="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done
[[ -z "$TASK" ]] && { echo "--task is required" >&2; exit 1; }
[[ -z "$CATEGORY" ]] && { echo "--category is required" >&2; exit 1; }
OUTPUT=$(agy agent dispatch --task "$TASK" --category "$CATEGORY" --headless --json)
echo "$OUTPUT" | jq -e '.task_id and .status' >/dev/null
echo "$OUTPUT"
