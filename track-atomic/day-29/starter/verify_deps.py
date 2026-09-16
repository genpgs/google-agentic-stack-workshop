#!/usr/bin/env python3
"""Day 29 Starter: Dependency verifier that makes remote pip index requests."""
import subprocess, json, sys

REQUIRED_PYTHON_PACKAGES = ["jq", "pytest"]
REQUIRED_BINARIES = ["bats", "jq"]

def check_package(pkg):
    # BUG: queries PyPI remote index instead of local cache
    result = subprocess.run(["pip", "index", "versions", pkg],
                            capture_output=True, text=True)
    return result.returncode == 0

def check_binary(binary):
    result = subprocess.run(["which", binary], capture_output=True, text=True)
    return result.returncode == 0

if __name__ == "__main__":
    results = {}
    for pkg in REQUIRED_PYTHON_PACKAGES:
        results[f"pkg:{pkg}"] = check_package(pkg)
    for binary in REQUIRED_BINARIES:
        results[f"bin:{binary}"] = check_binary(binary)
    print(json.dumps({"results": results, "all_ok": all(results.values())}))
