# Day 13 — Batch Job Dispatcher with Bats Runner (Bash)

## Concepts

### Bash Loop Exit Code Capture

In bash, the exit code of a command inside a `for` loop is stored in `$?`
immediately after the command runs. However, `set -e` (**errexit**) adds a
catch: if any command returns non-zero, the script exits immediately — even
inside a loop. This interacts with patterns like `|| true` in tricky ways.

```bash
for ITEM in "${ITEMS[@]}"; do
  some_command "$ITEM" || true   # BUG: swallows the exit code
done
```

Using `|| true` silences the error; `$?` is always `0` after the `||` branch
resolves to the right-hand side. The loop continues unconditionally even when
`some_command` fails.

### The `set -e` Gotcha Inside Loops

`set -e` will **not** abort the script for a failing command that is part of a
compound `||` or `&&` expression. This is by POSIX design. The correct pattern
to capture failure and still keep the loop running is:

```bash
some_command "$ITEM" || { FAILED+=("$ITEM"); break; }
```

The `break` stops the loop on first failure (fail-fast). Omitting `break` lets
subsequent iterations run even after recording a failure (soft-accumulate).

### Per-Iteration Exit Codes

Capture the command's output **and** its exit code in one step:

```bash
RESULT=$(some_command) || { FAILED+=("$ITEM"); break; }
```

Here `RESULT` holds stdout only if the command succeeds; on failure the `{}`
block runs instead.

### The `agy batch` Subcommand

```bash
agy batch --task <name> --headless --json
```

Returns a JSON object with `.status == "COMPLETED"` for each successful task.

## Your Task

1. Open `starter/batch_run.sh` and find the `|| true` that swallows errors.
2. Replace it with a pattern that:
   - Captures the JSON result on success.
   - Records the failing task name and **breaks** the loop on first failure.
3. After the loop, check `${#FAILED[@]}` and exit `1` if any task failed.

## Running the Tests

```bash
bats track-atomic/day-13/test.bats
```
