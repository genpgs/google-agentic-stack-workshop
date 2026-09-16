#!/usr/bin/env python3
"""Day 12 Solution: Validates artifact against schema before saving."""
import json
import sys

try:
    import jsonschema
except ImportError:
    print("jsonschema not installed; run: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

SCHEMA = {
    "type": "object",
    "required": ["name", "version", "status", "metadata"],
    "properties": {
        "name": {"type": "string"},
        "version": {"type": "string"},
        "status": {"type": "string"},
        "metadata": {"type": "object"},
    },
}


def validate_and_save(data, path="/tmp/artifact_valid.json"):
    jsonschema.validate(instance=data, schema=SCHEMA)
    with open(path, "w") as f:
        json.dump(data, f)
    print(json.dumps({"saved": path, "status": "VALID"}))


if __name__ == "__main__":
    good_artifact = {
        "name": "spark-output",
        "version": "1.0",
        "status": "COMPLETED",
        "metadata": {"headless": True},
    }
    validate_and_save(good_artifact)
