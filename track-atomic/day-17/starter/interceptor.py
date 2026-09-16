#!/usr/bin/env python3
"""Day 17 Starter: Interceptor with whitespace bug in regex matching."""
import re, json

MOCK_ROUTES = {
    r"agy version": {"version": "2.0.0-mock", "status": "COMPLETED",
                     "metadata": {"status": "COMPLETED", "version": "2.0.0-mock", "headless": True}},
    r"agy run": {"task_id": "mock-001", "status": "COMPLETED",
                 "metadata": {"status": "COMPLETED", "version": "2.0.0-mock", "headless": True}},
}

def intercept(command):
    # BUG: does not strip trailing whitespace from command before matching
    for pattern, response in MOCK_ROUTES.items():
        if re.match(pattern, command):
            return json.dumps(response)
    return None

if __name__ == "__main__":
    cmd = "agy version  "  # trailing whitespace
    result = intercept(cmd)
    print(result if result else "NO MATCH")
