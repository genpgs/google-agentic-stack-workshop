#!/usr/bin/env python3
"""
track-sprint/module-04/workspace/orchestrator.py

Core autograder orchestrator for all 30 atomic days and 3 sprint modules.
Runs entirely offline in an air-gapped CI container.
"""
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"

sys.path.insert(0, str(Path(__file__).parent))
from spark_bridge import run_all_atomic_tests
from grade_reporter import GradeReporter
from sandbox_guard import SandboxGuard


class AutograderCore:
    """End-to-end autograder for the full Agentic Learning Monorepo curriculum."""

    def __init__(self, repo_root: Path | None = None):
        self.repo_root = repo_root or REPO_ROOT
        self.sandbox = SandboxGuard()
        self._results: dict = {}

    def _build_env(self) -> dict:
        env = os.environ.copy()
        env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
        env["AGY_OFFLINE_MODE"] = "1"
        return env

    def run_atomic_evaluation(self) -> dict:
        """Run all 30 atomic daily test.bats suites."""
        track_root = self.repo_root / "track-atomic"
        results = run_all_atomic_tests(track_root)
        self._results["atomic"] = results
        return results

    def run_sprint_evaluation(self) -> list[dict]:
        """Stub sprint evaluation — checks each module's test directory exists."""
        sprint_root = self.repo_root / "track-sprint"
        module_results = []
        for module_dir in sorted(sprint_root.glob("module-*/")):
            tests_dir = module_dir / "tests"
            passed = tests_dir.exists() and any(tests_dir.glob("test_*.py"))
            module_results.append({
                "module": module_dir.name,
                "passed": passed,
                "tests_dir_exists": tests_dir.exists(),
            })
        self._results["sprint"] = module_results
        return module_results

    def generate_report(self) -> str:
        """Generate final JSON grade report."""
        atomic = self._results.get("atomic", {"total": 0, "passed": 0, "failed": 0, "skipped": 0})
        sprint = self._results.get("sprint", [])
        reporter = GradeReporter(atomic, sprint)
        return reporter.to_json()

    def run_full_evaluation(self) -> dict:
        """Run complete autograder evaluation pipeline."""
        with self.sandbox.managed() as sandbox_path:
            atomic_results = self.run_atomic_evaluation()
            sprint_results = self.run_sprint_evaluation()
            report_json = self.generate_report()
            report_path = sandbox_path / "grade_report.json"
            report_path.write_text(report_json, encoding="utf-8")
            return {
                "atomic": atomic_results,
                "sprint": sprint_results,
                "report": json.loads(report_json),
                "report_path": str(report_path),
                "status": "COMPLETED",
            }


if __name__ == "__main__":
    grader = AutograderCore()
    result = grader.run_full_evaluation()
    print(json.dumps(result["report"], indent=2))
