# Day 12 — JSON Schema Validation for Spark Artifacts (Python)

## Concepts

### The `jsonschema` Library

[`jsonschema`](https://python-jsonschema.readthedocs.io/) is the standard
Python library for validating data structures against a **JSON Schema**
(json-schema.org). Install it with:

```bash
pip install jsonschema
```

The core API is a single call:

```python
import jsonschema
jsonschema.validate(instance=my_data, schema=MY_SCHEMA)
```

If validation passes, `validate()` returns `None`. If it fails, it raises
`jsonschema.ValidationError` with a human-readable message.

### Draft7Validator

The library ships multiple validator classes — one per JSON Schema draft.
`Draft7Validator` is widely compatible and is what `jsonschema.validate()`
defaults to internally. You can use it directly for programmatic error
collection:

```python
validator = jsonschema.Draft7Validator(schema)
errors = list(validator.iter_errors(data))
```

### Why Validate Before Saving?

Writing an invalid artifact to disk — and discovering the problem only when a
downstream consumer reads it — leads to:

- **Silent data corruption**: downstream jobs read bad data without knowing it.
- **Hard-to-debug failures**: errors surface far from the source.
- **CI pipeline breakage**: long build times before the problem is caught.

Validating at the point of creation makes the failure **loud and immediate**.

### Our Artifact Schema

```json
{
  "type": "object",
  "required": ["name", "version", "status", "metadata"],
  "properties": {
    "name":     { "type": "string" },
    "version":  { "type": "string" },
    "status":   { "type": "string" },
    "metadata": { "type": "object" }
  }
}
```

Any artifact missing one of the four required fields will be rejected before
touching the filesystem.

## Your Task

1. Open `starter/validate_artifact.py` and observe that it writes to disk
   without checking the schema.
2. Add a `jsonschema.validate()` call **before** `json.dump()`.
3. Make the script exit non-zero (via an unhandled `ValidationError`) when the
   artifact is invalid.

## Running the Tests

```bash
bats track-atomic/day-12/test.bats
```
