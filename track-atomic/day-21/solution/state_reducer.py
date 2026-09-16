#!/usr/bin/env python3
"""Day 21 Solution: State reducer that preserves history across tool result appends."""
import json

class ConversationReducer:
    def __init__(self):
        self.history = []

    def add_turn(self, role, content):
        self.history.append({"role": role, "content": content})

    def add_tool_result(self, tool_name, result):
        # FIX: append to history, do not reset
        self.history.append({"role": "tool", "tool_name": tool_name, "result": result})

    def to_payload(self):
        return json.dumps({"turns": self.history, "status": "COMPLETED"})

if __name__ == "__main__":
    r = ConversationReducer()
    r.add_turn("user", "What files are in the repo?")
    r.add_turn("model", "I will search for you.")
    r.add_tool_result("search_files", ["README.md", "AGENT_SPEC.md"])
    payload = r.to_payload()
    data = json.loads(payload)
    assert len(data["turns"]) == 3, f"Expected 3 turns, got {len(data['turns'])}"
    print(payload)
