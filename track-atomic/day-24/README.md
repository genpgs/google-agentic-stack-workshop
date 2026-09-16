# Day 24: Antigravity 2.0 Task Manifest Validator (Python)

## Overview
The task manifest must include an `autograder` block pointing to starter, solution, and test files to be valid. Missing these prevents autograding from working properly.

## Bug
The current validator permits missing autograder block (starter, solution, test.bats) in day specifications.

## Task
Fix the validator to require and check for the `autograder` block and its sub-keys.

## Instruction
Run tests with `bats track-atomic/day-24/test.bats`.
