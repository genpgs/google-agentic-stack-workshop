#!/usr/bin/env python3
"""
track-sprint/module-02/src/spark_prompt_builder.py

Builds structured Gemini Spark prompt payloads for headless agent dispatch.
Ensures proper JSON escaping, role tag injection, and offline-safe serialization.
"""
import json
from dataclasses import dataclass, field
from typing import Any

SPARK_USER_ROLE = "user"
SPARK_MODEL_ROLE = "model"
SPARK_TOOL_ROLE = "tool"


@dataclass
class SparkTurn:
    role: str
    content: str
    tool_calls: list[dict] = field(default_factory=list)


class SparkPromptBuilder:
    """Builds Gemini Spark prompt payloads with proper escaping and role tags."""

    def __init__(self, system_instruction: str = ""):
        self.system_instruction = system_instruction
        self.turns: list[SparkTurn] = []

    def add_user_turn(self, content: str) -> "SparkPromptBuilder":
        self.turns.append(SparkTurn(role=SPARK_USER_ROLE, content=content))
        return self

    def add_model_turn(self, content: str) -> "SparkPromptBuilder":
        self.turns.append(SparkTurn(role=SPARK_MODEL_ROLE, content=content))
        return self

    def add_tool_result(self, tool_name: str, result: Any) -> "SparkPromptBuilder":
        self.turns.append(SparkTurn(
            role=SPARK_TOOL_ROLE,
            content=json.dumps(result),
            tool_calls=[{"tool_name": tool_name, "result": result}]
        ))
        return self

    def build(self) -> str:
        """Build the JSON payload string for --payload argument."""
        payload = {
            "system_instruction": self.system_instruction,
            "turns": [
                {"role": t.role, "content": t.content, "tool_calls": t.tool_calls}
                for t in self.turns
            ],
            "headless": True,
        }
        return json.dumps(payload)

    def validate(self) -> list[str]:
        """Validate the built payload. Returns list of error strings."""
        errors = []
        if not self.turns:
            errors.append("No turns added to prompt")
        roles = [t.role for t in self.turns]
        for i, role in enumerate(roles):
            if role not in (SPARK_USER_ROLE, SPARK_MODEL_ROLE, SPARK_TOOL_ROLE):
                errors.append(f"Invalid role at turn {i}: {role}")
        return errors
