# Day 08: Gemini Spark Prompt Assembly & Escaping

When constructing JSON payloads for CLI commands, raw Python f-strings are susceptible to JSON formatting issues. Unescaped quotes inside user inputs will break the CLI payload JSON. Using `json.dumps()` correctly formats strings for CLI JSON ingestion.

## Task
Fix the prompt template builder to use `json.dumps()` instead of raw interpolation, properly preserving the JSON formatting when user inputs include quotes. 

## Instruction
Run tests with: `bats track-atomic/day-08/test.bats`
