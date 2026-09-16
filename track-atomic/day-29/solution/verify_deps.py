#!/usr/bin/env python3
"""Day 29 Solution: Dependency verifier using only local checks — no network."""
import importlib.metadata
import json
import shutil
import sys

REQUIRED_PYTHON_PACKAGES = ["pytest"]
REQUIRED_BINARIES = ["jq"]

def check_package_local(pkg):
    """Check if a Python package is installed locally via importlib.metadata."""
    try:
        version = importlib.metadata.version(pkg)
        return {"installed": True, "version": version}
    except importlib.metadata.PackageNotFoundError:
        return {"installed": False, "version": None}

def check_binary_local(binary):
    """Check if a binary is in PATH using shutil.which (no network)."""
    path = shutil.which(binary)
    return {"installed": path is not None, "path": path}

if __name__ == "__main__":
    results = {}
    errors = []
    for pkg in REQUIRED_PYTHON_PACKAGES:
        info = check_package_local(pkg)
        results[f"pkg:{pkg}"] = info
        if not info["installed"]:
            errors.append(f"Python package not found: {pkg}")
    for binary in REQUIRED_BINARIES:
        info = check_binary_local(binary)
        results[f"bin:{binary}"] = info
        if not info["installed"]:
            errors.append(f"Binary not in PATH: {binary}")
    all_ok = len(errors) == 0
    print(json.dumps({"results": results, "errors": errors, "all_ok": all_ok}, indent=2))
    if not all_ok:
        sys.exit(1)
