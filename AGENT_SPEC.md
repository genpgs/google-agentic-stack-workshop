# Specification: Agentic Learning Monorepo
- Scope: Gemini Spark, Antigravity 2.0, Antigravity CLI
- Structure:
  * .devcontainer/ (Codespaces, Python 3.11, bats-core, jq)
  * mock-bin/agy (mock executable for headless, offline CI)
  * track-atomic/ (30 daily 15-min challenges: README, starter, solution, test.bats)
  * track-sprint/ (4 workshop modules: README, workspace, pytest)
- Autograder Rules:
  * Tests must verify non-interactive headless flags (--headless, --json).
  * No network dependencies or live API quota usage during test runs.
