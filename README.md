# Codex Toolkit

Codex-native skills for a prompt-pack build pipeline:

1. Convert specs into executable prompt packs.
2. Build one prompt pack at a time.
3. Verify build completeness, integration wiring, and spec-to-pack coverage.
4. Review local changes for correctness, security, and missing tests.
5. Optionally orchestrate build -> verify -> review with resumable state.

This repository is a port of the process refined in `claude-toolkit`, but it is not a direct file copy. Codex uses skills, `AGENTS.md`, plugins, hooks, and subagents rather than Claude Code command files.

## Use During Development

The canonical skill source lives in `skills/`. For repo-local development, `.agents/skills/` contains symlinks to those same skill folders so Codex can discover them when this repo is the active workspace.

After changing a skill, restart Codex or start a new thread if the updated skill does not appear.

Validate the repo with:

```bash
python3 scripts/validate.py
```

## Install as a Local Plugin

This repo also includes a repo marketplace at `.agents/plugins/marketplace.json`. Because the repository root is the plugin root, the marketplace entry points at `./`.

From this repo, Codex should show the `Codex Toolkit Local` marketplace in the plugin directory after restart. Install `codex-toolkit` from that marketplace to test plugin packaging.

## Skills

| Skill | Purpose |
|---|---|
| `$create-prompt-packs` | Generate prompt packs from PRDs, roadmaps, `AGENTS.md`, and other spec files. |
| `$build-prompt-pack` | Execute one prompt pack with tests, quality gates, and logical commits. |
| `$verify-build` | Audit whether the pack's deliverables, tests, and acceptance criteria were built. |
| `$verify-wiring` | Audit whether built features are reachable end to end. |
| `$verify-coverage` | Audit whether every spec capability has an owning pack or named deferred home. |
| `$review-changes` | Review local changes for serious correctness, security, and test coverage issues. |
| `$build-verify-review` | Orchestrate the full pack pipeline with resumable state. |

## Layout

```text
.agents/
  plugins/
    marketplace.json
  skills/
    create-prompt-packs -> ../../skills/create-prompt-packs
    ...
.codex/
  agents/
    coverage-auditor.toml
    wiring-auditor.toml
    change-reviewer.toml
.codex-plugin/
  plugin.json
skills/
  create-prompt-packs/
  build-prompt-pack/
  verify-build/
  verify-wiring/
  verify-coverage/
  review-changes/
  build-verify-review/
```

## Custom Agents

The repo includes read-only custom agents for large audit fanout during local development. These are project-local `.codex/agents` files, not bundled plugin components. Installed plugin users get equivalent audit-role prompts through the relevant skill references:

- `skills/verify-coverage/references/subagent-prompts.md`
- `skills/verify-wiring/references/subagent-prompts.md`
- `skills/review-changes/references/subagent-prompts.md`

| Agent | Purpose |
|---|---|
| `coverage-auditor` | Inventory specs and map capabilities to prompt-pack ownership evidence. |
| `wiring-auditor` | Trace reachability, caller chains, scheduler registration, and security wiring. |
| `change-reviewer` | Review local changes for serious correctness, security, and test gaps. |

## Status

Initial port in progress. The current skills are Codex-native first-pass ports: they capture the core workflow contracts and stable output shapes, with detailed Claude-specific mechanics intentionally left behind.
