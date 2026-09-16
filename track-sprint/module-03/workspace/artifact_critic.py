#!/usr/bin/env python3
"""
track-sprint/module-03/src/artifact_critic.py

Evaluates generated code artifacts for quality and structural compliance.
Runs non-interactively and flags intentional anomalies in a JSON report.
"""
import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"

ANOMALY_PATTERNS = [
    (r"shell=True", "SECURITY: shell=True subprocess call detected"),
    (r"print\s*\(", "STYLE: bare print() without logger"),
    (r"TODO|FIXME", "QUALITY: unresolved TODO/FIXME marker"),
]


def critique_artifact(content: str, filename: str) -> dict:
    """Evaluate artifact content and return structured critique report."""
    import re
    anomalies = []
    for pattern, message in ANOMALY_PATTERNS:
        if re.search(pattern, content):
            anomalies.append({"pattern": pattern, "message": message})
    return {
        "filename": filename,
        "anomalies": anomalies,
        "anomaly_count": len(anomalies),
        "status": "FLAGGED" if anomalies else "CLEAN",
    }


def run_headless_critique(artifact_path: str) -> dict:
    """Run critique via agy headlessly, attach local analysis."""
    env = os.environ.copy()
    env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
    result = subprocess.run(
        ["agy", "run", "--headless", "--json", "--payload",
         json.dumps({"task": "critique", "artifact": artifact_path})],
        capture_output=True, text=True, env=env, timeout=30
    )
    if result.returncode != 0:
        return {"error": result.stderr, "status": "FAILED"}
    agy_response = json.loads(result.stdout)
    content = Path(artifact_path).read_text() if Path(artifact_path).exists() else ""
    local_critique = critique_artifact(content, artifact_path)
    return {**agy_response, "local_critique": local_critique}


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else __file__
    print(json.dumps(run_headless_critique(path), indent=2))
