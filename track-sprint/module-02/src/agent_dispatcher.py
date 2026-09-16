#!/usr/bin/env python3
"""
track-sprint/module-02/src/agent_dispatcher.py

Autonomous agent dispatcher using Gemini Spark prompts and headless execution.
Orchestrates multi-turn conversations with stateful history and local tool calls.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"

sys.path.insert(0, str(Path(__file__).parent))
from spark_prompt_builder import SparkPromptBuilder
from turn_manager import TurnManager
from tools.workspace_tools import dispatch_tool


class AgentDispatcher:
    """Headless autonomous agent dispatcher with multi-turn state management."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.turn_manager = TurnManager()
        self._env = self._build_env()

    def _build_env(self) -> dict:
        env = os.environ.copy()
        env["PATH"] = str(MOCK_BIN) + ":" + env.get("PATH", "")
        env["AGY_OFFLINE_MODE"] = "1"
        return env

    def dispatch(self, task: str, category: str = "general") -> dict:
        """Dispatch a task headlessly via agy agent dispatch."""
        result = subprocess.run(
            ["agy", "agent", "dispatch",
             "--task", task, "--category", category,
             "--headless", "--json"],
            capture_output=True, text=True,
            env=self._env, timeout=self.timeout
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, ["agy"],
                output=result.stdout, stderr=result.stderr
            )
        return json.loads(result.stdout)

    def run_with_prompt(self, user_message: str, system_instruction: str = "") -> dict:
        """Run agy with a Spark prompt payload, track history."""
        self.turn_manager.add_user_message(user_message)
        builder = (SparkPromptBuilder(system_instruction)
                   .add_user_turn(user_message))
        errors = builder.validate()
        if errors:
            raise ValueError(f"Invalid prompt: {errors}")
        payload = builder.build()
        result = subprocess.run(
            ["agy", "run", "--headless", "--json", "--payload", payload],
            capture_output=True, text=True,
            env=self._env, timeout=self.timeout
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, ["agy"],
                output=result.stdout, stderr=result.stderr
            )
        response = json.loads(result.stdout)
        self.turn_manager.add_model_message(response.get("output", ""))
        return response

    def run_tool_and_continue(self, tool_name: str, params: dict) -> dict:
        """Execute a local workspace tool and add result to history."""
        tool_result = dispatch_tool(tool_name, params)
        self.turn_manager.add_tool_result(tool_name, tool_result)
        return tool_result

    def get_history(self) -> list[dict]:
        return self.turn_manager.get_history()
