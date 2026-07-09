---
name: build-verify-review
description: Orchestrate the Codex prompt-pack pipeline. Use when the user wants to build prompt packs through build, verify-build, verify-wiring, review-changes, and retry loops with resumable state.
---

# Build Verify Review

Run the full prompt-pack pipeline for one pack per session:

1. `$build-prompt-pack`
2. `$verify-build`
3. `$verify-wiring`
4. `$review-changes`

Do not assume invoking this skill automatically loads the child skill bodies. Before running a phase, read the sibling skill file for that phase (`../build-prompt-pack/SKILL.md`, `../verify-build/SKILL.md`, `../verify-wiring/SKILL.md`, or `../review-changes/SKILL.md`) and any direct references it names.

## State

Persist state to `.codex/prompt-pipeline/state.json`.

Shape:

```json
{
  "completedPacks": [],
  "currentPack": null,
  "currentPhase": null,
  "phaseAttempts": 0,
  "lastUpdated": "2026-07-09T00:00:00Z",
  "history": [],
  "halted": null
}
```

Never cache the pack list in state. Re-enumerate prompt packs from disk each session and subtract `completedPacks`.

## Workflow

1. Handle flags from the user prompt: status, reset, from-pack, only-pack, skip-questions.
2. Enumerate pack files from the standard prompt-pack paths.
3. Resume halted state only after reporting the halt reason.
4. Ask upfront blocking questions for the current pack unless answers are already in `.codex/prompt-pipeline/answers.md` or the user opted out.
5. Run the current phase and require its result trailer.
6. If `RESULT: pass`, advance to the next phase.
7. If `RESULT: fail`, fix deterministic in-scope gaps, commit logical fixes, and retry the same phase.
8. If `RESULT: blocked`, set `halted`, save state, and stop loudly.
9. After review passes, mark the pack complete, reconcile resolved backlog entries, save state, and stop at the pack boundary.

## Loop Rules

- Do not ask the user to continue between phases.
- Do not retry a verifier without making a relevant change.
- Advisory `verify-wiring` findings do not trigger retries.
- Backlogged review findings do not trigger retries.
- There is no attempt cap, but print a convergence warning after every five attempts on the same phase.

## References

Read `references/orchestrator-state.md` before editing state files or changing phase transitions.

## Output

End pack sessions with:

```text
RESULT: pass|blocked
PHASE: build-verify-review
PACK: <pack-id>
COMPLETED: true|false
NEXT_PACK: <pack-id or none>
HALTED_REASON: <reason or none>
```
