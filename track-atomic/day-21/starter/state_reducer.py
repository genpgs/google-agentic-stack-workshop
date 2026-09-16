#!/usr/bin/env python3
"""Day 21 Starter: State reducer that drops history on tool result append."""
import json

class ConversationReducer:
    def __init__(self):
        self.history = []

    def add_turn(self, role, content):
        self.history.append({"role": role, "content": content})

    def add_tool_result(self, tool_name, result):
        # BUG: resets history instead of appending
        self.history = [{"role": "tool", "tool_name": tool_name, "result": result}]

    def to_payload(self):
        return json.dumps({"turns": self.history})

if __name__ == "__main__":
    r = ConversationReducer()
    r.add_turn("user", "What files are in the repo?")
    r.add_turn("model", "I will search for you.")
    r.add_tool_result("search_files", ["README.md", "AGENT_SPEC.md"])
    print(r.to_payload())
