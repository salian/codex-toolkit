---
name: build-prompt-pack
description: Build one prompt pack end to end in a Codex repository. Use when the user asks to implement a prompt pack, build a milestone such as M12 or 12_LEAD_CAPTURE, resume a pack build, or execute docs/prompt-packs/*.prompt.md.
---

# Build Prompt Pack

Build exactly one prompt pack with tests, quality gates, and logical commits.

## Inputs

Accept a pack id such as `M12`, `12`, `12_LEAD_CAPTURE`, or a direct pack path. If the id starts with `M`, strip it and left-pad the numeric prefix to two digits before globbing.

Search in order:

```text
docs/prompt-packs/<id>*.prompt.md
docs/prompts/<id>*.prompt.md
prompts/<id>*.prompt.md
.prompts/<id>*.prompt.md
```

If multiple packs match, ask the user which one. If no pack matches, ask for the path.

## Workflow

1. Read the pack, `_PREAMBLE.prompt.md`, `AGENTS.md`, and every referenced spec file.
2. Extract an execution plan from the pack's required deliverables, tests, wiring checklist, failure modes, and acceptance criteria.
3. Run a pre-flight touchpoint sweep using `references/build-workflow.md`.
4. Implement one logical step at a time:
   - read adjacent code first
   - build the deliverable
   - write tests with the change
   - satisfy assigned pre-flight obligations
   - run the relevant quality checks
   - commit only the files for that logical step
5. Capture spec'd-but-deferred obligations in `docs/dev/backlog.md`.
6. Capture unspecced improvement ideas in `docs/dev/ideas.md`; never build directly from ideas.
7. Run the full project quality gate after all steps.

## Resume

For interrupted builds, reconcile state from:

- current todo list or conversation summary
- `git log`
- changed files
- `.codex/prompt-pipeline/state.json` when present

Do not repeat already committed steps unless the current code is incomplete.

## References

Read `references/build-workflow.md` before implementing.

## Output

End with:

```text
RESULT: pass|fail|blocked
PHASE: build
PACK: <pack-id>
COMMITS: <count>
TEST_STATUS: pass|fail|skipped
BACKLOG_ADDED: <comma-separated ids or none>
IDEAS_ADDED: <comma-separated ids or none>
```
