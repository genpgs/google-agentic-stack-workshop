#!/usr/bin/env python3
"""Day 20 Solution: Safe argument handling using list-based subprocess call."""
import json, subprocess, os, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"

def run_agy_safe(user_prompt):
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    payload = json.dumps({"prompt": user_prompt})
    # FIX: list-based args, no shell=True
    cmd = ["agy", "run", "--headless", "--json", "--payload", payload]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    result.check_returncode()
    return json.loads(result.stdout)

if __name__ == "__main__":
    resp = run_agy_safe('hello; echo INJECTED')
    print(json.dumps(resp, indent=2))
