#!/usr/bin/env python3
"""Day 06 Solution: Subprocess wrapper with mock-bin injected into PATH."""
import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MOCK_BIN = REPO_ROOT / "mock-bin"

def run_agy(args):
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    env["AGY_OFFLINE_MODE"] = "1"
    result = subprocess.run(
        ["agy"] + args + ["--headless", "--json"],
        capture_output=True, text=True, env=env
    )
    result.check_returncode()
    return json.loads(result.stdout)

if __name__ == "__main__":
    resp = run_agy(["version"])
    print(json.dumps(resp, indent=2))
