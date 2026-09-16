#!/usr/bin/env bash
set -euo pipefail
# BUG: uses interactive read prompts
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
echo -n "Enter task name: "
read -r TASK
echo -n "Enter category: "
read -r CATEGORY
agy agent dispatch --task "$TASK" --category "$CATEGORY" --headless --json
