#!/usr/bin/env python3
"""
track-sprint/module-01/src/mock_executor.py

Mock executor that validates the mock-bin/agy fixture injection
and enforces offline boundaries using socket interception.
"""
import json
import os
import socket
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"


def _block_socket(*args, **kwargs):
    """Raise an error for any attempted socket connection (offline boundary)."""
    raise ConnectionRefusedError("Offline mode: network access is blocked")


def execute_offline(args: list[str], fixture_path: str | None = None) -> dict:
    """
    Execute agy with offline socket blocking and optional fixture override.
    Returns parsed JSON response.
    """
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    env["AGY_OFFLINE_MODE"] = "1"
    if fixture_path:
        env["AGY_FIXTURE_PATH"] = fixture_path

    cmd = ["agy"] + args + ["--headless", "--json"]

    with patch("socket.socket", side_effect=_block_socket):
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd,
            output=result.stdout,
            stderr=result.stderr,
        )
    return json.loads(result.stdout)


if __name__ == "__main__":
    resp = execute_offline(["version"])
    print(json.dumps(resp, indent=2))
