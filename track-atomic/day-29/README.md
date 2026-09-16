# DAY 29: Offline Dependency Integrity Verifier (Python)

**Bug**: Integrity checker queries remote repository instead of checking local environment.

**Explain**:
Verifying dependencies in environments that may lack external internet access requires offline checks. Checking installed packages using `importlib.metadata` or `pip show --local` prevents network calls to the PyPI index, which is what `pip index versions` triggers. Additionally, verifying executables like `bats` and `jq` should be done purely via the local `PATH`.

**Task**:
Fix the integrity checker to use only local inspection (like `importlib.metadata` and `shutil.which`), eliminating network calls.

**Instruction**:
Run `bats track-atomic/day-29/test.bats` to check if dependencies are verified correctly and locally.
