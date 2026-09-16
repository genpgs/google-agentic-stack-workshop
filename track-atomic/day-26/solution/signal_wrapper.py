#!/usr/bin/env python3
"""Day 26 Solution: Subprocess wrapper with SIGINT/SIGTERM signal handling."""
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

# signal_wrapper.py is at: solution/ → day-26/ → track-atomic/ → repo-root/
# parents[0] = solution/, parents[1] = day-26/, parents[2] = track-atomic/, parents[3] = repo-root
REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"

_child_proc = None


def _handle_signal(signum, frame):
    global _child_proc
    if _child_proc and _child_proc.poll() is None:
        _child_proc.terminate()
        try:
            _child_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _child_proc.kill()
    sys.exit(128 + signum)


signal.signal(signal.SIGINT, _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)


def run_agy():
    global _child_proc
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    # Use stdout/stderr=PIPE (capture_output is not valid for Popen)
    _child_proc = subprocess.Popen(
        ["agy", "run", "--headless", "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    stdout, stderr = _child_proc.communicate()
    _child_proc = None
    if not stdout.strip():
        raise RuntimeError(f"Empty stdout. stderr: {stderr}")
    return json.loads(stdout)


if __name__ == "__main__":
    resp = run_agy()
    print(json.dumps(resp, indent=2))
