#!/usr/bin/env python3
"""Day 04 Starter: Buggy config loader using relative paths."""
# BUG: Uses relative path which breaks when run from different directories
import json
import subprocess

CONFIG_PATH = "agy.config.json"  # BUG: relative path


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def main():
    config = load_config()
    print(f"headless_default: {config.get('headless_default')}")


if __name__ == "__main__":
    main()
