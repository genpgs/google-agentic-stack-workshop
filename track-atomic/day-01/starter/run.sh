#!/usr/bin/env bash
set -euo pipefail
# BUG: PATH does not include mock-bin, so the wrong agy binary may be found (or
#      the command will fail entirely with "command not found").
# BUG: Missing --headless and --json flags, so output is human-readable text
#      rather than machine-parseable JSON. In a CI environment this may also
#      block waiting for terminal input.
OUTPUT=$(agy version)
echo "$OUTPUT"
