#!/usr/bin/env python3
"""Block Codex Bash git commits that are likely to omit a detailed body."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shlex
import sys


REQUIRED_SECTIONS = (
    "What changed:",
    "Why:",
    "Verification:",
    "Notes/Risks:",
)


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def command_from_payload() -> str:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return ""

    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command")
    return command if isinstance(command, str) else ""


def is_git_commit(tokens: list[str]) -> bool:
    if not tokens:
        return False
    if tokens[0] == "git" and len(tokens) > 1:
        return tokens[1] == "commit"
    return tokens[0].endswith("/git") and len(tokens) > 1 and tokens[1] == "commit"


def heredoc_message(command: str) -> str | None:
    match = re.search(r"<<-?'?([A-Za-z0-9_.-]+)'?\n(.*?)(?:\n\1\s*)$", command, re.S)
    if not match:
        return None
    return match.group(2)


def has_detailed_body(message: str) -> bool:
    lines = [line.rstrip() for line in message.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1].strip():
        lines.pop()
    if len(lines) < 4:
        return False
    if not lines[0].strip() or len(lines[0].strip()) > 72:
        return False
    if lines[1].strip():
        return False
    body = "\n".join(lines[2:])
    if len(body.strip()) < 40:
        return False
    return all(section in body for section in REQUIRED_SECTIONS)


def message_file_from_tokens(tokens: list[str]) -> str | None:
    for index, token in enumerate(tokens):
        if token in {"-F", "--file"} and index + 1 < len(tokens):
            return tokens[index + 1]
        if token.startswith("--file="):
            return token.split("=", 1)[1]
    return None


def file_message(path_text: str) -> str | None:
    if path_text == "-":
        return None
    try:
        path = Path(path_text).expanduser()
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def main() -> int:
    command = command_from_payload()
    if not command:
        return 0

    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return 0

    if not is_git_commit(tokens):
        return 0

    if "--no-verify" in tokens:
        deny("Use of git commit --no-verify is blocked.")
        return 0

    message = heredoc_message(command)
    if message is not None and has_detailed_body(message):
        return 0

    file_arg = message_file_from_tokens(tokens)
    if file_arg:
        message = file_message(file_arg)
        if message is not None and has_detailed_body(message):
            return 0

    deny(
        "Codex commits must use a detailed body with What changed, Why, "
        "Verification, and Notes/Risks. Use git commit -F - <<'EOF' with "
        "the required sections."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
