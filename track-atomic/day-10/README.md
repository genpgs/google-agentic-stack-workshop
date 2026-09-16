# Day 10: Subprocess Error Capture & Logging

When standard error (`stderr`) is uncaptured in non-zero exiting subprocesses, troubleshooting logs remain empty. Proper usage of Python's `capture_output=True` enables structured JSON capturing on errors (retrieved through `subprocess.CalledProcessError.stderr`).

## Task
Fix the runner caller to capture `stderr` natively, and structure the emitted JSON log accordingly on failures (triggered via mock-bin/agy's `--fail` flag).

## Instruction
Run tests with: `bats track-atomic/day-10/test.bats`
