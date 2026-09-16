#!/usr/bin/env bats
# track-atomic/day-08/test.bats
# Tests for Day 08: Gemini Spark Prompt Assembly & JSON Escaping
#
# The Day 08 exercise is about safe payload construction (json.dumps vs f-strings).
# The solution script's build_payload() produces valid JSON; its __main__ also calls
# agy run with --payload, but the mock-bin does not recognise --payload and exits 2.
# Therefore: test only the JSON serialization output, not the full agy call.
# Use `python3 -c` to import and call build_payload() directly.

setup() {
  REPO_ROOT="$(git -C "${BATS_TEST_DIRNAME}" rev-parse --show-toplevel)"
  export PATH="${REPO_ROOT}/mock-bin:${PATH}"
  SOLUTION="${REPO_ROOT}/track-atomic/day-08/solution/build_prompt.py"
  STARTER="${REPO_ROOT}/track-atomic/day-08/starter/build_prompt.py"
}

@test "solution: build_payload produces valid JSON with .prompt field" {
  run python3 -c "
import sys, json
sys.path.insert(0, '$(dirname "$SOLUTION")')
from build_prompt import build_payload
result = build_payload('Say \"hello world\"')
data = json.loads(result)
assert 'prompt' in data, 'Missing prompt key'
assert data['prompt'] == 'Say \"hello world\"', 'Prompt value mismatch'
print(result)
"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.prompt'
}

@test "solution: build_payload with quotes in input produces valid JSON (safe escaping)" {
  run python3 -c "
import sys, json
sys.path.insert(0, '$(dirname "$SOLUTION")')
from build_prompt import build_payload
result = build_payload('Say \"hi\" and <tag>')
json.loads(result)  # must not raise
print('VALID')
"
  [ "$status" -eq 0 ]
  [[ "$output" == *"VALID"* ]]
}

@test "starter: raw f-string interpolation produces invalid JSON when input contains quotes" {
  run python3 -c "
import sys, json
sys.path.insert(0, '$(dirname "$STARTER")')
from build_prompt import build_payload
result = build_payload('Say \"hello world\"')
try:
    json.loads(result)
    print('VALID')  # if it somehow parses, that is a false pass
except json.JSONDecodeError:
    print('INVALID')
"
  [ "$status" -eq 0 ]
  [[ "$output" == *"INVALID"* ]]
}

@test "solution: uses json.dumps for safe serialization" {
  grep -q 'json.dumps' "$SOLUTION"
}

@test "starter: uses f-string interpolation (the bug)" {
  grep -q 'return f' "$STARTER"
}
