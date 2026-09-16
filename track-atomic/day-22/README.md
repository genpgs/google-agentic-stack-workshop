# Day 22: Headless Failure Telemetry Formatter (Bash)

## Overview
Structured logging using the NDJSON (Newline Delimited JSON) format enables efficient log parsing by tools like `jq`. Plain text logs interspersed with JSON will break downstream `jq` consumers in CI pipelines.

## Bug
The telemetry script sends logs to stdout as raw text, which breaks CI pipelines trying to parse JSON.

## Task
Fix the telemetry script to emit all log lines as JSON objects with `.severity` and `.message`.

## Instruction
Run tests with `bats track-atomic/day-22/test.bats`.
