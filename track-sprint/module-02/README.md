# Module 02 — Gemini Spark 24/7 Workspace Assistant Simulator

> **Track:** Sprint | **Module:** 02 | **Difficulty:** Intermediate–Advanced

## Capstone Goal

Implement a **multi-step autonomous agent dispatcher** that uses Gemini Spark prompts, stateful multi-turn history tracking, and headless function calling over local workspace files — all without live API calls or network dependencies.

By the end of this module you will have built:

- A **`SparkPromptBuilder`** that serialises structured multi-role prompt payloads (user / model / tool) for headless `agy` execution.
- A **`TurnManager`** that preserves full conversation history across iterative tool invocations without resetting state.
- **Local workspace tools** (`list_workspace_files`, `read_workspace_file`, `write_workspace_file`) that the agent can call via a central `dispatch_tool` registry.
- An **`AgentDispatcher`** orchestrator that ties all pieces together: it builds prompts, invokes `agy` via `mock-bin/`, routes tool calls, and tracks history.

---

## File Structure

```
track-sprint/module-02/
├── README.md                          ← this file
├── workspace/
│   ├── spark_prompt_builder.py        ← Spark payload builder & validator
│   ├── turn_manager.py                ← Stateful multi-turn history manager
│   ├── agent_dispatcher.py            ← Autonomous dispatcher orchestrator
│   └── tools/
│       └── workspace_tools.py         ← Local workspace tool implementations
└── tests/
    └── test_agent_dispatcher.py       ← Pytest harness (4 test classes)
```

---

## Prerequisites

| Requirement | Detail |
|---|---|
| Python | ≥ 3.10 (uses `list[…] \| None` union syntax) |
| pytest | Installed in the repo `.venv` |
| mock-bin/agy | Offline mock binary at repo root — **no live API needed** |
| Environment | `AGY_OFFLINE_MODE=1` is set automatically by fixtures |

No additional packages beyond the standard library and `pytest` are required.

---

## How to Run the Tests

From the **repository root**:

```bash
pytest track-sprint/module-02/tests/ -v
```

Or target a specific test class:

```bash
pytest track-sprint/module-02/tests/test_agent_dispatcher.py::TestMultiTurnStatePreservation -v
```

---

## The Four Pytest Criteria

Each test class maps to one graded criterion:

### 1. `TestAgentDispatchHeadless`
**`test_agent_dispatch_headless`** — Verifies the agent orchestrates tasks without prompt pauses.

- Calls `agy agent dispatch --headless --json` via subprocess.
- Asserts the response contains `status == "COMPLETED"` and `metadata.headless == True`.
- Confirms both `--headless` and `--json` flags are present in the subprocess invocation.

### 2. `TestToolCallRouting`
**`test_tool_call_routing`** — Confirms tool calls route to local workspace tools without external API requests.

- `list_workspace_files` returns a `files` list directly from the local filesystem.
- `dispatch_tool` routes by name and handles unknown tools with a structured error.
- Tool results are appended to the agent's history with `role == "tool"`.

### 3. `TestMultiTurnStatePreservation`
**`test_multi_turn_state_preservation`** — Asserts history buffer maintains context integrity across turns.

- History accumulates correctly across user → model → tool turns.
- Adding a tool result does **not** reset prior history entries.
- `to_session_payload()` emits valid JSON with `headless: true`.
- `SparkPromptBuilder` preserves the exact role sequence in the built payload.

### 4. `TestAgentTimeoutAndRecovery`
**`test_agent_timeout_and_recovery`** — Validates the agent recovers from mock CLI execution timeouts.

- A near-zero `timeout` triggers `subprocess.TimeoutExpired`.
- A non-zero subprocess exit raises `subprocess.CalledProcessError`.
- The dispatcher can be cleanly reinitialised after an error (history reset + re-dispatch).

---

## Key Design Decisions

### Why `headless=True` everywhere?
The `mock-bin/agy` script will block indefinitely on stdin when invoked without `--headless` (simulating a real interactive session). All dispatch paths must pass `--headless` to prevent test hangs.

### Why local tools instead of API function calling?
The module is designed to run in **fully offline CI environments**. The `TOOL_REGISTRY` in `workspace_tools.py` acts as the function-calling surface; the dispatcher resolves and executes tools locally rather than round-tripping to an external API.

### Path resolution in `workspace_tools.py`
`REPO_ROOT` is resolved as **5 levels above** `workspace_tools.py` (`parents[5]` from `tools/`), which correctly points to the monorepo root. All file paths are validated to stay within `REPO_ROOT` (or a provided `sandbox_root`) to prevent path-traversal.

---

## Running in CI

The test suite is self-contained and requires only:

```bash
export PATH="$(pwd)/mock-bin:$PATH"
export AGY_OFFLINE_MODE=1
pytest track-sprint/module-02/tests/ -v --tb=short
```

Expected exit code: **0** (all tests pass).
