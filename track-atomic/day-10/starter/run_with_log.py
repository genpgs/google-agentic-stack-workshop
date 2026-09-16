#!/usr/bin/env python3
"""Day 10 Starter: Subprocess caller that swallows stderr."""
import subprocess, json, os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MOCK_BIN = REPO_ROOT / "mock-bin"

def run_agy(args):
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    try:
        # BUG: stderr not captured, lost on failure
        result = subprocess.run(["agy"] + args, check=True, capture_output=False, text=True, env=env)
    except subprocess.CalledProcessError as e:
        # BUG: stderr not in exception, logs nothing useful
        print(json.dumps({"error": "command failed", "stderr": None}))
        raise

if __name__ == "__main__":
    run_agy(["run", "--fail", "--headless", "--json"])
