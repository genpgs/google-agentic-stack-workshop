# Day 21: Gemini Spark Multi-Turn Conversation State Reducer (Python)

## Overview
In multi-turn conversations, the model and user take alternating roles. When a tool is called, the result must be appended as a `tool` role message. Gemini Spark requires the conversation history to properly maintain context.

## Bug
The current state reducer drops the previous role history when appending tool result messages, effectively resetting the conversation buffer.

## Task
Fix the reducer to preserve role history when appending tool results.

## Instruction
Run tests with `bats track-atomic/day-21/test.bats`.
