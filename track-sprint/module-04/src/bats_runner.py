#!/usr/bin/env python3
"""
track-sprint/module-04/src/bats_runner.py

Bats test suite runner for all track-atomic daily challenges.
Runs each day's test.bats in isolation and aggregates results.
"""
import json
import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"


def run_single_bats(bats_file: Path, timeout: int = 60) -> dict:
    """
    Run a single test.bats file and return structured results.
    Never raises — always returns a result dict.
    """
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    env["AGY_OFFLINE_MODE"] = "1"

    if not shutil.which("bats"):
        return {
            "file": str(bats_file),
            "passed": False,
            "skipped": True,
            "error": "bats not installed",
            "stdout": "", "stderr": "",
        }
    try:
        result = subprocess.run(
            ["bats", str(bats_file)],
            capture_output=True, text=True,
            env=env, timeout=timeout
        )
        return {
            "file": str(bats_file),
            "passed": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "file": str(bats_file),
            "passed": False,
            "error": f"Timeout after {timeout}s",
            "stdout": "", "stderr": "",
        }
    except Exception as e:
        return {
            "file": str(bats_file),
            "passed": False,
            "error": str(e),
            "stdout": "", "stderr": "",
        }


def run_all_atomic_tests(track_root: Path | None = None) -> dict:
    """Run test.bats for all track-atomic/day-* directories."""
    if track_root is None:
        track_root = REPO_ROOT / "track-atomic"

    day_dirs = sorted(track_root.glob("day-*/"))
    results = []
    for day_dir in day_dirs:
        bats_file = day_dir / "test.bats"
        if bats_file.exists():
            r = run_single_bats(bats_file)
            r["day"] = day_dir.name
            results.append(r)

    passed = sum(1 for r in results if r.get("passed"))
    skipped = sum(1 for r in results if r.get("skipped"))
    failed = len(results) - passed - skipped

    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "results": results,
        "status": "COMPLETED" if failed == 0 else "FAILED",
    }


if __name__ == "__main__":
    summary = run_all_atomic_tests()
    print(json.dumps(summary, indent=2))
