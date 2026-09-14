#!/usr/bin/env bash
set -euo pipefail
# BUG: PATH does not include mock-bin, so agy cannot be found.
# BUG: Uses grep/head/cut to parse JSON instead of jq. This is fragile:
#      - It may match the wrong "status" key (e.g. from a nested object).
#      - It will silently produce an empty or incorrect string.
#      - It does NOT use jq --exit-status, so a missing field won't cause
#        a non-zero exit, hiding failures from the CI pipeline.
OUTPUT=$(agy run --headless --json)
STATUS=$(echo "$OUTPUT" | grep '"status"' | head -1 | cut -d'"' -f4)
echo "$STATUS"
