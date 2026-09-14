# Day 02 — Headless Output Deserialization with jq

## Concepts

### Multiline JSON Streaming from `agy`

`agy run --headless --json` emits its result as a single pretty-printed JSON
object (potentially spanning many lines).  Naive tools like `grep` and `head`
are **line-oriented** and will match the first line containing the key — which
may be an inner object, the wrong field, or a different chunk entirely in a
streaming context.  A fragile `grep | head | cut` pipeline will:

- Return the wrong value if the JSON structure changes.
- Silently produce an empty string when the key is nested.
- Never signal an error, so failures go undetected.

The correct approach is to pipe the full output through `jq`:

```bash
STATUS=$(agy run --headless --json | jq --exit-status '.metadata.status')
```

### The `--exit-status` / `-e` Flag in `jq`

By default `jq` exits `0` even when the selected value is `null` or `false`.
The `--exit-status` flag changes this:

| Output value | Exit code without `-e` | Exit code with `-e` |
|---|---|---|
| Any truthy value | `0` | `0` |
| `null` | `0` | `1` |
| `false` | `0` | `1` |

Using `--exit-status` turns missing or falsy values into **detectable failures**,
which is essential for CI pipelines that rely on exit codes to gate deployments.

### Why `--headless` and `--json` Are Still Required

As established in Day 01, `--headless` prevents the process from blocking on
stdin, and `--json` ensures the output is machine-parseable.  Both flags must be
present **before** piping to `jq`; otherwise there is no JSON for `jq` to read.

---

## Your Task

The `starter/run.sh` script has **two bugs**:

1. `mock-bin/` is not on `PATH` (inherited from Day 01).
2. JSON parsing uses `grep | head | cut` instead of `jq --exit-status`, so:
   - The extracted value may be wrong or empty.
   - A missing / null field will not cause a non-zero exit.

**Fix both bugs** so that:

- `REPO_ROOT/mock-bin` is prepended to `PATH`.
- The command pipeline becomes  
  `agy run --headless --json | jq --exit-status '.metadata.status'`
- The script exits `0` and prints `"COMPLETED"` (quoted, as `jq` renders strings).

---

## Expected Output

```
"COMPLETED"
```

> [!NOTE]
> `jq` outputs JSON-encoded strings including the surrounding double-quotes.
> The test checks for the literal value `"COMPLETED"` (with quotes).

---

## Running the Tests

```bash
bats track-atomic/day-02/test.bats
```

> [!TIP]
> Run from the **repo root** so that relative paths resolve correctly.

---

## File Layout

```
track-atomic/day-02/
├── README.md          ← you are here
├── starter/
│   └── run.sh         ← buggy script — edit this to complete the exercise
├── solution/
│   └── run.sh         ← reference solution (do not peek until you've tried!)
└── test.bats          ← automated grader
```
