---
name: smart-commit
description: Stage focused changes and create a detailed git commit. Use when the user asks Codex to commit, save progress, checkpoint work, create a baseline commit, or make a git commit.
---

# Smart Commit

Create focused git commits with required detailed message bodies.

## Workflow

1. Run `git status --short --branch` and inspect the relevant diffs before staging.
2. If the project has a `CHANGELOG.md`, update it for meaningful behavior, packaging, or documentation changes. Do not duplicate existing entries.
3. Stage only relevant files. Do not use `git add .`; stage explicit paths or pathspec groups.
4. Never stage secrets, `.env` files, `.DS_Store`, dependency folders, generated output directories, or local tool settings.
5. Create the commit with a detailed message body. Treat user-provided short text as the subject unless it already includes a complete body.
6. Verify with `git status --short --branch` and `git log --format='%h %s%n%b' -1`.

## Message Format

Use this shape for every commit:

```text
subject

What changed:
- ...

Why:
- ...

Verification:
- ...

Notes/Risks:
- ...
```

Rules:

- Subject: imperative, under 72 characters, Conventional Commits when applicable.
- Body: always present and separated from the subject by a blank line.
- Bullets: concise, specific, and factual.
- If a section has nothing material to report, write `- None`.
- Never use a single `git commit -m "subject"`.

Preferred command:

```bash
git commit -F - <<'EOF'
subject

What changed:
- ...

Why:
- ...

Verification:
- ...

Notes/Risks:
- ...
EOF
```

## Constraints

- Never amend unless the user explicitly asks.
- Never push unless the user explicitly asks.
- Never use `--no-verify`.
- If hooks fail, fix the issue and create a new commit attempt.

## Optional Git Enforcement

This plugin bundles a Codex PreToolUse hook that blocks common bodyless commit commands when the plugin is installed and its hooks are trusted.

For git-native enforcement outside Codex, run `python3 scripts/install_git_commit_policy.py` from the plugin or repository root. The installer configures a global `commit-msg` hook that rejects commits missing the required sections.
