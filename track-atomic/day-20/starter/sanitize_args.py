#!/usr/bin/env python3
"""Day 20 Starter: Argument sanitizer using dangerous shell=True."""
import subprocess, os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"

def run_agy_unsafe(user_prompt):
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    # BUG: shell=True with unsanitized user input — injection risk
    cmd = f'agy run --headless --json --payload "{user_prompt}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    return result.stdout

if __name__ == "__main__":
    output = run_agy_unsafe("hello world")
    print(output)
