# Day 23: Mock CLI Fixture Override Mechanism (Bash)

## Overview
The `AGY_FIXTURE_PATH` environment variable tells `mock-bin/agy` where to read JSON fixtures from, allowing dynamic fixture switching during testing. Hardcoded paths remove test flexibility.

## Bug
The script hardcodes the fixture path instead of respecting the `AGY_FIXTURE_PATH` environment override.

## Task
Fix the script to use `AGY_FIXTURE_PATH` if set, otherwise fallback to the default path.

## Instruction
Run tests with `bats track-atomic/day-23/test.bats`.
