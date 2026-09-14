# Day 03 — Offline Environment Guard & API Key Stubbing

## Concept

### Why Offline Mode is Critical for CI/CD Pipelines

In CI/CD environments, scripts run without human supervision and without guaranteed network
access. Any script that reaches out to a live API endpoint during automated testing risks:

- **Flaky pipelines** — transient network failures cause false test negatives.
- **Cost overruns** — unguarded scripts can exhaust API quota or rack up billing charges.
- **Secret leakage** — CI systems may not have `GEMINI_API_KEY` set, causing fallback
  logic to make unauthenticated or misdirected requests.
- **Non-determinism** — live API responses vary; tests must be reproducible.

The solution is to enforce `AGY_OFFLINE_MODE=1` unconditionally before invoking the CLI.

---

### How `AGY_OFFLINE_MODE=1` Works

The `mock-bin/agy` binary respects the `AGY_OFFLINE_MODE` environment variable. When this
variable is set to `1`, the CLI skips all live network activity and returns deterministic
mock responses suitable for automated testing.

Setting it in two ways is considered best practice:

```bash
export AGY_OFFLINE_MODE=1            # exported into shell environment
OUTPUT=$(AGY_OFFLINE_MODE=1 agy run --headless --json)   # inline on the command
```

The inline form guarantees the variable is present even if `export` was somehow skipped.

---

### The Bug in the Starter

The starter script (`starter/run.sh`) contains two bugs:

1. **It checks a live remote endpoint** when `GEMINI_API_KEY` is not defined:
   ```bash
   if [ -z "${GEMINI_API_KEY:-}" ]; then
     curl -sf https://api.gemini.example.com/health || echo "Network check failed"
   fi
   ```
   In an offline or network-restricted environment, `curl` will fail or hang, breaking
   the pipeline.

2. **It never sets `AGY_OFFLINE_MODE=1`**, so `agy` may attempt live calls.

---

### Your Task

Fix `starter/run.sh` so that it:

1. **Never calls `curl`** or any live network endpoint.
2. **Always exports `AGY_OFFLINE_MODE=1`** before invoking `agy`.
3. **Passes `AGY_OFFLINE_MODE=1` inline** to the `agy run` invocation.
4. **Prepends `mock-bin/` to `PATH`** using `REPO_ROOT` derived from `git rev-parse`.
5. Extracts `.metadata.status` from the JSON output via `jq` and prints it.

The expected output is `COMPLETED`.

---

### How `mock-bin/agy` Respects This Variable

The mock binary at `mock-bin/agy` is a Python script that serves deterministic JSON
responses for all subcommands (`run`, `auth`, `task`, `session`, etc.). When invoked with
`--headless --json`, it always returns a JSON object containing:

```json
{
  "metadata": {
    "status": "COMPLETED"
  }
}
```

No live API key or network is required. The binary is designed to be used in tests by
prepending `mock-bin/` to `PATH`.

---

## Running the Tests

```bash
# From the repo root:
bats track-atomic/day-03/test.bats
```

Ensure `bats` is installed (`apt install bats` or `brew install bats-core`).

The test suite verifies:
- **Solution**: exits 0 and produces `COMPLETED` output with no live network calls.
- **Starter**: exits non-zero when `GEMINI_API_KEY` is unset (curl fails in offline env).
