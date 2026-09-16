#!/usr/bin/env bash
set -euo pipefail
# track-atomic/day-14/starter/sandboxed_run.sh
# Day 14 Starter: Buggy runner that creates temp files in the current working directory.

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"

# BUG: creates temp files in current working directory
TMPFILE="./agy_session_$$.json"
agy run --headless --json > "$TMPFILE"
cat "$TMPFILE"
rm -f "$TMPFILE"
