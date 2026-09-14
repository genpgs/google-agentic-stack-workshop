#!/usr/bin/env bash
set -euo pipefail
# Determine the repo root from the location of this script so the PATH fix
# works regardless of which directory the caller invoked the script from.
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
# Prepend mock-bin so the workshop agy binary is always found first.
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
# Pipe agy output directly into jq.
# --exit-status causes jq to exit non-zero when the selected value is
# null or false, turning missing fields into detectable CI failures.
STATUS=$(agy run --headless --json | jq --exit-status '.metadata.status')
echo "$STATUS"
