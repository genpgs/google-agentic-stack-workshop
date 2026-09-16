#!/usr/bin/env python3
"""
track-sprint/module-03/tests/test_module03.py

Pytest test harness for Sprint Module 03: Antigravity 2.0 Multi-Agent Code Review & PR Bot.
All tests run strictly offline — no live API calls.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"
WORKSPACE_DIR = Path(__file__).resolve().parents[1] / "workspace"
sys.path.insert(0, str(WORKSPACE_DIR))

from pr_reviewer import PipelineEngine
from rules_engine import SubagentCoordinator, AgentMessage
from artifact_critic import critique_artifact, run_headless_critique
from patch_generator import apply_patch, parse_unified_diff


@pytest.fixture(autouse=True)
def set_offline_env(monkeypatch):
    monkeypatch.setenv("PATH", str(MOCK_BIN) + ":" + os.environ.get("PATH", ""))
    monkeypatch.setenv("AGY_OFFLINE_MODE", "1")


class TestPipelineMultiAgentFlow:
    """test_pipeline_multi_agent_flow: Asserts generator and critic communicate through structured JSON envelopes"""

    def test_agent_message_serializes_to_json(self):
        msg = AgentMessage(sender="pipeline", recipient="generator",
                           task="build", payload={"key": "val"})
        data = json.loads(msg.to_json())
        assert data["sender"] == "pipeline"
        assert data["recipient"] == "generator"
        assert data["status"] == "PENDING"

    def test_agent_message_round_trips(self):
        msg = AgentMessage(sender="a", recipient="b", task="t", payload={"x": 1})
        restored = AgentMessage.from_json(msg.to_json())
        assert restored.sender == msg.sender
        assert restored.recipient == msg.recipient

    def test_coordinator_routes_to_known_agents(self):
        coord = SubagentCoordinator()
        msg = AgentMessage(sender="pipeline", recipient="generator", task="gen")
        response = coord.send(msg)
        assert response.get("status") == "COMPLETED"

    def test_coordinator_rejects_unknown_agents(self):
        coord = SubagentCoordinator()
        msg = AgentMessage(sender="pipeline", recipient="unknown_agent", task="t")
        response = coord.send(msg)
        assert "error" in response

    def test_message_log_tracks_send_and_reply(self):
        coord = SubagentCoordinator()
        msg = AgentMessage(sender="pipeline", recipient="critic", task="review")
        coord.send(msg)
        log = coord.get_message_log()
        assert len(log) >= 1


class TestArtifactDeterministicOutput:
    """test_artifact_deterministic_output: Confirms generated artifacts match expected golden hashes under mock seeds"""

    def test_same_seed_produces_same_hash(self):
        engine = PipelineEngine(seed="test-seed-42")
        result1 = engine.generate_artifact("my_task", "def hello(): pass")
        engine2 = PipelineEngine(seed="test-seed-42")
        result2 = engine2.generate_artifact("my_task", "def hello(): pass")
        assert result1["hash"] == result2["hash"]

    def test_different_seed_produces_different_hash(self):
        engine1 = PipelineEngine(seed="seed-A")
        result1 = engine1.generate_artifact("task", "content")
        engine2 = PipelineEngine(seed="seed-B")
        result2 = engine2.generate_artifact("task", "content")
        assert result1["hash"] != result2["hash"]

    def test_artifact_contains_seed_in_content(self):
        engine = PipelineEngine(seed="golden-seed")
        result = engine.generate_artifact("test", "body")
        assert "golden-seed" in result["content"]

    def test_artifact_hash_is_sha256(self):
        engine = PipelineEngine(seed="s")
        result = engine.generate_artifact("t", "c")
        assert len(result["hash"]) == 64  # SHA-256 hex digest


class TestHeadlessCriticEvaluation:
    """test_headless_critic_evaluation: Verifies critic evaluation runs non-interactively and flags anomalies"""

    def test_critique_flags_shell_true(self):
        content = 'subprocess.run(cmd, shell=True)'
        result = critique_artifact(content, "test.py")
        assert result["status"] == "FLAGGED"
        assert any("SECURITY" in a["message"] for a in result["anomalies"])

    def test_critique_clean_content_passes(self):
        content = 'subprocess.run(["agy", "version"], capture_output=True)'
        result = critique_artifact(content, "clean.py")
        assert result["status"] == "CLEAN"
        assert result["anomaly_count"] == 0

    def test_headless_critique_returns_json(self):
        result = run_headless_critique(__file__)
        assert "local_critique" in result
        assert "status" in result["local_critique"]

    def test_critic_pipeline_returns_agy_response(self):
        engine = PipelineEngine(seed="critic-test")
        engine.generate_artifact("my-artifact", "def func(): pass")
        result = engine.critique_artifact_pipeline("my-artifact")
        assert "agy_response" in result
        assert result["agy_response"]["status"] == "COMPLETED"


class TestPatchApplicationSafety:
    """test_patch_application_safety: Validates diff_patcher rejects malformed patches without corrupting workspace"""

    def test_valid_patch_applies_successfully(self, tmp_path):
        patch = "--- a/test.py\n+++ b/test.py\n@@ -1,1 +1,1 @@\n-old\n+new\n"
        result = apply_patch(patch, str(tmp_path))
        assert result["applied"] is True
        assert "test.py" in result["files_modified"]

    def test_malformed_hunk_header_rejected(self, tmp_path):
        patch = "--- a/test.py\n+++ b/test.py\n@@ malformed @@\n-old\n+new\n"
        result = apply_patch(patch, str(tmp_path))
        assert result["applied"] is False
        assert "error" in result

    def test_path_traversal_rejected(self, tmp_path):
        patch = "--- a/../../etc/passwd\n+++ b/../../etc/passwd\n@@ -1,1 +1,1 @@\n-root\n+hacked\n"
        result = apply_patch(patch, str(tmp_path))
        assert result["applied"] is False

    def test_empty_patch_rejected(self, tmp_path):
        result = apply_patch("", str(tmp_path))
        assert result["applied"] is False
