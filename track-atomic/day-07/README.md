# Day 07: BATS Test Suite Assertion for CLI Exit Codes

When checking whether a command failed in a BATS script, asserting on the `$status` variable (which captures the exit code) is more robust than matching regex patterns against standard output.
The `mock-bin/agy` test binary will emit an exit code `2` with `INVALID_ARGUMENT` structured JSON on stderr if required arguments are missing.

## Task
Fix the BATS test in the starter code to assert `[ "$status" -eq 2 ]` and to check the structured JSON output on standard error.

## Instruction
Run tests with: `bats track-atomic/day-07/test.bats`
