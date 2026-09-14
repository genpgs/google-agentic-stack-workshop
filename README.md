# Google Agentic Stack Workshop: Antigravity 2.0 & Gemini Spark

[![Grading Runner](https://github.com/google-workshop/agentic-stack/actions/workflows/grading-runner.yml/badge.svg)](.github/workflows/grading-runner.yml)
[![Dev Container](https://img.shields.io/badge/Dev%20Container-Python%203.11-blue?logo=docker)](.devcontainer/devcontainer.json)
[![bats-core](https://img.shields.io/badge/tests-bats--core-yellow?logo=gnubash)](https://github.com/bats-core/bats-core)
[![pytest](https://img.shields.io/badge/tests-pytest-brightgreen?logo=pytest)](https://docs.pytest.org/)
[![Antigravity CLI](https://img.shields.io/badge/agy-v2.0.0--mock-orange)](mock-bin/agy)
[![Model](https://img.shields.io/badge/Model-Gemini%20Spark-purple?logo=google)](https://ai.google.dev)
[![Platform](https://img.shields.io/badge/Platform-Antigravity%202.0-teal)](https://antigravity.google)
[![Offline Mode](https://img.shields.io/badge/Network-Zero%20Egress%20Guaranteed-success)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

An enterprise-grade monorepo curriculum for hands-on mastery of autonomous AI agent development, multi-turn orchestration, and headless CLI scripting powered by **Gemini Spark**, **Antigravity 2.0**, and the **Antigravity CLI (`agy`)**.

Designed for zero-dependency, 100% air-gapped CI/CD execution with an offline mock runtime harness (`mock-bin/agy`).

---

## 🚀 Quick Launch with GitHub Codespaces

Start coding immediately in a fully configured browser-based container. No local installation or API keys required:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new)

> [!TIP]
> Launching via Codespaces automatically builds the `.devcontainer` image with Python 3.11, `bats-core`, `jq`, `pytest`, `pre-commit`, and injects `mock-bin/agy` into your `$PATH`.

---

## 📋 Prerequisites

To run this workshop locally (outside of GitHub Codespaces), ensure your system meets the following prerequisites:

| Requirement | Supported Versions | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.11.x` | Core scripting, pytest suites, schema validators |
| **Bash** | `4.4+` | Shell scripting challenges, pipeline dispatchers |
| **bats-core** | `v1.9+` | Automated assertion runner for shell & CLI suites |
| **jq** | `1.6+` | High-performance headless JSON stream extraction |
| **pre-commit** | `v3.0+` | Git hook automation and code formatting enforcement |
| **Git** | `2.30+` | Monorepo version control and diff validation |
| **Docker / Dev Containers** *(Optional)* | Latest | Local containerized dev environment matching Codespaces |

> [!NOTE]
> **Zero API Quota Consumption**: This workshop does **not** make live calls to external Gemini APIs or Vertex endpoints. All challenges execute against `mock-bin/agy` in complete isolation (`AGY_OFFLINE_MODE=1`).

---

## 🎯 Track Selector

Choose the learning track that best matches your timeline, learning style, and technical focus:

| Feature | ⚡ Track 1: Atomic Challenges (`track-atomic`) | 🏗️ Track 2: Sprint Workshops (`track-sprint`) |
| :--- | :--- | :--- |
| **Format** | 30 daily micro-challenges | 4 comprehensive capstone modules |
| **Pacing** | 15 minutes / challenge | 2 – 4 hours / module |
| **Skill Focus** | Bash & Python CLI debugging, jq parsing, error trapping | Multi-agent systems, prompt engineering, CI autograders |
| **Testing Engine** | `bats-core` (`test.bats`) | `pytest` (`test_*.py`) |
| **Structure** | `README.md`, `starter/`, `solution/`, `test.bats` | `README.md`, `src/`, `config/`, `tests/` |
| **Prerequisites** | Foundational shell scripting & Python basics | Intermediate Python & software architecture |
| **Target Outcome** | Muscle memory in headless CLI automation & sanitization | Production-ready autonomous agent pipeline architectures |

---

## 🧭 Curriculum Overview

### Track 1: 30-Day Atomic Challenges (`track-atomic`)

Every day tackles an intentional starter bug verified through automated `bats` assertions:

| Day | Challenge Title | Skill Focus | Learning Objectives |
| :---: | :--- | :---: | :--- |
| **01** | Antigravity CLI Binary Path & Version Probe | **Bash** | Resolve `mock-bin/agy` via `$PATH` and enforce `--headless` & `--json` |
| **02** | Headless Output Deserialization with jq | **Bash** | Stream-parse JSON payloads and verify `metadata.status == COMPLETED` |
| **03** | Offline Environment Guard & API Key Stubbing | **Bash** | Enforce `AGY_OFFLINE_MODE=1` and block outbound socket requests |
| **04** | Antigravity CLI Config Initialization | **Python** | Dynamically resolve `.devcontainer` and root config schemas |
| **05** | Non-Interactive Session Spawning | **Bash** | Avoid stdin deadlock with `--headless` session token extraction |
| **06** | Mock Binary Fixture Injection | **Python** | Prepend fixtures in subprocess environments using mock CLI payloads |
| **07** | BATS Test Suite Assertion for CLI Exit Codes | **Bash** | Assert exit code `2` on invalid arguments with structured JSON errors |
| **08** | Gemini Spark Prompt Assembly & Escaping | **Python** | Sanitize and assemble multi-line Spark payloads with `--payload` |
| **09** | Headless Agent Dispatcher Script | **Bash** | Non-interactive task categorization with `agy agent dispatch` |
| **10** | Subprocess Error Capture & Logging | **Python** | Capture `stderr` diagnostics without swallowing process exceptions |
| **11** | Deterministic Response Fixture Parser | **Python** | Reconstruct NDJSON streaming tokens from `agy stream --headless` |
| **12** | JSON Schema Validation for Spark Artifacts | **Python** | Offline validation of agent-generated schema artifacts |
| **13** | Batch Job Dispatcher with Bats Runner | **Bash** | Non-fatal batch execution with structured summary reporting |
| **14** | Environment Isolation & Temporary Sandbox | **Bash** | Strict sandbox containment via `mktemp` and `agy --workdir` |
| **15** | Gemini Spark Tool Call Serialization | **Python** | Enforce `camelCase` tool parameters for Antigravity 2.0 schemas |
| **16** | Headless Status Polling Loop | **Bash** | Bounded polling with retry limits and non-interactive status probes |
| **17** | Mock CLI Response Interceptor | **Python** | Regex subcommand routing with dynamic fixture interception |
| **18** | Antigravity Workspace Manifest Generation | **Python** | ISO timestamps and JSON serializable manifest generation |
| **19** | BATS Mock Verification for Network Egress Block | **Bash** | Automated assertion of network boundary enforcement |
| **20** | Antigravity CLI Argument Sanitizer | **Python** | Parameter escaping to mitigate shell command injection |
| **21** | Gemini Spark Multi-Turn Conversation State Reducer | **Python** | Preserve alternating turn history and tool feedback context |
| **22** | Headless Failure Telemetry Formatter | **Bash** | Format system error telemetry strictly as newline-delimited JSON |
| **23** | Mock CLI Fixture Override Mechanism | **Bash** | Dynamic fixture switching via `AGY_FIXTURE_PATH` |
| **24** | Antigravity 2.0 Task Manifest Validator | **Python** | Enforce starter/solution/test directory contract integrity |
| **25** | BATS Execution Timeout & Deadlock Guard | **Bash** | Implement `timeout 10s` guards with exit code `124` diagnostics |
| **26** | Python Subprocess Signal Handling & Termination | **Python** | Trap `SIGINT` & `SIGTERM` to eliminate orphaned CLI processes |
| **27** | Spark Capability Manifest Generator | **Python** | Export typed tool declarations compliant with Antigravity runtime |
| **28** | Structured Diff Assessor for Starter vs Solution | **Bash** | Validate non-zero unified diffs between starter and solution pairs |
| **29** | Offline Dependency Integrity Verifier | **Python** | Verify local environment integrity without remote network lookups |
| **30** | Full Atomic Track CI Pre-Flight Runner | **Bash** | Aggregate 30 daily test suites into a unified machine-readable report |

---

### Track 2: Sprint Workshop Modules (`track-sprint`)

Four end-to-end capstone modules combining multi-file architectures with `pytest`:

```
track-sprint/
├── module-1/  # Headless CLI Foundation & Mock Runtime Harness
├── module-2/  # Gemini Spark Autonomous Agent & Tool Dispatcher
├── module-3/  # Antigravity 2.0 Multi-Agent Pipeline & Artifact Engine
└── module-4/  # Enterprise Autograder & Offline CI/CD Verification Suite
```

#### Module 1: Headless CLI Foundation & Mock Runtime Harness
* **Capstone Goal**: Build a resilient headless wrapper around `mock-bin/agy` featuring deterministic JSON extraction, socket interception, and schema validation.
* **Components**: `cli_harness.py`, `mock_executor.py`, `schema_validator.py`, `agy_headless.json`.
* **Pytest Verification**:
  * `test_cli_headless_invocation`: Validates `--headless` and `--json` invocations return status 0.
  * `test_offline_boundary_enforcement`: Blocks socket egress.
  * `test_mock_binary_fallback`: Validates `AGY_OFFLINE_MODE=1` substitution.
  * `test_json_schema_validation`: Checks compliance with Antigravity 2.0 output schema.

#### Module 2: Gemini Spark Autonomous Agent & Tool Dispatcher
* **Capstone Goal**: Implement a multi-step autonomous agent dispatcher utilizing Gemini Spark prompts, stateful multi-turn history buffers, and headless local workspace tool invocation.
* **Components**: `agent_dispatcher.py`, `spark_prompt_builder.py`, `turn_manager.py`, `workspace_tools.py`.
* **Pytest Verification**:
  * `test_agent_dispatch_headless`: Verifies prompt execution without user intervention.
  * `test_tool_call_routing`: Verifies routing to local tool executors without network calls.
  * `test_multi_turn_state_preservation`: Validates conversation history persistence.
  * `test_agent_timeout_and_recovery`: Asserts graceful recovery from mock timeouts.

#### Module 3: Antigravity 2.0 Multi-Agent Pipeline & Artifact Engine
* **Capstone Goal**: Develop an agentic pipeline engine coordinating specialized Spark generator and critic subagents to generate, evaluate, and patch repository code headlessly.
* **Components**: `pipeline_engine.py`, `subagent_coordinator.py`, `artifact_critic.py`, `diff_patcher.py`.
* **Pytest Verification**:
  * `test_pipeline_multi_agent_flow`: Verifies JSON envelope communication between subagents.
  * `test_artifact_deterministic_output`: Verifies reproducible artifact generation.
  * `test_headless_critic_evaluation`: Ensures automated non-interactive code review.
  * `test_patch_application_safety`: Protects repository files against malformed patches.

#### Module 4: Enterprise Autograder & Offline CI/CD Verification Suite
* **Capstone Goal**: Construct an end-to-end autograding system capable of testing and scoring all 30 atomic challenges and 3 preceding sprint capstones in an air-gapped CI container.
* **Components**: `autograder_core.py`, `bats_runner.py`, `grade_reporter.py`, `sandbox_guard.py`.
* **Pytest Verification**:
  * `test_autograder_batch_evaluation`: Runs 30 atomic test suites and parses results.
  * `test_zero_network_leakage`: Proves execution completes with 100% offline isolation.
  * `test_non_interactive_report_generation`: Validates machine-readable grade reports.
  * `test_sandbox_containment`: Enforces filesystem sandboxing boundaries.

---

## 🛠️ Offline Mock CLI (`mock-bin/agy`)

The repo includes a mock executable at `mock-bin/agy` implementing the Antigravity CLI 2.0 interface:

```bash
# Verify version in JSON format
mock-bin/agy --version --json

# Run authentication in headless mode
mock-bin/agy auth --headless --json

# Execute an agent prompt non-interactively
mock-bin/agy run --payload '{"prompt":"Generate schema"}' --headless --json

# Dispatch a background task
mock-bin/agy task dispatch --task "code-generation" --category "spark" --headless --json
```

### Key Autograder Rules:
1. **Headless Execution**: Always pass `--headless` and `--json`. Commands lacking `--headless` intentionally block or fail in CI to simulate interactive prompts.
2. **Deterministic Errors**: Missing or invalid arguments immediately output structured JSON to `stderr` with exit code `2`:
   ```json
   {
     "code": "INVALID_ARGUMENT",
     "message": "Missing command arguments. Usage: agy <subcommand> [flags]",
     "status": "ERROR"
   }
   ```
3. **Fixture Overrides**: Use `AGY_FIXTURE_PATH=/path/to/fixture.json` or `--fixture /path/to/fixture.json` to mock specific responses dynamically.

---

## 🧪 Running Tests Locally

Run the complete autograding suite locally using `bats` and `pytest`:

```bash
# Add mock-bin to PATH and set offline mode
export PATH="$PWD/mock-bin:$PATH"
export AGY_OFFLINE_MODE="1"

# Run all BATS tests across track-atomic
find track-atomic -name "*.bats" -exec bats {} +

# Run all Pytest suites across track-sprint
pytest track-sprint -v

# Run pre-commit checks
pre-commit run --all-files
```

---

## 📂 Monorepo Structure

```
google-agentic-stack-workshop/
├── .devcontainer/
│   └── devcontainer.json        # Codespaces container config (Python 3.11, bats, jq)
├── .github/
│   └── workflows/
│       └── grading-runner.yml   # Air-gapped CI runner executing bats & pytest
├── mock-bin/
│   └── agy                      # Headless, offline Antigravity CLI 2.0 mock executable
├── track-atomic/                # 30 daily 15-minute challenges
│   └── day-XX/
│       ├── README.md            # Challenge briefing and instructions
│       ├── starter/             # Starter implementation containing bug
│       ├── solution/            # Reference solution
│       └── test.bats            # Automated BATS test specification
├── track-sprint/                # 4 deep-dive workshop capstones
│   └── module-X/
│       ├── README.md            # Architecture spec and capstone guide
│       ├── src/                 # Production agent components
│       ├── config/              # Runtime schemas & configurations
│       └── tests/               # Comprehensive pytest test suite
├── .pre-commit-config.yaml      # Code quality & formatting hooks
├── AGENT_SPEC.md                # System specification & autograder rules
├── curriculum_manifest.json     # Single source of truth for all curriculum tracks
└── README.md                    # Root documentation and track selector
```

---

## 📄 License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
