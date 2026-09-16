#!/usr/bin/env python3
"""Day 10 Solution: Subprocess caller with proper stderr capture and JSON logging."""
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"

def run_agy(args):
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    try:
        result = subprocess.run(
            ["agy"] + args,
            check=True, capture_output=True, text=True, env=env
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        log_entry = {
            "level": "ERROR",
            "event": "agy_subprocess_failed",
            "returncode": e.returncode,
            "stderr": e.stderr.strip() if e.stderr else "",
        }
        print(json.dumps(log_entry), file=sys.stderr)
        raise

if __name__ == "__main__":
    try:
        run_agy(["run", "--fail", "--headless", "--json"])
    except subprocess.CalledProcessError:
        sys.exit(1)
