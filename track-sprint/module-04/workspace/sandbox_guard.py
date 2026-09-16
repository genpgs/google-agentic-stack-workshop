#!/usr/bin/env python3
"""
track-sprint/module-04/src/sandbox_guard.py

Sandbox containment guard for autograder test execution.
Prevents tested code from modifying files outside the designated sandbox directory.
"""
import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path


class SandboxGuard:
    """Isolates test execution within a temporary sandbox directory."""

    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir
        self._sandbox: Path | None = None

    def create(self) -> Path:
        """Create a new temporary sandbox directory."""
        self._sandbox = Path(tempfile.mkdtemp(dir=self.base_dir, prefix="autograder_sandbox_"))
        return self._sandbox

    def destroy(self) -> None:
        """Remove the sandbox directory and all contents."""
        if self._sandbox and self._sandbox.exists():
            shutil.rmtree(self._sandbox)
            self._sandbox = None

    def is_contained(self, path: str | Path) -> bool:
        """Check whether a given path is contained within the sandbox."""
        if self._sandbox is None:
            return False
        try:
            Path(path).resolve().relative_to(self._sandbox.resolve())
            return True
        except ValueError:
            return False

    def safe_write(self, filename: str, content: str) -> Path:
        """Write a file inside the sandbox only. Raises if path escapes."""
        if self._sandbox is None:
            raise RuntimeError("Sandbox not created. Call create() first.")
        target = (self._sandbox / filename).resolve()
        if not self.is_contained(target):
            raise PermissionError(f"Path traversal attempt rejected: {filename}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    @contextmanager
    def managed(self):
        """Context manager that creates and auto-destroys the sandbox."""
        try:
            yield self.create()
        finally:
            self.destroy()

    @property
    def path(self) -> Path | None:
        return self._sandbox
