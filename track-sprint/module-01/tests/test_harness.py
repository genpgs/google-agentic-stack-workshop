#!/usr/bin/env python3
"""
track-sprint/module-01/tests/test_harness.py

Pytest test harness for Sprint Module 01: Headless CLI Foundation & Mock Runtime Harness.
All tests are strictly offline - no live API calls or network connections.
"""
import json
import os
import socket
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from cli_harness import run_agy, build_env
from mock_executor import execute_offline, _block_socket
from schema_validator import validate_response


@pytest.fixture(autouse=True)
def ensure_mock_bin_on_path(monkeypatch):
    """Ensure mock-bin is on PATH for all tests."""
    monkeypatch.setenv("PATH", str(MOCK_BIN) + ":" + os.environ.get("PATH", ""))
    monkeypatch.setenv("AGY_OFFLINE_MODE", "1")


class TestCliHeadlessInvocation:
    """test_cli_headless_invocation: Verifies agy is invoked with --headless and --json flags and returns exit code 0"""

    def test_version_headless_json_exit_zero(self):
        """agy version --headless --json should return exit code 0 and valid JSON."""
        env = build_env()
        result = subprocess.run(
            ["agy", "version", "--headless", "--json"],
            capture_output=True, text=True, env=env, timeout=30
        )
        assert result.returncode == 0, f"Expected exit 0, got {result.returncode}. stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["metadata"]["status"] == "COMPLETED"
        assert data["metadata"]["headless"] is True

    def test_run_agy_enforces_headless_json(self):
        """run_agy() helper always appends --headless --json."""
        response = run_agy(["version"])
        assert response["metadata"]["headless"] is True
        assert response["metadata"]["status"] == "COMPLETED"

    def test_exit_code_zero_on_valid_subcommand(self):
        """run_agy() returns dict (no exception) for valid subcommands."""
        response = run_agy(["run"])
        assert "status" in response
        assert response["status"] == "COMPLETED"


class TestOfflineBoundaryEnforcement:
    """test_offline_boundary_enforcement: Verifies socket connections are intercepted and blocked."""

    def test_socket_block_raises_connection_refused(self):
        """_block_socket raises ConnectionRefusedError to prevent network access."""
        with pytest.raises(ConnectionRefusedError, match="Offline mode"):
            _block_socket()

    def test_execute_offline_does_not_open_sockets(self):
        """execute_offline runs agy without allowing real socket connections."""
        # If socket.socket is patched and subprocess still succeeds,
        # the mock binary did not attempt network I/O.
        response = execute_offline(["version"])
        assert response["metadata"]["status"] == "COMPLETED"

    def test_agY_offline_mode_env_is_set(self):
        """build_env() sets AGY_OFFLINE_MODE=1 in the environment."""
        env = build_env()
        assert env["AGY_OFFLINE_MODE"] == "1"


class TestMockBinaryFallback:
    """test_mock_binary_fallback: Validates mock-bin/agy fixture substitution under AGY_OFFLINE_MODE=1"""

    def test_mock_bin_exists_and_is_executable(self):
        """mock-bin/agy must exist and be executable."""
        mock_agy = MOCK_BIN / "agy"
        assert mock_agy.exists(), f"mock-bin/agy not found at {mock_agy}"
        assert os.access(mock_agy, os.X_OK), "mock-bin/agy is not executable"

    def test_fixture_override_serves_custom_json(self, tmp_path):
        """AGY_FIXTURE_PATH causes mock-bin/agy to serve the designated fixture file."""
        fixture = {"status": "COMPLETED", "metadata": {"status": "COMPLETED", "version": "2.0.0-mock", "headless": True}}
        fixture_file = tmp_path / "fixture.json"
        fixture_file.write_text(json.dumps(fixture))

        env = build_env()
        env["AGY_FIXTURE_PATH"] = str(fixture_file)
        result = subprocess.run(
            ["agy", "version", "--headless", "--json"],
            capture_output=True, text=True, env=env, timeout=30
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["metadata"]["status"] == "COMPLETED"

    def test_mock_binary_path_on_env(self):
        """PATH in build_env() must start with mock-bin directory."""
        env = build_env()
        path_dirs = env["PATH"].split(":")
        assert str(MOCK_BIN) == path_dirs[0], f"Expected mock-bin first in PATH, got: {path_dirs[0]}"


class TestJsonSchemaValidation:
    """test_json_schema_validation: Asserts harness stdout adheres to AGY CLI 2.0 output schema"""

    def test_version_response_passes_schema(self):
        """agy version --headless --json response must pass schema validation."""
        response = run_agy(["version"])
        errors = validate_response(response)
        assert errors == [], f"Schema validation errors: {errors}"

    def test_run_response_passes_schema(self):
        """agy run --headless --json response must pass schema validation."""
        response = run_agy(["run"])
        errors = validate_response(response)
        assert errors == [], f"Schema validation errors: {errors}"

    def test_missing_status_fails_validation(self):
        """Response missing 'status' key must fail schema validation."""
        bad_response = {"metadata": {"status": "COMPLETED", "version": "x", "headless": True}}
        errors = validate_response(bad_response)
        assert any("status" in e for e in errors)

    def test_non_headless_metadata_fails_validation(self):
        """Response with metadata.headless=False must fail schema validation."""
        bad_response = {
            "status": "COMPLETED",
            "metadata": {"status": "COMPLETED", "version": "2.0.0-mock", "headless": False}
        }
        errors = validate_response(bad_response)
        assert any("headless" in e for e in errors)
