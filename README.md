# Codex Toolkit

Codex-native skills for a prompt-pack build pipeline:

1. Convert specs into executable prompt packs.
2. Build one prompt pack at a time.
3. Verify build completeness, integration wiring, and spec-to-pack coverage.
4. Review local changes for correctness, security, and missing tests.
5. Optionally orchestrate build -> verify -> review with resumable state.
6. Create focused git commits with detailed message bodies.

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

The plugin bundles a Codex PreToolUse hook in `hooks/hooks.json`. After installing or updating the plugin, review and trust the hook in Codex when prompted. The hook blocks common bodyless `git commit` commands and allows detailed commit messages that include `What changed`, `Why`, `Verification`, and `Notes/Risks`.

For git-native enforcement outside Codex, run:

```bash
python3 scripts/install_git_commit_policy.py
```

That optional installer configures a global `commit-msg` hook and commit template for the current user. It is intentionally opt-in; installing the plugin does not rewrite global git settings.

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
| `$smart-commit` | Stage focused changes and create a detailed git commit. |

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
hooks/
  hooks.json
  pre_tool_use_commit_policy.py
scripts/
  install_git_commit_policy.py
  validate.py
skills/
  create-prompt-packs/
  build-prompt-pack/
  verify-build/
  verify-wiring/
  verify-coverage/
  review-changes/
  build-verify-review/
  smart-commit/
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
