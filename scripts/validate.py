#!/usr/bin/env python3
"""Validate the Codex Toolkit repository with only Python stdlib."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)


def main() -> int:
    errors: list[str] = []
    validate_plugin(errors)
    validate_marketplace(errors)
    validate_skills(errors)
    validate_repo_skill_links(errors)
    validate_custom_agents(errors)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed.")
    return 0


def validate_plugin(errors: list[str]) -> None:
    path = ROOT / ".codex-plugin" / "plugin.json"
    payload = load_json(path, errors)
    if payload is None:
        return
    for key in ("name", "version", "description", "skills", "interface"):
        if key not in payload:
            errors.append(f"{path}: missing `{key}`")
    skills_path = payload.get("skills")
    if isinstance(skills_path, str):
        if not (ROOT / skills_path).resolve().is_dir():
            errors.append(f"{path}: skills path `{skills_path}` does not resolve to a directory")
    interface = payload.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{path}: `interface` must be an object")
        return
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities", "defaultPrompt"):
        if key not in interface:
            errors.append(f"{path}: interface missing `{key}`")


def validate_marketplace(errors: list[str]) -> None:
    path = ROOT / ".agents" / "plugins" / "marketplace.json"
    payload = load_json(path, errors)
    if payload is None:
        return
    plugins = payload.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append(f"{path}: `plugins` must be a non-empty array")
        return
    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            errors.append(f"{path}: plugins[{index}] must be an object")
            continue
        source = plugin.get("source")
        if not isinstance(source, dict):
            errors.append(f"{path}: plugins[{index}].source must be an object")
            continue
        source_path = source.get("path")
        if not isinstance(source_path, str) or not source_path.startswith("./"):
            errors.append(f"{path}: plugins[{index}].source.path must start with `./`")
            continue
        plugin_root = (ROOT / source_path).resolve()
        if not (plugin_root / ".codex-plugin" / "plugin.json").is_file():
            errors.append(f"{path}: plugins[{index}].source.path does not point at a plugin root")


def validate_skills(errors: list[str]) -> None:
    skills_root = ROOT / "skills"
    if not skills_root.is_dir():
        errors.append("skills/: missing directory")
        return
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        if "TODO" in text or "[TODO" in text:
            errors.append(f"{skill_md}: contains TODO marker")
        match = SKILL_FRONTMATTER_RE.match(text)
        if not match:
            errors.append(f"{skill_md}: missing YAML frontmatter")
            continue
        frontmatter = parse_simple_yaml_mapping(match.group("body"))
        if frontmatter.get("name") != skill_dir.name:
            errors.append(f"{skill_md}: frontmatter name must equal folder name")
        if not frontmatter.get("description"):
            errors.append(f"{skill_md}: missing description")
        agent_yaml = skill_dir / "agents" / "openai.yaml"
        if agent_yaml.is_file():
            validate_openai_yaml(agent_yaml, errors)


def validate_openai_yaml(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for key in ("display_name:", "short_description:", "default_prompt:"):
        if key not in text:
            errors.append(f"{path}: missing `{key}`")


def validate_repo_skill_links(errors: list[str]) -> None:
    repo_skills = ROOT / ".agents" / "skills"
    if not repo_skills.is_dir():
        errors.append(".agents/skills/: missing directory")
        return
    source_names = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    link_names = {path.name for path in repo_skills.iterdir()}
    if source_names != link_names:
        errors.append(".agents/skills/: symlink set does not match skills/")
    for link in sorted(repo_skills.iterdir()):
        if not link.is_symlink():
            errors.append(f"{link}: must be a symlink to ../../skills/{link.name}")
            continue
        if not (link.resolve() / "SKILL.md").is_file():
            errors.append(f"{link}: symlink target is not a skill directory")


def validate_custom_agents(errors: list[str]) -> None:
    agents_root = ROOT / ".codex" / "agents"
    if not agents_root.is_dir():
        return
    for path in sorted(agents_root.glob("*.toml")):
        text = path.read_text(encoding="utf-8")
        for key in ("name", "description", "developer_instructions"):
            if not re.search(rf"(?m)^{key}\s*=", text):
                errors.append(f"{path}: missing `{key}`")


def parse_simple_yaml_mapping(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_json(path: Path, errors: list[str]) -> dict | None:
    if not path.is_file():
        errors.append(f"{path}: missing file")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}: expected JSON object")
        return None
    return payload


if __name__ == "__main__":
    sys.exit(main())

