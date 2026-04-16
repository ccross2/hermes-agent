from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


CLASSIC_PRESENTATION = "classic"
CLAUDE_CODE_PRESENTATION = "claude_code"


def normalize_presentation_mode(mode: object) -> str:
    raw = str(mode or "").strip().lower().replace("-", "_")
    if raw == CLAUDE_CODE_PRESENTATION:
        return CLAUDE_CODE_PRESENTATION
    return CLASSIC_PRESENTATION


def is_claude_code_mode(mode: object) -> bool:
    return normalize_presentation_mode(mode) == CLAUDE_CODE_PRESENTATION


def summarize_tool_activity(function_name: Optional[str], preview: Optional[str]) -> str:
    label = (preview or function_name or "working").strip()
    if not label:
        label = "working"

    tool_name = (function_name or "").strip().lower()
    if tool_name == "terminal":
        prefix = "Bash"
    elif tool_name == "browser_navigate":
        prefix = "Browser"
    elif tool_name.startswith("browser_"):
        prefix = "Browser"
    elif tool_name in {"read_file", "search_files", "write_file", "patch"}:
        prefix = "Files"
    elif tool_name in {"web_search", "web_extract"}:
        prefix = "Web"
    else:
        prefix = (function_name or "Tool").replace("_", " ").strip().title() or "Tool"

    return f"{prefix} · {label}"


def workspace_label(cwd: Optional[str] = None) -> str:
    current = cwd or os.getenv("TERMINAL_CWD") or os.getcwd()
    path = Path(current)
    parts = path.parts
    if "cDesign" in parts:
        return "cDesign"
    return path.name or current


def approval_label(approval_state: object) -> str:
    return "approval" if approval_state else "no-approval"


def shell_count_label(background_tasks: object) -> str:
    count = len(background_tasks or {})
    return f"{count} shell" if count == 1 else f"{count} shells"
