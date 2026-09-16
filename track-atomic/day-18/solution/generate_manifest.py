#!/usr/bin/env python3
"""Day 18 Solution: Manifest generator with custom datetime encoder."""
import json
from datetime import datetime, timezone

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def generate_manifest():
    return {
        "monorepo_version": "2.0.0",
        "timestamp": datetime.now(timezone.utc),
        "status": "COMPLETED",
        "metadata": {"version": "2.0.0-mock"}
    }

if __name__ == "__main__":
    manifest = generate_manifest()
    output = json.dumps(manifest, cls=DateTimeEncoder, indent=2)
    # Validate round-trip
    json.loads(output)
    print(output)
