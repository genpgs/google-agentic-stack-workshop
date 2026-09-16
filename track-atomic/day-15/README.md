# Day 15 — Gemini Spark Tool Call Serialization (Python)

## Concepts

### camelCase vs snake_case API Contracts

Python idiom uses `snake_case` for variable and function names. REST/JSON APIs —
especially those generated from Protocol Buffers — typically use `camelCase`.
When a Python program serializes a dict to JSON, it outputs whatever key strings
you supply; there is no automatic conversion.

```python
# Python variable (snake_case) — correct for Python code
function_name = "search_files"

# JSON key (camelCase) — required by the Antigravity 2.0 API
{"functionName": "search_files"}
```

Sending `function_name` instead of `functionName` causes a **silent API
error**: the server ignores unknown keys and treats the required field as
missing.

### Antigravity 2.0 Tool Call Schema

The Antigravity 2.0 runtime expects tool call payloads in this shape:

```json
{
  "functionName": "<string>",
  "inputSchema": {
    "parameterType": "STRING",
    "parameterDescription": "<string>"
  }
}
```

| Wrong (snake_case)       | Correct (camelCase)        |
|--------------------------|----------------------------|
| `function_name`          | `functionName`             |
| `input_schema`           | `inputSchema`              |
| `parameter_type`         | `parameterType`            |
| `parameter_description`  | `parameterDescription`     |

### JSON Round-Trip Invariance

A serializer is correct if parsing its output and re-serializing produces the
identical object:

```python
def round_trip_check(serialized):
    data = json.loads(serialized)
    return json.loads(json.dumps(data)) == data
```

This catches encoding bugs (e.g., double-escaping) independently of key naming.

### Conversion Strategy

The simplest fix is to use the correct camelCase strings as dict keys directly
in the `json.dumps()` call. For large codebases a utility function is cleaner:

```python
import re

def to_camel(s):
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])
```

## Your Task

1. Open `starter/serialize_tool.py` and identify the four snake_case dict keys.
2. Rename them to their camelCase equivalents.
3. Optionally add the `round_trip_check` guard from the solution to protect
   against future regressions.

## Running the Tests

```bash
bats track-atomic/day-15/test.bats
```
