# Module 04 — End-to-End Autonomous Software Factory

## Capstone Goal
Construct an end-to-end autograding system capable of testing and validating all 30 atomic daily challenges and 3 preceding sprint capstones in an offline, air-gapped CI container.

## File Structure
- `workspace/autograder_core.py`: Core orchestrator.
- `workspace/bats_runner.py`: Bats test runner for atomic days.
- `workspace/grade_reporter.py`: Generates the JSON grade report.
- `workspace/sandbox_guard.py`: Isolates test execution in a sandbox.
- `tests/test_autograder_core.py`: Pytest test suite for validating all criteria.

## How to Run
```bash
pytest track-sprint/module-04/tests/ -v
```

## The Four Pytest Criteria
1. **test_autograder_batch_evaluation**: Verifies autograder runs all 30 atomic test.bats and parses structured results.
2. **test_zero_network_leakage**: Confirms pytest suite executes strictly offline with all egress blocked.
3. **test_non_interactive_report_generation**: Validates grade_reporter outputs valid machine-readable JSON.
4. **test_sandbox_containment**: Asserts tested code cannot modify files outside designated sandbox.

## Prerequisites
- Python 3.10+
- `pytest`
- `bats-core`
- The `mock-bin/agy` wrapper must be present in the repository root.
