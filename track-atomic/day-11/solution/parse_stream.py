#!/usr/bin/env python3
"""Day 11 Solution: NDJSON streaming parser that accumulates all chunks."""
import json
import subprocess
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"


def parse_stream():
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    result = subprocess.run(
        ["agy", "stream", "--headless", "--json"],
        capture_output=True,
        text=True,
        env=env,
    )
    result.check_returncode()
    chunks = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line:
            chunks.append(json.loads(line))
    full_text = "".join(c.get("text", "") for c in chunks)
    return {
        "chunks": len(chunks),
        "full_text": full_text,
        "status": chunks[-1]["status"] if chunks else "UNKNOWN",
    }


if __name__ == "__main__":
    result = parse_stream()
    print(json.dumps(result, indent=2))
