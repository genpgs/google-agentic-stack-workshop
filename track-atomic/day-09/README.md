# Day 09: Headless Agent Dispatcher Script

Dispatcher scripts using interactive `read` prompts will hang in automated or CI environments (which usually run in headless mode). 
Using argument parsing techniques, such as standard shell flag iterations `--task` and `--category`, ensures the dispatcher script operates fully non-interactively.

## Task
Remove `read` calls from the dispatcher and parse `--task` and `--category` arguments respectively to pass them down into the `agy agent dispatch` execution.

## Instruction
Run tests with: `bats track-atomic/day-09/test.bats`
