#!/usr/bin/env python3
"""
track-sprint/module-01/src/cli_harness.py

Headless CLI harness for Antigravity CLI (mock-bin/agy).
Wraps subprocess invocation with deterministic JSON output,
error capture, and offline-only enforcement.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"


def build_env() -> dict:
    """Build subprocess environment with mock-bin prepended to PATH."""
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    env["AGY_OFFLINE_MODE"] = "1"
    return env


def run_agy(args: list[str], timeout: int = 30) -> dict:
    """
    Run agy CLI with --headless --json flags enforced.
    Returns parsed JSON response dict.
    Raises subprocess.CalledProcessError on non-zero exit.
    """
    cmd = ["agy"] + args + ["--headless", "--json"]
    env = build_env()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd,
            output=result.stdout,
            stderr=result.stderr
        )
    return json.loads(result.stdout)


def main():
    """CLI entry point for manual testing."""
    args = sys.argv[1:] if len(sys.argv) > 1 else ["version"]
    try:
        response = run_agy(args)
        print(json.dumps(response, indent=2))
    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": str(e), "stderr": e.stderr}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
