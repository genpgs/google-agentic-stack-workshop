# Day 06: Mock Binary Fixture Injection

PATH manipulation in Python subprocesses is critical for ensuring tests are hermetic.
If we do not inject the `mock-bin` path into our subprocess environment variables, the script will call the global `agy` executable instead of our test fixture.
This leads to non-deterministic behaviors and breaks hermetic testing.

## Task
Fix the subprocess call in the starter code to use `mock-bin/agy` by updating the `PATH` environment variable.

## Instruction
Run tests with: `bats track-atomic/day-06/test.bats`
