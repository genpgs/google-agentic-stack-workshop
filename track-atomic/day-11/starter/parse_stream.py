#!/usr/bin/env python3
"""Day 11 Starter: Buggy single-chunk parser that crashes on NDJSON stream."""
import json
import subprocess
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MOCK_BIN = REPO_ROOT / "mock-bin"


def parse_response():
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    result = subprocess.run(
        ["agy", "stream", "--headless", "--json"],
        capture_output=True,
        text=True,
        env=env,
    )
    # BUG: treats entire stdout as single JSON object — fails on NDJSON
    return json.loads(result.stdout)


if __name__ == "__main__":
    data = parse_response()
    print(data)
