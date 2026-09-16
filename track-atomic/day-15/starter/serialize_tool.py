#!/usr/bin/env python3
"""Day 15 Starter: Tool call serializer using snake_case (wrong)."""
import json


def serialize_tool_call(function_name, parameters):
    # BUG: snake_case keys instead of camelCase
    return json.dumps(
        {
            "function_name": function_name,
            "input_schema": {
                "parameter_type": "STRING",
                "parameter_description": parameters.get("description", ""),
            },
        }
    )


if __name__ == "__main__":
    result = serialize_tool_call("search_files", {"description": "Search workspace files"})
    print(result)
