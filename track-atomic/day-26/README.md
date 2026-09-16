# DAY 26: Python Subprocess Signal Handling & Graceful Termination (Python)

**Bug**: CLI wrapper leaves orphaned mock-bin processes on SIGTERM.

**Explain**:
Python's `signal.signal()` is used to set handlers for asynchronous events. Handling `SIGINT` (Ctrl+C) and `SIGTERM` (termination signal) is important when managing subprocesses. `subprocess.terminate()` gracefully asks a process to stop, while `.kill()` forcefully terminates it. Without these handlers, an application wrapping a long-running subprocess might exit on a signal, leaving the child process orphaned and running in the background. In Continuous Integration (CI) environments, these orphaned processes can cause resource leaks and potentially hang CI pipelines or exhaust system resources.

**Task**:
Add `SIGINT` and `SIGTERM` handlers that gracefully terminate the child processes before exit.

**Instruction**:
Run `bats track-atomic/day-26/test.bats` to check if your solution correctly handles termination signals.
