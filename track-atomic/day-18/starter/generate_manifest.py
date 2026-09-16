#!/usr/bin/env python3
"""Day 18 Starter: Manifest generator that fails on datetime objects."""
import json
from datetime import datetime, timezone

def generate_manifest():
    return {
        "monorepo_version": "2.0.0",
        "timestamp": datetime.now(timezone.utc),  # BUG: not JSON-serializable
        "status": "COMPLETED",
    }

if __name__ == "__main__":
    manifest = generate_manifest()
    # BUG: raises TypeError: Object of type datetime is not JSON serializable
    print(json.dumps(manifest))
