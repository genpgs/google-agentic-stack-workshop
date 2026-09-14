#!/usr/bin/env bash
set -euo pipefail
# BUG: Checks live endpoint when GEMINI_API_KEY is missing
# BUG: Does not set AGY_OFFLINE_MODE=1
if [ -z "${GEMINI_API_KEY:-}" ]; then
  curl -sf https://api.gemini.example.com/health || echo "Network check failed"
fi
agy run --headless --json
