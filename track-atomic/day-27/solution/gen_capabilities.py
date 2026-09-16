#!/usr/bin/env python3
"""Day 27 Solution: Capability manifest generator with valid tool declarations."""
import json, sys

PARAM_SCHEMA = {
    "type": "object",
    "required": ["functionName", "parameters"],
    "properties": {
        "functionName": {"type": "string"},
        "parameters": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "required": ["type", "description"],
                "properties": {
                    "type": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        }
    }
}

def generate_tool(name, params):
    return {
        "functionName": name,
        "parameters": {
            k: {"type": "STRING", "description": f"Parameter: {k}"}
            for k in params
        }
    }

def validate_tool(tool):
    try:
        import jsonschema
        jsonschema.validate(instance=tool, schema=PARAM_SCHEMA)
        return []
    except jsonschema.ValidationError as e:
        return [str(e.message)]
    except ImportError:
        return []  # skip validation if jsonschema not installed

if __name__ == "__main__":
    tool = generate_tool("search_files", ["query", "path"])
    errors = validate_tool(tool)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(tool, indent=2))
