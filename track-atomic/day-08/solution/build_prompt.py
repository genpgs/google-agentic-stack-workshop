#!/usr/bin/env python3
"""Day 08 Solution: Safe prompt builder using json.dumps for escaping."""
import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"
ROLE_TAG = '<spark:role name="assistant">'
USER_INPUT = 'Say "hello world"'

def build_payload(user_input):
    data = {"prompt": user_input, "role": ROLE_TAG}
    return json.dumps(data)

def run_with_payload(payload):
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    result = subprocess.run(
        ["agy", "run", "--headless", "--json", "--payload", payload],
        capture_output=True, text=True, env=env
    )
    result.check_returncode()
    return json.loads(result.stdout)

if __name__ == "__main__":
    payload = build_payload(USER_INPUT)
    json.loads(payload)  # validate
    resp = run_with_payload(payload)
    print(json.dumps(resp, indent=2))
