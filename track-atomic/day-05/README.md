# Day 05 — Non-Interactive Session Spawning

## Concept: Interactive vs. Non-Interactive Mode

CLI tools designed for humans often operate in **interactive mode** by default:
they open a TTY, prompt the user for input, and block until a response is received.
This is great for developer workflows, but catastrophic in automation contexts.

**Non-interactive (headless) mode** tells the CLI to:
- Skip all prompts
- Read configuration exclusively from flags and environment variables
- Return deterministic, machine-readable output (JSON) and exit immediately

### The `--headless` Flag in Antigravity CLI

```
agy session start --headless --json
```

| Flag | Effect |
|------|--------|
| *(absent)* | Opens an interactive session, blocks on stdin — **hangs in CI** |
| `--headless` | Returns immediately with a `session_token` in JSON |
| `--json` | Ensures output is structured JSON (implied by `--headless`) |

---

## Why `--headless` Is Required in CI/CD Pipelines

Continuous integration runners (GitHub Actions, Cloud Build, Jenkins) have **no
attached TTY**. Any process that waits for keyboard input will:

1. Block indefinitely (or until the CI job's timeout kills it).
2. Consume runner resources without doing any work.
3. Report a confusing timeout failure instead of a clear error message.

> **Rule:** Every `agy` invocation inside a script, pipeline, or test harness
> **must** pass `--headless`.

---

## How `agy session start --headless` Works

When called with `--headless --json`, the CLI returns a JSON object like:

```json
{
  "session_id": "mock-session-3003",
  "session_token": "mock-session-token-3003",
  "action": "start",
  "status": "COMPLETED",
  "metadata": {
    "status": "COMPLETED",
    "version": "2.0.0-mock",
    "headless": true
  }
}
```

The `session_token` field is the value downstream steps use to authenticate
subsequent `agy` calls within the same session.

---

## Your Task

The [`starter/run.sh`](starter/run.sh) script is **buggy** — it calls
`agy session start` without `--headless`, causing the mock binary to simulate
a 30-second hang (the same behaviour as the real CLI awaiting stdin).

**Fix it** by adding the `--headless` flag so the command returns immediately
with a valid `session_token`.

### What to change

```diff
-OUTPUT=$(timeout 5 agy session start --json || true)
+OUTPUT=$(agy session start --headless --json)
```

Your fixed version should:
1. Run `agy session start --headless --json`
2. Extract `session_token` from the JSON output using `jq`
3. Print the token and exit `0`

See [`solution/run.sh`](solution/run.sh) for the reference implementation.

---

## Running the Tests

From the **repo root**:

```bash
bats track-atomic/day-05/test.bats
```

Expected output:

```
 ✓ solution: exits 0 and captures a non-empty session_token
 ✓ starter: exits non-zero or session_token is empty (hangs without --headless)

2 tests, 0 failures
```

### Prerequisites

| Tool | Minimum version |
|------|-----------------|
| [bats-core](https://github.com/bats-core/bats-core) | 1.8 |
| `jq` | 1.6 |
| `timeout` (GNU coreutils) | any |
