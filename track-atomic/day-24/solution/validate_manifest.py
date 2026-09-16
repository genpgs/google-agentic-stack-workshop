#!/usr/bin/env python3
"""Day 24 Solution: Manifest validator that requires autograder block."""
import json, sys
from pathlib import Path

REQUIRED_KEYS = ["day_number", "title", "skill_focus"]
REQUIRED_AUTOGRADER = ["starter", "solution", "test_bats"]

def validate_day_spec(spec, repo_root=None):
    errors = []
    for key in REQUIRED_KEYS:
        if key not in spec:
            errors.append(f"Missing required key: {key}")
    for ag_key in REQUIRED_AUTOGRADER:
        if ag_key not in spec.get("autograder", {}):
            errors.append(f"Missing autograder key: {ag_key}")
    if repo_root and "day_number" in spec:
        day = f"day-{spec['day_number']:02d}"
        day_dir = Path(repo_root) / "track-atomic" / day
        for item in ["starter", "solution", "test.bats"]:
            if not (day_dir / item).exists():
                errors.append(f"Missing filesystem artifact: {day}/{item}")
    return errors

if __name__ == "__main__":
    spec_bad = {"day_number": 1, "title": "Test", "skill_focus": "Bash"}
    errors = validate_day_spec(spec_bad)
    print(json.dumps({"valid": len(errors) == 0, "errors": errors}))
    assert len(errors) > 0, "Should have caught missing autograder"
    print("Validation correctly rejected missing autograder block.", file=sys.stderr)
    sys.exit(0)
