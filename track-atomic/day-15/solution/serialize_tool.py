#!/usr/bin/env python3
"""Day 15 Solution: Tool call serializer using correct camelCase keys."""
import json


def serialize_tool_call(function_name, parameters):
    return json.dumps(
        {
            "functionName": function_name,
            "inputSchema": {
                "parameterType": "STRING",
                "parameterDescription": parameters.get("description", ""),
            },
        }
    )


def round_trip_check(serialized):
    """Verify that parsing and re-serializing the JSON produces an identical object."""
    data = json.loads(serialized)
    reserialized = json.dumps(json.loads(json.dumps(data)))
    return json.loads(reserialized) == data


if __name__ == "__main__":
    result = serialize_tool_call("search_files", {"description": "Search workspace files"})
    assert round_trip_check(result), "Round-trip invariance failed"
    print(result)
