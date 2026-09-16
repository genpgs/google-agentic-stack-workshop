#!/usr/bin/env python3
"""Day 26 Solution: Subprocess wrapper with SIGINT/SIGTERM signal handling."""
import json, os, signal, subprocess, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
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
    _child_proc = subprocess.Popen(["agy", "run", "--headless", "--json"],
                                   capture_output=True, text=True, env=env)
    stdout, stderr = _child_proc.communicate()
    _child_proc = None
    if not stdout.strip():
        raise RuntimeError(f"Empty stdout. stderr: {stderr}")
    return json.loads(stdout)

if __name__ == "__main__":
    resp = run_agy()
    print(json.dumps(resp, indent=2))
