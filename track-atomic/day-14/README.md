# Day 14 — Environment Isolation & Temporary Sandbox (Bash)

## Concepts

### `mktemp -d` — Isolated Temporary Directories

`mktemp -d` creates a unique, randomly named directory under `/tmp`:

```bash
WORKDIR="$(mktemp -d)"
# e.g. /tmp/tmp.A3fKz9Xp1q
```

Benefits:
- **Collision-free**: the random suffix prevents conflicts between concurrent
  CI runs.
- **Out of tree**: nothing is written into the repository working directory.
- **Standard**: tooling (Docker, Buildkite, GitHub Actions) cleans `/tmp`
  between jobs automatically.

### EXIT Traps for Cleanup

A `trap` registers a command to run when the script exits — regardless of
whether it exits cleanly or because of an error:

```bash
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
```

The trap fires on:
- Normal `exit 0`
- Error-triggered exit from `set -e`
- `SIGINT` / `SIGTERM` (with appropriate signal handling)

Without the trap, failed scripts leave stale `/tmp/tmp.*` directories that
accumulate across CI runs.

### Why Polluting the Repo Root Is Harmful in CI

Creating session files in `./` (the repo checkout directory) causes:

1. **Dirty working tree**: `git status` shows untracked files; PR checks that
   validate a clean tree will fail.
2. **Race conditions**: parallel CI workers writing to the same paths clash.
3. **Leaked secrets**: auth tokens written to `./` may be captured by build
   artifact collectors.

### `--workdir` Flag

The `agy run` command accepts `--workdir <dir>` to write its internal session
files into the specified directory instead of the current working directory.

```bash
agy run --headless --json --workdir "$WORKDIR"
```

## Your Task

1. Open `starter/sandboxed_run.sh` and find where `TMPFILE` is created with a
   `./` prefix (current working directory).
2. Replace the pattern with `mktemp -d`, pass `--workdir` to `agy`, and add an
   `EXIT` trap to delete the sandbox.
3. Confirm the output still contains `.metadata.status == "COMPLETED"`.

## Running the Tests

```bash
bats track-atomic/day-14/test.bats
```
