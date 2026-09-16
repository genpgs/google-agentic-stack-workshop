#!/usr/bin/env python3
"""Day 04 Solution: Config loader using absolute paths."""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # goes up to repo root
CONFIG_PATH = REPO_ROOT / "track-atomic" / "day-04" / "solution" / "agy.config.json"


def load_config():
    if not CONFIG_PATH.exists():
        sys.exit(f"Config not found: {CONFIG_PATH}")
    with open(CONFIG_PATH) as f:
        return json.load(f)


def main():
    config = load_config()
    assert config.get("headless_default") is True, "headless_default must be True"
    print(json.dumps({"headless_default": config["headless_default"], "status": "VALID"}))


if __name__ == "__main__":
    main()
