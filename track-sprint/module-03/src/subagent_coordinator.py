#!/usr/bin/env python3
"""
track-sprint/module-03/src/subagent_coordinator.py

Coordinates multiple specialized Spark subagents via JSON message envelopes.
All inter-agent communication uses structured JSON; no plain-text interchange.
"""
import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
MOCK_BIN = REPO_ROOT / "mock-bin"


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    task: str
    payload: dict = field(default_factory=dict)
    status: str = "PENDING"

    def to_json(self) -> str:
        return json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "task": self.task,
            "payload": self.payload,
            "status": self.status,
        })

    @classmethod
    def from_json(cls, data: str) -> "AgentMessage":
        d = json.loads(data)
        return cls(**d)


class SubagentCoordinator:
    """Routes tasks to specialized subagents via agy agent dispatch."""

    KNOWN_AGENTS = {"generator", "critic", "validator"}

    def __init__(self):
        self._env = os.environ.copy()
        self._env["PATH"] = str(MOCK_BIN) + ":" + self._env.get("PATH", "")
        self._env["AGY_OFFLINE_MODE"] = "1"
        self._message_log: list[AgentMessage] = []

    def send(self, message: AgentMessage) -> dict:
        """Send a task message to a subagent via agy. Returns structured response."""
        if message.recipient not in self.KNOWN_AGENTS:
            return {"error": f"Unknown agent: {message.recipient}", "status": "FAILED"}
        self._message_log.append(message)
        result = subprocess.run(
            ["agy", "agent", "dispatch",
             "--task", message.task,
             "--category", message.recipient,
             "--headless", "--json"],
            capture_output=True, text=True,
            env=self._env, timeout=30
        )
        if result.returncode != 0:
            msg = AgentMessage(
                sender=message.recipient, recipient=message.sender,
                task=message.task, status="FAILED",
                payload={"error": result.stderr}
            )
            self._message_log.append(msg)
            return json.loads(result.stderr) if result.stderr else {"status": "FAILED"}
        response = json.loads(result.stdout)
        reply = AgentMessage(
            sender=message.recipient, recipient=message.sender,
            task=message.task, status="COMPLETED",
            payload=response
        )
        self._message_log.append(reply)
        return response

    def get_message_log(self) -> list[dict]:
        return [json.loads(m.to_json()) for m in self._message_log]
