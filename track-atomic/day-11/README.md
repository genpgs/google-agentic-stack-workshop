# Day 11 — Deterministic Response Fixture Parser (Python)

## Concepts

### NDJSON — Newline-Delimited JSON

**NDJSON** (also called JSON Lines or `.jsonl`) is a format where each line of a
file or stream is a self-contained, valid JSON object. It is the natural choice
for streaming APIs because partial output is immediately useful — you don't have
to wait for a closing `}` at the end of a multi-megabyte response body.

```
{"chunk":1,"text":"Gemini ","status":"STREAMING"}
{"chunk":2,"text":"Spark ","status":"STREAMING"}
{"chunk":3,"text":"response completed.","status":"COMPLETED"}
```

### How `agy stream --headless --json` Works

When you call `agy stream --headless --json` the CLI writes **one JSON object
per line** to stdout and then exits. Each object carries:

| Field    | Description                              |
|----------|------------------------------------------|
| `chunk`  | Monotonically increasing chunk number    |
| `text`   | Token text emitted in this chunk         |
| `status` | `"STREAMING"` for mid-stream, `"COMPLETED"` on final chunk |

### Why `json.loads(result.stdout)` Fails

`json.loads()` expects **exactly one** JSON value. When `result.stdout` contains
three lines — three separate JSON objects — the parser raises:

```
json.decoder.JSONDecodeError: Extra data: line 2 column 1 (char 42)
```

The entire output is **not** a JSON array; it is three separate objects
separated by newlines.

### The Accumulator Pattern

The fix is simple: split stdout on newlines and parse each line individually,
accumulating the results into a list.

```python
chunks = []
for line in result.stdout.strip().splitlines():
    line = line.strip()
    if line:                         # skip blank lines
        chunks.append(json.loads(line))
```

Once all chunks are collected you can:
- Concatenate the `text` fields to reconstruct the full response.
- Inspect `chunks[-1]["status"]` to confirm the stream finished cleanly.

## Your Task

1. Open `starter/parse_stream.py` and identify the single-line bug.
2. Apply the accumulator pattern so the parser handles all three NDJSON chunks.
3. Ensure `parse_stream()` returns a dict with keys `chunks`, `full_text`, and
   `status`.

## Running the Tests

```bash
bats track-atomic/day-11/test.bats
```

Both tests must pass — the solution parses cleanly, and the starter crashes.
