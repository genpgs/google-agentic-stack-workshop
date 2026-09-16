#!/usr/bin/env python3
"""Day 26 Starter: Subprocess wrapper without signal handling — orphans processes."""
import subprocess, os, json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"

def run_agy():
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    # BUG: no signal handlers — SIGTERM leaves child running
    proc = subprocess.Popen(["agy", "run", "--headless", "--json"],
                            capture_output=True, text=True, env=env)
    stdout, stderr = proc.communicate()
    return json.loads(stdout)

if __name__ == "__main__":
    resp = run_agy()
    print(json.dumps(resp, indent=2))
