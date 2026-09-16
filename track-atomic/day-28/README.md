# DAY 28: Structured Diff Assessor for Starter vs Solution (Bash)

**Bug**: Diff checker returns 0 even when starter and solution files are completely identical.

**Explain**:
The `diff` command returns specific exit codes: `0` means files are identical, `1` means they are different, and `2` means there was an error. For an automated test checking whether a solution was implemented, identical files (starter == solution) are a failure (the student hasn't done the task). A diff assessor must return a non-zero exit code when files are identical, and output a JSON summary of changes when they differ.

**Task**:
Fix the script to return a non-zero exit code when the provided files are identical.

**Instruction**:
Run `bats track-atomic/day-28/test.bats` to check if your diff assessor is behaving correctly.
