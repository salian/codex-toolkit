#!/usr/bin/env python3
"""Install the Codex Toolkit commit message policy as a global git hook."""

from __future__ import annotations

import argparse
import datetime as dt
import stat
import subprocess
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "What changed:",
    "Why:",
    "Verification:",
    "Notes/Risks:",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing global hooksPath and back up an existing commit-msg hook",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    hooks_dir = Path.home() / ".githooks"
    current_hooks_path = git_config_get("core.hooksPath")
    if current_hooks_path:
        current_path = Path(current_hooks_path).expanduser()
        if current_path != hooks_dir and not args.force:
            print(
                "Refusing to replace existing global core.hooksPath="
                f"{current_hooks_path}. Re-run with --force to install "
                f"Codex Toolkit hooks at {hooks_dir}.",
                file=sys.stderr,
            )
            return 2

    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "commit-msg"
    contents = hook_contents()
    if hook_path.exists() and hook_path.read_text(encoding="utf-8", errors="replace") != contents:
        backup_path = hook_path.with_name(
            f"commit-msg.backup-{dt.datetime.now(dt.UTC).strftime('%Y%m%d%H%M%S')}"
        )
        hook_path.rename(backup_path)
        print(f"Backed up existing commit-msg hook to {backup_path}")
    hook_path.write_text(contents, encoding="utf-8")
    hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    template_path = Path.home() / ".stCommitMsg"
    if not template_path.exists() or not template_path.read_text(encoding="utf-8", errors="replace").strip():
        template_path.write_text(commit_template(), encoding="utf-8")

    subprocess.run(["git", "config", "--global", "core.hooksPath", str(hooks_dir)], check=True)
    subprocess.run(["git", "config", "--global", "commit.template", str(template_path)], check=True)

    print(f"Installed commit-msg policy at {hook_path}")
    print(f"Configured git core.hooksPath={hooks_dir}")
    print(f"Configured git commit.template={template_path}")
    print(f"Policy source: {repo_root}")
    return 0


def git_config_get(key: str) -> str | None:
    result = subprocess.run(
        ["git", "config", "--global", "--get", key],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    value = result.stdout.strip()
    return value or None


def commit_template() -> str:
    return """subject

What changed:
- 

Why:
- 

Verification:
- 

Notes/Risks:
- 
"""


def hook_contents() -> str:
    return f"""#!/bin/sh

message_file="$1"

if [ -z "$message_file" ] || [ ! -f "$message_file" ]; then
  echo "commit-msg hook: missing commit message file" >&2
  exit 1
fi

python3 - "$message_file" <<'PY'
import sys

path = sys.argv[1]
required_sections = ({required_sections_literal()})

with open(path, "r", encoding="utf-8", errors="replace") as handle:
    raw = handle.read()

lines = raw.replace("\\r\\n", "\\n").split("\\n")
content_lines = [
    line for line in lines
    if line.strip() and not line.lstrip().startswith("#")
]
message = "\\n".join(content_lines).strip()

if not message:
    print("Commit message is empty.", file=sys.stderr)
    sys.exit(1)

subject = content_lines[0].strip()
if len(subject) > 72:
    print("Commit subject must be 72 characters or fewer.", file=sys.stderr)
    sys.exit(1)

body = "\\n".join(content_lines[1:]).strip()
if len(body) < 40:
    print("Commit message must include a meaningful body.", file=sys.stderr)
    sys.exit(1)

missing = [section for section in required_sections if section not in body]
if missing:
    print(
        "Commit body is missing required section(s): " + ", ".join(missing),
        file=sys.stderr,
    )
    sys.exit(1)
PY
status=$?
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

git_dir="$(git rev-parse --git-dir 2>/dev/null || true)"
if [ -n "$git_dir" ] && [ -x "$git_dir/hooks/commit-msg" ]; then
  "$git_dir/hooks/commit-msg" "$message_file"
fi
"""


def required_sections_literal() -> str:
    return "".join(f"\n    {section!r}," for section in REQUIRED_SECTIONS) + "\n"


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        raise SystemExit(exc.returncode)
