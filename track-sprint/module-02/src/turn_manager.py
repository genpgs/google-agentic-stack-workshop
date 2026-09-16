#!/usr/bin/env python3
"""
track-sprint/module-02/src/turn_manager.py

Manages multi-turn conversation state for Gemini Spark agent sessions.
Preserves history integrity across iterative tool invocations.
"""
import json
from typing import Any


class TurnManager:
    """Stateful multi-turn conversation history manager."""

    def __init__(self):
        self._history: list[dict] = []
        self._tool_calls: list[dict] = []

    def add_user_message(self, content: str) -> None:
        self._history.append({"role": "user", "content": content})

    def add_model_message(self, content: str, tool_calls: list[dict] | None = None) -> None:
        entry = {"role": "model", "content": content}
        if tool_calls:
            entry["tool_calls"] = tool_calls
            self._tool_calls.extend(tool_calls)
        self._history.append(entry)

    def add_tool_result(self, tool_name: str, result: Any) -> None:
        """Append tool result WITHOUT resetting history (preserves context)."""
        self._history.append({
            "role": "tool",
            "tool_name": tool_name,
            "result": result,
        })

    def get_history(self) -> list[dict]:
        return list(self._history)

    def to_session_payload(self) -> str:
        return json.dumps({
            "turns": self._history,
            "total_turns": len(self._history),
            "tool_calls": self._tool_calls,
            "headless": True,
        })

    def reset(self) -> None:
        self._history.clear()
        self._tool_calls.clear()
