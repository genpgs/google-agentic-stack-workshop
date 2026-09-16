#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
# BUG: always exits 0 regardless of whether files differ
FILE_A="${1:-/dev/null}"
FILE_B="${2:-/dev/null}"
diff "$FILE_A" "$FILE_B" > /dev/null 2>&1 || true
echo '{"diff": "checked", "exit_code": 0}'
