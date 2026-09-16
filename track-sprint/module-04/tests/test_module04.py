#!/usr/bin/env python3
"""
track-sprint/module-04/tests/test_module04.py

Pytest test harness for Sprint Module 04: End-to-End Autonomous Software Factory.
All tests run strictly offline — no live API calls, no network egress.
"""
import json
import os
import socket
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"
WORKSPACE_DIR = Path(__file__).resolve().parents[1] / "workspace"
sys.path.insert(0, str(WORKSPACE_DIR))

from orchestrator import AutograderCore
from spark_bridge import run_single_bats, run_all_atomic_tests
from grade_reporter import GradeReporter
from sandbox_guard import SandboxGuard


@pytest.fixture(autouse=True)
def set_offline_env(monkeypatch):
    monkeypatch.setenv("PATH", str(MOCK_BIN) + ":" + os.environ.get("PATH", ""))
    monkeypatch.setenv("AGY_OFFLINE_MODE", "1")


class TestAutograderBatchEvaluation:
    """test_autograder_batch_evaluation: Verifies autograder runs all 30 atomic test.bats and parses structured results"""

    def test_run_atomic_evaluation_returns_dict(self):
        grader = AutograderCore()
        results = grader.run_atomic_evaluation()
        assert isinstance(results, dict)
        assert "total" in results
        assert "passed" in results
        assert "failed" in results

    def test_all_atomic_days_discovered(self):
        track_root = REPO_ROOT / "track-atomic"
        results = run_all_atomic_tests(track_root)
        assert results["total"] >= 15, f"Expected at least 15 days, found {results['total']}"

    def test_result_status_is_string(self):
        grader = AutograderCore()
        results = grader.run_atomic_evaluation()
        assert results["status"] in ("COMPLETED", "FAILED")

    def test_each_result_has_day_field(self):
        track_root = REPO_ROOT / "track-atomic"
        results = run_all_atomic_tests(track_root)
        for r in results["results"]:
            assert "day" in r


class TestZeroNetworkLeakage:
    """test_zero_network_leakage: Confirms pytest suite executes strictly offline with all egress blocked"""

    def test_no_live_socket_connections_during_grading(self):
        """Block socket.connect and verify autograder still completes."""
        original_connect = socket.socket.connect
        blocked_calls = []

        def mock_connect(self, address):
            blocked_calls.append(address)
            raise ConnectionRefusedError("Offline: network blocked")

        with patch.object(socket.socket, "connect", mock_connect):
            grader = AutograderCore()
            results = grader.run_atomic_evaluation()
        # No real connections should have been attempted
        assert blocked_calls == [], f"Unexpected socket connection attempts: {blocked_calls}"

    def test_mock_bin_is_used_not_global_agy(self):
        import shutil
        mock_agy = MOCK_BIN / "agy"
        assert mock_agy.exists(), "mock-bin/agy must exist"
        env_path = str(MOCK_BIN) + ":" + os.environ.get("PATH", "")
        found = shutil.which("agy", path=env_path)
        assert found == str(mock_agy), f"Expected mock-bin/agy, got {found}"

    def test_gy_offline_mode_env_set(self):
        grader = AutograderCore()
        env = grader._build_env()
        assert env["AGY_OFFLINE_MODE"] == "1"


class TestNonInteractiveReportGeneration:
    """test_non_interactive_report_generation: Validates grade_reporter outputs valid machine-readable JSON"""

    def test_reporter_generates_valid_json(self):
        batch = {"total": 30, "passed": 28, "failed": 2, "skipped": 0}
        sprint = [{"passed": True}, {"passed": True}, {"passed": True}]
        reporter = GradeReporter(batch, sprint)
        output = reporter.to_json()
        data = json.loads(output)  # must not raise
        assert "atomic_track" in data
        assert "sprint_track" in data
        assert "overall" in data

    def test_reporter_status_completed_when_all_pass(self):
        batch = {"total": 30, "passed": 30, "failed": 0, "skipped": 0}
        sprint = [{"passed": True}, {"passed": True}, {"passed": True}]
        reporter = GradeReporter(batch, sprint)
        report = reporter.generate()
        assert report["status"] == "COMPLETED"

    def test_reporter_status_failed_when_any_fail(self):
        batch = {"total": 30, "passed": 25, "failed": 5, "skipped": 0}
        reporter = GradeReporter(batch)
        report = reporter.generate()
        assert report["status"] == "FAILED"

    def test_report_has_timestamp(self):
        reporter = GradeReporter({"total": 0, "passed": 0, "failed": 0, "skipped": 0})
        report = reporter.generate()
        assert "timestamp" in report
        assert "T" in report["timestamp"]  # ISO 8601 format


class TestSandboxContainment:
    """test_sandbox_containment: Asserts tested code cannot modify files outside designated sandbox"""

    def test_sandbox_creates_temp_directory(self):
        guard = SandboxGuard()
        sandbox = guard.create()
        assert sandbox.exists()
        assert sandbox.is_dir()
        guard.destroy()
        assert not sandbox.exists()

    def test_sandbox_contains_writes(self):
        guard = SandboxGuard()
        sandbox = guard.create()
        try:
            written = guard.safe_write("output.txt", "test content")
            assert written.exists()
            assert guard.is_contained(written)
        finally:
            guard.destroy()

    def test_path_traversal_rejected(self):
        guard = SandboxGuard()
        guard.create()
        try:
            with pytest.raises(PermissionError, match="Path traversal"):
                guard.safe_write("../../etc/passwd", "hacked")
        finally:
            guard.destroy()

    def test_context_manager_auto_destroys(self, tmp_path):
        guard = SandboxGuard(base_dir=str(tmp_path))
        with guard.managed() as sandbox_path:
            assert sandbox_path.exists()
            guard.safe_write("test.txt", "content")
        assert not sandbox_path.exists()  # cleaned up

    def test_full_evaluation_sandbox_cleaned_up(self):
        grader = AutograderCore()
        result = grader.run_full_evaluation()
        report_path = Path(result["report_path"])
        # Sandbox is destroyed after context manager — report file should be gone
        assert not report_path.exists(), "Sandbox was not cleaned up after evaluation"
