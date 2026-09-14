# Day 01 — Antigravity CLI Binary Path & Version Probe

## Concepts

### How Bash PATH Resolution Works

When you type a command like `agy`, bash searches every directory listed in the
`PATH` environment variable **left-to-right** and executes the first matching
executable it finds.  If `mock-bin/` is not in `PATH`, bash may pick up a
system-installed `agy` (if one exists), or fail with `command not found`.

The correct pattern for workshop scripts is to **prepend** the repo-local
`mock-bin/` directory so it is always found first:

```bash
REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
export PATH="${REPO_ROOT}/mock-bin:${PATH}"
```

`dirname "${BASH_SOURCE[0]}"` gives the directory of the currently executing
script, and `git rev-parse --show-toplevel` walks up the tree to the repo root —
so the path resolution works regardless of where you `cd` before calling the
script.

### Why `--headless` and `--json` Matter for CI

| Mode | Behaviour |
|---|---|
| Interactive (default) | May block waiting for stdin, emits human-readable text |
| `--headless` | Never blocks; guaranteed non-interactive execution |
| `--json` | All output is strict JSON — machine-parseable, no ANSI codes |

In CI pipelines (GitHub Actions, Cloud Build, etc.) there is **no terminal and
no human** to provide input.  A script that starts an interactive prompt will
hang the pipeline forever.  Always pass `--headless --json` so that:

1. The process exits promptly.
2. Output can be parsed with `jq` without stripping escape sequences.
3. Exit codes are deterministic (`0` = success, non-zero = error).

---

## Your Task

The `starter/run.sh` script has **two bugs**:

1. `mock-bin/` is not on `PATH`, so `agy` resolves to the wrong binary (or fails).
2. `agy version` is called without `--headless --json`, so the output is
   human-readable text instead of JSON.

**Fix both bugs** so that:

- `REPO_ROOT/mock-bin` is prepended to `PATH`.
- The command becomes `agy version --headless --json`.
- The script exits `0` and prints valid JSON where `metadata.status` equals
  `"COMPLETED"`.

Open `starter/run.sh`, apply the fix, then verify with the test suite.

---

## Expected Output

```json
{
  "version": "2.0.0-mock",
  "cli": "antigravity",
  "runtime": "Antigravity 2.0",
  "status": "COMPLETED",
  "metadata": {
    "status": "COMPLETED",
    "version": "2.0.0-mock",
    "headless": true
  }
}
```

`metadata.status` **must** equal `"COMPLETED"` for the test to pass.

---

## Running the Tests

```bash
bats track-atomic/day-01/test.bats
```

> [!TIP]
> Run from the **repo root** so that relative paths resolve correctly.

---

## File Layout

```
track-atomic/day-01/
├── README.md          ← you are here
├── starter/
│   └── run.sh         ← buggy script — edit this to complete the exercise
├── solution/
│   └── run.sh         ← reference solution (do not peek until you've tried!)
└── test.bats          ← automated grader
```
