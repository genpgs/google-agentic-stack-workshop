#!/usr/bin/env python3
"""
track-sprint/module-02/src/tools/workspace_tools.py

Local workspace tool implementations for the autonomous agent dispatcher.
All operations are purely local — no network access.
"""
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def list_workspace_files(directory: str = ".", extensions: list[str] | None = None) -> dict:
    """List files in a workspace directory, optionally filtered by extension."""
    target = (REPO_ROOT / directory).resolve()
    if not target.exists():
        return {"error": f"Directory not found: {directory}", "files": []}
    files = []
    for p in sorted(target.rglob("*")):
        if p.is_file():
            if extensions is None or p.suffix in extensions:
                files.append(str(p.relative_to(REPO_ROOT)))
    return {"directory": directory, "files": files, "count": len(files)}


def read_workspace_file(filepath: str) -> dict:
    """Read a file from the workspace. Returns content or error."""
    target = (REPO_ROOT / filepath).resolve()
    if not target.exists():
        return {"error": f"File not found: {filepath}", "content": None}
    try:
        content = target.read_text(encoding="utf-8")
        return {"filepath": filepath, "content": content, "size": len(content)}
    except Exception as e:
        return {"error": str(e), "content": None}


def write_workspace_file(filepath: str, content: str, sandbox_root: str | None = None) -> dict:
    """Write content to a workspace file. Restricted to sandbox_root if provided."""
    if sandbox_root:
        target = (Path(sandbox_root) / filepath).resolve()
        if not str(target).startswith(str(Path(sandbox_root).resolve())):
            return {"error": "Path traversal attempt detected", "written": False}
    else:
        target = (REPO_ROOT / filepath).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"filepath": str(target), "written": True, "size": len(content)}


TOOL_REGISTRY = {
    "list_workspace_files": list_workspace_files,
    "read_workspace_file": read_workspace_file,
    "write_workspace_file": write_workspace_file,
}


def dispatch_tool(tool_name: str, params: dict) -> dict:
    """Dispatch a tool call by name with parameters."""
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"Unknown tool: {tool_name}"}
    return TOOL_REGISTRY[tool_name](**params)
