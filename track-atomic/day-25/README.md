# Day 25: BATS Execution Timeout & Deadlock Guard (Bash)

## Overview
CI tests need time bounds to prevent deadlocks from hanging the entire suite. The `timeout` command in bash returns exit code 124 when a command times out.

## Bug
The BATS test runner lacks a command timeout wrapper, allowing potential deadlocks (like `agy` session starting without `--headless`) to hang the tests.

## Task
Wrap all `agy` calls in `timeout 10s`.

## Instruction
Run tests with `bats track-atomic/day-25/test.bats`.
