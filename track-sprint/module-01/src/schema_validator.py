#!/usr/bin/env python3
"""
track-sprint/module-01/src/schema_validator.py

Validates Antigravity CLI 2.0 JSON output against the expected schema.
No network access is performed; validation is purely local.
"""
import json
import sys

REQUIRED_TOP_KEYS = {"status", "metadata"}
REQUIRED_METADATA_KEYS = {"status", "version", "headless"}


def validate_response(data: dict) -> list[str]:
    """
    Validate a parsed AGY JSON response.
    Returns list of validation error strings (empty if valid).
    """
    errors = []
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            errors.append(f"Missing required top-level key: '{key}'")
    if "metadata" in data:
        meta = data["metadata"]
        if not isinstance(meta, dict):
            errors.append("'metadata' must be a dict")
        else:
            for key in REQUIRED_METADATA_KEYS:
                if key not in meta:
                    errors.append(f"Missing required metadata key: '{key}'")
            if meta.get("headless") is not True:
                errors.append("metadata.headless must be True")
            if meta.get("status") != "COMPLETED":
                errors.append(f"metadata.status must be COMPLETED, got: {meta.get('status')}")
    return errors


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"valid": False, "errors": [f"JSON parse error: {e}"]}))
        sys.exit(1)

    errors = validate_response(data)
    result = {"valid": len(errors) == 0, "errors": errors}
    print(json.dumps(result, indent=2))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
