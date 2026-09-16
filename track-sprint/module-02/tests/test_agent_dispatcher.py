#!/usr/bin/env python3
"""
track-sprint/module-02/tests/test_agent_dispatcher.py

Pytest test harness for Sprint Module 02: Gemini Spark Autonomous Agent & Tool Dispatcher.
All tests run strictly offline — no live API calls.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(SRC_DIR / "tools"))

from agent_dispatcher import AgentDispatcher
from spark_prompt_builder import SparkPromptBuilder
from turn_manager import TurnManager
from tools.workspace_tools import dispatch_tool, list_workspace_files, read_workspace_file


@pytest.fixture(autouse=True)
def set_offline_env(monkeypatch):
    monkeypatch.setenv("PATH", str(MOCK_BIN) + ":" + os.environ.get("PATH", ""))
    monkeypatch.setenv("AGY_OFFLINE_MODE", "1")


class TestAgentDispatchHeadless:
    """test_agent_dispatch_headless: Verifies agent orchestrates tasks without prompt pauses using --headless"""

    def test_dispatch_exits_zero_headless(self):
        dispatcher = AgentDispatcher()
        response = dispatcher.dispatch("analyze-workspace", "ci")
        assert response["status"] == "COMPLETED"
        assert response["metadata"]["headless"] is True

    def test_run_with_prompt_returns_completed(self):
        dispatcher = AgentDispatcher()
        response = dispatcher.run_with_prompt("List all Python files", "You are a CI assistant.")
        assert response["metadata"]["status"] == "COMPLETED"

    def test_headless_flag_in_subprocess_cmd(self, monkeypatch):
        captured = []
        original_run = subprocess.run
        def mock_run(cmd, **kwargs):
            captured.append(cmd)
            return original_run(cmd, **kwargs)
        monkeypatch.setattr(subprocess, "run", mock_run)
        dispatcher = AgentDispatcher()
        dispatcher.dispatch("test-task", "general")
        assert any("--headless" in c for c in captured)
        assert any("--json" in c for c in captured)


class TestToolCallRouting:
    """test_tool_call_routing: Confirms tool calls route to local workspace tools without external API requests"""

    def test_list_workspace_files_is_local(self):
        result = list_workspace_files(".")
        assert "files" in result
        assert isinstance(result["files"], list)

    def test_dispatch_tool_routes_correctly(self):
        result = dispatch_tool("list_workspace_files", {"directory": "."})
        assert "files" in result

    def test_unknown_tool_returns_error(self):
        result = dispatch_tool("nonexistent_tool", {})
        assert "error" in result

    def test_tool_result_added_to_history(self):
        dispatcher = AgentDispatcher()
        tool_result = dispatcher.run_tool_and_continue("list_workspace_files", {"directory": "."})
        assert "files" in tool_result
        history = dispatcher.get_history()
        assert any(h["role"] == "tool" for h in history)


class TestMultiTurnStatePreservation:
    """test_multi_turn_state_preservation: Asserts history buffer maintains context integrity"""

    def test_history_accumulates_across_turns(self):
        tm = TurnManager()
        tm.add_user_message("Hello")
        tm.add_model_message("Hi there")
        tm.add_tool_result("search", ["file1.py"])
        history = tm.get_history()
        assert len(history) == 3
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "model"
        assert history[2]["role"] == "tool"

    def test_tool_result_does_not_reset_history(self):
        tm = TurnManager()
        tm.add_user_message("Turn 1")
        tm.add_model_message("Response 1")
        tm.add_tool_result("my_tool", {"data": 42})
        assert len(tm.get_history()) == 3  # must not reset

    def test_session_payload_is_valid_json(self):
        tm = TurnManager()
        tm.add_user_message("Test message")
        payload = tm.to_session_payload()
        data = json.loads(payload)
        assert "turns" in data
        assert data["headless"] is True

    def test_prompt_builder_preserves_roles(self):
        builder = (SparkPromptBuilder("System instruction")
                   .add_user_turn("User msg")
                   .add_model_turn("Model response")
                   .add_tool_result("tool", {"ok": True}))
        payload = json.loads(builder.build())
        roles = [t["role"] for t in payload["turns"]]
        assert roles == ["user", "model", "tool"]


class TestAgentTimeoutAndRecovery:
    """test_agent_timeout_and_recovery: Validates agent recovers from mock CLI execution timeouts"""

    def test_subprocess_timeout_raises_timeout_error(self):
        dispatcher = AgentDispatcher(timeout=0.001)  # near-zero timeout
        with pytest.raises((subprocess.TimeoutExpired, subprocess.CalledProcessError, Exception)):
            dispatcher.dispatch("slow-task", "general")

    def test_non_zero_exit_raises_called_process_error(self, monkeypatch):
        def mock_fail(*args, **kwargs):
            import subprocess as sp
            mock_result = sp.CompletedProcess(args=[], returncode=1,
                                              stdout="", stderr='{"code": "EXECUTION_ERROR"}')
            return mock_result
        monkeypatch.setattr(subprocess, "run", mock_fail)
        dispatcher = AgentDispatcher()
        with pytest.raises(subprocess.CalledProcessError):
            dispatcher.dispatch("fail-task")

    def test_dispatcher_can_reinitialize_after_error(self):
        dispatcher = AgentDispatcher()
        # Reset history and re-run
        dispatcher.turn_manager.reset()
        assert dispatcher.get_history() == []
        response = dispatcher.dispatch("recovery-task", "general")
        assert response["status"] == "COMPLETED"
