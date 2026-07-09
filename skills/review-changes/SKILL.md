---
name: review-changes
description: Review local code changes for serious issues. Use after a prompt-pack build or before committing to find correctness bugs, security issues, behavior regressions, missing tests, and out-of-scope findings that should be backlogged.
---

# Review Changes

Run an independent review of the current changes. In Codex this is a native review workflow, not an external Codex shell-out by default.

## Scope Selection

Resolve scope in this order:

1. If the user names a pack, review commits and uncommitted changes associated with that pack.
2. If the user provides a base ref, review changes since that ref.
3. If there are uncommitted changes, review those first.
4. Otherwise review the recent commit range most likely tied to the current task.

## Review Priorities

Prioritize:

- correctness bugs
- security/privacy issues
- behavior regressions
- missed edge cases
- missing tests for changed behavior
- broken prompt-pack contracts

Do not spend findings on style preferences unless they create a real defect.

## Triage

For each finding:

- Fix legitimate in-scope bugs immediately when the user asked for autonomous completion or an orchestrator invoked this skill.
- Backlog real issues that belong to a later pack in `docs/dev/backlog.md`.
- Capture unspecced improvement ideas in `docs/dev/ideas.md`.
- Dismiss false positives with a one-line reason.

When a finding touches a classification, invariant, or state machine, re-derive the full decision table before fixing.

## Subagents

For larger reviews, explicitly spawn read-only subagents by concern or changed area. Read `references/subagent-prompts.md` for the packaged change-reviewer prompt. The parent agent owns final triage and must not pass through style-only findings.

## Output

End with:

```text
RESULT: pass|fail|blocked
PHASE: review-changes
PACK: <pack-id or none>
SCOPE: <description>
FINDINGS: <count>
LEGITIMATE: <count>
DISMISSED: <count>
BACKLOGGED: <count>
BACKLOG_ADDED: <comma-separated ids or none>
IDEAS_ADDED: <comma-separated ids or none>
```
