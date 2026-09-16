# Day 16: Headless Status Polling Loop
Learn about bounded retry loops in bash, sleep intervals, max retries pattern, and why unbounded loops cause CI timeouts. Use `agy status --headless --json`.
Task: Fix the polling loop to have a max retry count (10) with a 1s sleep.
Instruction: Run `bats track-atomic/day-16/test.bats`.
