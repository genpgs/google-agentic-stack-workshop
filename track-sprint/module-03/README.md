# Module 03 — Antigravity 2.0 Multi-Agent Pipeline & Artifact Engine

## Capstone Goal

Build an agentic **pipeline engine** that coordinates multiple specialized Spark subagents
(`generator`, `critic`, `validator`) to generate, critique, and validate structured repository
code artifacts — entirely **headlessly** and **offline**.

---

## File Structure

```
track-sprint/module-03/
├── README.md                        ← This file
├── src/
│   ├── diff_patcher.py              ← Safe unified diff applier
│   ├── artifact_critic.py           ← Headless artifact quality evaluator
│   ├── subagent_coordinator.py      ← JSON-envelope inter-agent router
│   └── pipeline_engine.py          ← Top-level pipeline orchestrator
└── tests/
    └── test_pipeline_engine.py      ← Pytest harness (4 test classes)
```

---

## Prerequisites

| Requirement | Details |
|---|---|
| Python | ≥ 3.11 (uses `list[dict]` PEP 585 generics) |
| pytest | `pip install pytest` or use `.venv` at repo root |
| mock-bin/agy | Already present at repo root — **no live API needed** |
| Offline mode | `AGY_OFFLINE_MODE=1` is set automatically by the test fixture |

---

## How to Run

From the **repository root**:

```bash
pytest track-sprint/module-03/tests/ -v
```

Or target the file directly:

```bash
python3 -m pytest track-sprint/module-03/tests/test_pipeline_engine.py -v
```

---

## The Four Pytest Criteria

### 1 · `TestPipelineMultiAgentFlow`
> **Asserts generator and critic communicate through structured JSON envelopes.**

Verifies `AgentMessage` serialises to and deserialises from JSON correctly, that
`SubagentCoordinator` routes dispatches to known agents (`generator`, `critic`,
`validator`) via `agy agent dispatch --headless --json`, and that unknown agents are
rejected before any subprocess is spawned. The message log is checked to confirm every
send is recorded.

### 2 · `TestArtifactDeterministicOutput`
> **Confirms generated artifacts match expected golden hashes under mock seeds.**

Runs `PipelineEngine.generate_artifact()` twice with the same seed and asserts the
SHA-256 hash is identical. Also checks that a different seed produces a different hash,
that the seed string appears verbatim in the artifact content, and that the hash string
is exactly 64 hex characters (SHA-256).

### 3 · `TestHeadlessCriticEvaluation`
> **Verifies critic evaluation runs non-interactively and flags anomalies.**

Calls `critique_artifact()` directly to confirm `shell=True` is flagged `SECURITY` and
clean subprocess usage is `CLEAN`. Exercises `run_headless_critique()` (which calls
`agy run --headless --json`) and checks the returned dict includes `local_critique` with
a valid `status` key. Also confirms the pipeline's critic stage returns `agy_response`
with `status == "COMPLETED"`.

### 4 · `TestPatchApplicationSafety`
> **Validates diff_patcher rejects malformed patches without corrupting workspace.**

Passes a well-formed unified diff and asserts `applied == True`. Passes a patch with an
unparseable `@@` header and asserts it is rejected with an `error` key. Passes a patch
whose filename escapes the sandbox via `../../` and asserts path-traversal is rejected.
Passes an empty string and asserts it is rejected.

---

## Architecture Overview

```
PipelineEngine
  │
  ├── generate_artifact()  ──►  SubagentCoordinator.send(AgentMessage → "generator")
  │                                       │
  │                               agy agent dispatch --task <t> --category generator
  │                                       │
  │                              deterministic content hash (SHA-256)
  │
  ├── critique_artifact_pipeline()  ──►  critique_artifact() [local pattern scan]
  │                                   ──►  SubagentCoordinator.send(→ "critic")
  │
  └── validate_and_patch()  ──►  apply_patch() [sandbox-safe diff applier]
                              ──►  SubagentCoordinator.send(→ "validator")
```

All inter-agent communication uses **structured JSON envelopes** (`AgentMessage`).
No plain-text interchange. No live network calls. `mock-bin/agy` handles all
`subprocess` invocations offline.

---

## Key Design Decisions

- **`set -euo pipefail` equivalent**: Python modules use `subprocess.run(...,
  capture_output=True)` with explicit `returncode` checks — no silent failures.
- **Path traversal guard**: `diff_patcher.apply_patch()` resolves both the sandbox root
  and target path with `Path.resolve()` and checks prefix membership before any write.
- **Determinism**: `PipelineEngine` constructs artifact content from `seed + task +
  template` without any timestamp or random component, making SHA-256 hashes stable
  across runs.
- **Offline-first**: `AGY_OFFLINE_MODE=1` is set in `SubagentCoordinator.__init__()` and
  reinforced by the `set_offline_env` autouse fixture so no test can accidentally reach
  a live endpoint.
