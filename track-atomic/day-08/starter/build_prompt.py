#!/usr/bin/env python3
"""Day 08 Starter: Buggy prompt builder with unsafe string interpolation."""
import subprocess, os
from pathlib import Path

ROLE_TAG = '<spark:role name="assistant">'
USER_INPUT = 'Say "hello world"'  # contains double quotes

def build_payload(user_input):
    # BUG: raw f-string interpolation breaks JSON when user_input has quotes
    return f'{{"prompt": "{user_input}", "role": "{ROLE_TAG}"}}'

if __name__ == "__main__":
    payload = build_payload(USER_INPUT)
    print(payload)
