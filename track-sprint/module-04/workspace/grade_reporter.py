#!/usr/bin/env python3
"""
track-sprint/module-04/src/grade_reporter.py

Generates machine-readable JSON grade reports from autograder results.
No manual interaction required — fully non-interactive output.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


class GradeReporter:
    """Compiles autograder results into a structured JSON grade report."""

    def __init__(self, batch_results: dict, sprint_results: list[dict] | None = None):
        self.batch_results = batch_results
        self.sprint_results = sprint_results or []
        self._timestamp = datetime.now(timezone.utc).isoformat()

    def _atomic_score(self) -> dict:
        total = self.batch_results.get("total", 0)
        passed = self.batch_results.get("passed", 0)
        skipped = self.batch_results.get("skipped", 0)
        return {
            "total_days": total,
            "passed": passed,
            "skipped": skipped,
            "failed": total - passed - skipped,
            "score_pct": round(passed / total * 100, 1) if total > 0 else 0.0,
        }

    def _sprint_score(self) -> dict:
        total = len(self.sprint_results)
        passed = sum(1 for r in self.sprint_results if r.get("passed"))
        return {
            "total_modules": total,
            "passed": passed,
            "failed": total - passed,
            "score_pct": round(passed / total * 100, 1) if total > 0 else 0.0,
        }

    def generate(self) -> dict:
        """Generate the full grade report as a Python dict."""
        atomic = self._atomic_score()
        sprint = self._sprint_score()
        overall_passed = atomic["passed"] + sprint["passed"]
        overall_total = atomic["total_days"] + sprint["total_modules"]
        return {
            "report_version": "1.0",
            "timestamp": self._timestamp,
            "monorepo_version": "2.0.0",
            "atomic_track": atomic,
            "sprint_track": sprint,
            "overall": {
                "total": overall_total,
                "passed": overall_passed,
                "score_pct": round(overall_passed / overall_total * 100, 1) if overall_total > 0 else 0.0,
            },
            "status": "COMPLETED" if atomic["failed"] == 0 and sprint["failed"] == 0 else "FAILED",
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize the report to JSON string."""
        return json.dumps(self.generate(), indent=indent)


if __name__ == "__main__":
    sample_batch = {"total": 30, "passed": 28, "failed": 2, "skipped": 0}
    sample_sprint = [{"passed": True}, {"passed": True}, {"passed": False}]
    reporter = GradeReporter(sample_batch, sample_sprint)
    print(reporter.to_json())
