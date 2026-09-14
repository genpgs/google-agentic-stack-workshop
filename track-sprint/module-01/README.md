# Sprint Module 01 — Headless CLI Foundation & Mock Runtime Harness

## Capstone Goal

Build a **resilient, headless execution harness** that wraps the Antigravity CLI
(`mock-bin/agy`) with:

- Deterministic JSON output via enforced `--headless --json` flags
- Error interceptors using `subprocess.CalledProcessError`
- Offline-only enforcement through socket interception (`unittest.mock.patch`)
- Complete offline test coverage via `pytest` — **zero live network calls**

By the end of this module you will have a production-grade Python harness that
can be dropped into any CI/CD pipeline without modification.

---

## File Structure

```
track-sprint/module-01/
├── README.md                   ← this file
├── config/
│   └── agy_headless.json       ← harness configuration (flags, schema version, timeouts)
├── src/
│   ├── cli_harness.py          ← primary harness: run_agy() + build_env()
│   ├── mock_executor.py        ← offline executor with socket blocking
│   └── schema_validator.py     ← AGY CLI 2.0 JSON schema validator
└── tests/
    └── test_harness.py         ← pytest suite (4 test classes, 11 test cases)
```

### Source Modules

| File | Purpose |
|------|---------|
| [`cli_harness.py`](src/cli_harness.py) | `run_agy(args)` — always appends `--headless --json`, returns parsed `dict` |
| [`mock_executor.py`](src/mock_executor.py) | `execute_offline(args)` — patches `socket.socket` to block network I/O |
| [`schema_validator.py`](src/schema_validator.py) | `validate_response(data)` — returns list of schema error strings |

### Configuration

[`config/agy_headless.json`](config/agy_headless.json) declares the canonical
harness contract consumed by CI tooling:

```json
{
  "headless_default": true,
  "offline_mode": true,
  "required_flags": ["--headless", "--json"],
  "timeout_seconds": 30,
  "schema_version": "2.0",
  "required_output_keys": ["status", "metadata"],
  "required_metadata_keys": ["status", "version", "headless"]
}
```

---

## Running the Tests

From the **repo root**:

```bash
pytest track-sprint/module-01/tests/ -v
```

Expected output:

```
track-sprint/module-01/tests/test_harness.py::TestCliHeadlessInvocation::test_version_headless_json_exit_zero PASSED
track-sprint/module-01/tests/test_harness.py::TestCliHeadlessInvocation::test_run_agy_enforces_headless_json PASSED
track-sprint/module-01/tests/test_harness.py::TestCliHeadlessInvocation::test_exit_code_zero_on_valid_subcommand PASSED
track-sprint/module-01/tests/test_harness.py::TestOfflineBoundaryEnforcement::test_socket_block_raises_connection_refused PASSED
track-sprint/module-01/tests/test_harness.py::TestOfflineBoundaryEnforcement::test_execute_offline_does_not_open_sockets PASSED
track-sprint/module-01/tests/test_harness.py::TestOfflineBoundaryEnforcement::test_agY_offline_mode_env_is_set PASSED
track-sprint/module-01/tests/test_harness.py::TestMockBinaryFallback::test_mock_bin_exists_and_is_executable PASSED
track-sprint/module-01/tests/test_harness.py::TestMockBinaryFallback::test_fixture_override_serves_custom_json PASSED
track-sprint/module-01/tests/test_harness.py::TestMockBinaryFallback::test_mock_binary_path_on_env PASSED
track-sprint/module-01/tests/test_harness.py::TestJsonSchemaValidation::test_version_response_passes_schema PASSED
track-sprint/module-01/tests/test_harness.py::TestJsonSchemaValidation::test_run_response_passes_schema PASSED
track-sprint/module-01/tests/test_harness.py::TestJsonSchemaValidation::test_missing_status_fails_validation PASSED
track-sprint/module-01/tests/test_harness.py::TestJsonSchemaValidation::test_non_headless_metadata_fails_validation PASSED

13 passed in X.XXs
```

---

## The Four Test Criteria

### 1. `TestCliHeadlessInvocation` — Headless invocation with exit 0

Verifies that `agy` is always invoked with `--headless` and `--json`, and that
every valid subcommand returns exit code `0` with a parseable JSON body.

> **Key assertion:** `metadata.headless == True` and `metadata.status == "COMPLETED"`

### 2. `TestOfflineBoundaryEnforcement` — Socket interception

Validates that the harness enforces offline operation by patching
`socket.socket` to raise `ConnectionRefusedError`. The mock binary must never
require real network access.

> **Key assertion:** `_block_socket()` raises `ConnectionRefusedError("Offline mode: …")`

### 3. `TestMockBinaryFallback` — Mock binary and fixture injection

Confirms that `mock-bin/agy` exists, is executable, and honours the
`AGY_FIXTURE_PATH` environment variable to serve custom JSON fixtures —
enabling deterministic response injection for edge-case testing.

> **Key assertion:** `PATH` starts with `mock-bin/`; fixture file is served verbatim

### 4. `TestJsonSchemaValidation` — AGY CLI 2.0 schema compliance

Runs every response through `validate_response()` to assert the presence of
`status`, `metadata`, `metadata.headless == true`, and
`metadata.status == "COMPLETED"`. Also verifies that malformed responses are
correctly rejected.

> **Key assertion:** `validate_response(response) == []` for all valid commands

---

## Prerequisites

| Tool | Minimum Version | Install |
|------|----------------|---------|
| Python | 3.11 | `apt install python3.11` / `pyenv install 3.11` |
| pytest | 7.x | `pip install pytest` |
| jq | 1.6 | `apt install jq` |
| bats-core | 1.8 | `apt install bats` or [from source](https://github.com/bats-core/bats-core) |
| GNU coreutils (`timeout`) | any | pre-installed on Linux |

> [!NOTE]
> All tests are **fully offline** — no API keys, credentials, or network access
> are required. The `mock-bin/agy` binary at the repo root provides all
> simulated responses.

> [!TIP]
> Run with `-v --tb=short` for concise failure output during development:
> ```bash
> pytest track-sprint/module-01/tests/ -v --tb=short
> ```
