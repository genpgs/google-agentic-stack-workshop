#!/usr/bin/env python3
"""Day 12 Starter: Saves artifacts without schema validation."""
import json

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


def save_artifact(data, path="/tmp/artifact.json"):
    # BUG: writes directly without validation
    with open(path, "w") as f:
        json.dump(data, f)
    print(f"Saved to {path}")


if __name__ == "__main__":
    bad_artifact = {"name": "test"}  # missing required fields
    save_artifact(bad_artifact)
