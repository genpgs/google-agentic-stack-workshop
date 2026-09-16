#!/usr/bin/env python3
"""Day 06 Starter: Buggy subprocess wrapper calling global agy."""
import json
import subprocess

# BUG: calls global 'agy' without injecting mock-bin into PATH
def run_agy(args):
    result = subprocess.run(
        ["agy"] + args + ["--headless", "--json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

if __name__ == "__main__":
    resp = run_agy(["version"])
    print(json.dumps(resp))
