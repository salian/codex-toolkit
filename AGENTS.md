# Codex Toolkit Instructions

This repository is a Codex plugin that ports the Claude prompt-pack pipeline into Codex-native skills. Keep the implementation Codex-first; use the Claude toolkit only as source material for behavior.

## Repository Layout

- `.codex-plugin/plugin.json` - Codex plugin manifest.
- `.agents/skills/<name>` - repo-local development symlinks to `skills/<name>`.
- `.agents/plugins/marketplace.json` - repo marketplace entry for installing this plugin locally.
- `skills/<name>/SKILL.md` - Codex agent skills.
- `skills/<name>/references/` - detailed workflow references loaded only when needed.
- `CODEX_PORTABILITY_EVALUATION.md` - migration rationale and mapping from Claude to Codex.

## Authoring Rules

- Prefer Codex skills over custom prompts. Custom prompts are deprecated for reusable workflows.
- Keep each `SKILL.md` concise. Move long procedures, tables, and examples into `references/`.
- Skill frontmatter must contain only `name` and `description`.
- Descriptions are trigger-critical: state what the skill does and when to use it.
- Use `AGENTS.md` terminology for Codex project guidance. Do not introduce `CLAUDE.md` in Codex-side generated artifacts except when discussing migration from Claude.
- Keep runtime state under `.codex/prompt-pipeline/` and durable project artifacts under `docs/`.
- End verifier skills with the stable result trailer documented in the skill body.

## Validation

After editing plugin, skill, marketplace, or agent metadata, run the repo-local stdlib validator:

```bash
python3 scripts/validate.py
```

When the system skill dependencies are available, also run the official validators for the files you changed.

## Change Hygiene

- Update `README.md` when adding, removing, or renaming a skill.
- Update `CHANGELOG.md` for meaningful behavior or packaging changes.
- Keep changes scoped; do not import Claude command files wholesale.
