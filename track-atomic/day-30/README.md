# DAY 30: Full Atomic Track CI Pre-Flight Runner (Bash)

**Bug**: Pre-flight script exits on first non-fatal warning instead of aggregating all BATS results.

**Explain**:
In CI pre-flight runners, executing multiple test suites requires tracking outcomes across all files before failing. When running `bash` with `set -e`, any command that returns a non-zero exit code causes an immediate termination of the script. This behavior breaks aggregation, preventing the script from collecting results from all suites and generating a final JSON summary report.

**Task**:
Fix the runner so that it handles test failures gracefully, aggregates results across all days, and outputs a valid JSON summary before exiting with the appropriate status.

**Instruction**:
Run `bats track-atomic/day-30/test.bats` to ensure your pre-flight runner aggregates test results properly.
