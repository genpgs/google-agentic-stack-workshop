#!/usr/bin/env python3
"""Day 27 Starter: Capability manifest generator with malformed tool declarations."""
import json

def generate_tool(name, params):
    # BUG: parameters missing required 'type' and 'description' fields
    return {
        "functionName": name,
        "parameters": {k: {} for k in params}  # empty dicts, no type/description
    }

if __name__ == "__main__":
    tool = generate_tool("search_files", ["query", "path"])
    print(json.dumps(tool, indent=2))
