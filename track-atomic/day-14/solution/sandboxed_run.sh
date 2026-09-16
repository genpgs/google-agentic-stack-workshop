#!/usr/bin/env bash
set -euo pipefail
# track-atomic/day-14/solution/sandboxed_run.sh
# Day 14 Solution: Uses mktemp -d for an isolated sandbox and traps EXIT for cleanup.

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

agy run --headless --json --workdir "$WORKDIR" > "$WORKDIR/output.json"
cat "$WORKDIR/output.json" | jq -e '.metadata.status == "COMPLETED"' > /dev/null
cat "$WORKDIR/output.json"
