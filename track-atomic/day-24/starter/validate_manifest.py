#!/usr/bin/env python3
"""Day 24 Starter: Manifest validator that skips autograder block check."""
import json, sys

REQUIRED_KEYS = ["day_number", "title", "skill_focus"]

def validate_day_spec(spec):
    errors = []
    for key in REQUIRED_KEYS:
        if key not in spec:
            errors.append(f"Missing required key: {key}")
    # BUG: does not check for starter, solution, test.bats presence
    return errors

if __name__ == "__main__":
    spec = {"day_number": 1, "title": "Test", "skill_focus": "Bash"}
    # Missing autograder block — should fail but doesn't
    errors = validate_day_spec(spec)
    print(json.dumps({"valid": len(errors) == 0, "errors": errors}))
