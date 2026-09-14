#!/usr/bin/env bash
set -euo pipefail
# Determine the repo root from the location of this script so the PATH fix
# works regardless of which directory the caller invoked the script from.
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
# Prepend mock-bin so the workshop agy binary is always found first.
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
# Invoke agy version with --headless (non-blocking, no stdin wait) and
# --json (machine-parseable output) for deterministic CI-safe execution.
OUTPUT=$(agy version --headless --json)
echo "$OUTPUT"
