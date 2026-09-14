# Day 04 — Antigravity CLI Config Initialization (Python)

## Concept

### Relative vs Absolute Paths in Python Scripts

A common Python bug is loading files using a **relative path** like:

```python
CONFIG_PATH = "agy.config.json"
```

This resolves relative to the **current working directory** (`os.getcwd()`), not the
location of the script. If you run the script from a different directory — as happens
constantly in CI pipelines, test runners, and shell one-liners — Python will fail to find
the file:

```
FileNotFoundError: [Errno 2] No such file or directory: 'agy.config.json'
```

This is the root cause of the bug in `starter/config_loader.py`.

---

### Fixing It with `pathlib` and `__file__`

Python's `__file__` attribute is the absolute path of the **currently executing script**.
Combining it with `pathlib.Path` gives you a reliable anchor regardless of the current
working directory:

```python
from pathlib import Path

# __file__  →  /repo/track-atomic/day-04/solution/config_loader.py
# .resolve() ensures symlinks and ".." segments are fully expanded
SCRIPT_DIR = Path(__file__).resolve().parent

# Navigate to the config relative to the script, not cwd:
CONFIG_PATH = SCRIPT_DIR / "agy.config.json"
```

For larger monorepos you may need to walk further up the tree:

```python
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_PATH = REPO_ROOT / "track-atomic" / "day-04" / "solution" / "agy.config.json"
```

Both approaches are equivalent; the solution uses the explicit REPO_ROOT form so the path
logic is transparent to readers.

---

### Your Task

Fix `starter/config_loader.py` so that:

1. `CONFIG_PATH` is computed using `Path(__file__).resolve()` (or equivalent) — **not** a
   bare string literal.
2. The script exits with a clear error message if the config file does not exist.
3. It asserts `headless_default` is `True` and prints a validated JSON result:
   ```json
   {"headless_default": true, "status": "VALID"}
   ```

The script must exit **0** when run from **any directory**, including `/tmp`.

---

### Expected Config Schema

Both `starter/agy.config.json` and `solution/agy.config.json` have identical content:

```json
{
  "headless_default": true,
  "offline_mode": true,
  "mock_binary": "mock-bin/agy"
}
```

Key fields:

| Field            | Type    | Required | Meaning                              |
|------------------|---------|----------|--------------------------------------|
| `headless_default` | bool  | Yes      | CLI defaults to headless mode        |
| `offline_mode`   | bool    | Yes      | Prevents live API calls              |
| `mock_binary`    | string  | Yes      | Relative path to the mock executable |

---

## Running the Tests

```bash
# From the repo root:
bats track-atomic/day-04/test.bats
```

The test suite verifies:
- **Solution**: `python3 solution/config_loader.py` exits 0 from **any directory**
  (`/tmp` is used) and outputs valid JSON containing `"headless_default": true`.
- **Starter**: `python3 starter/config_loader.py` **fails** when run from `/tmp` because
  it uses a relative path that resolves to `/tmp/agy.config.json` (which does not exist).
