# Orchestrator State

Path: `.codex/prompt-pipeline/state.json`

## Shape

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

## Rules

- Save after every state transition.
- Never cache the pack list.
- Append to `history`; do not rewrite it.
- `phaseAttempts` is observational and never a hard cap.
- Use `halted` only for real blockers, not designed pack boundaries.
- Store upfront answers in `.codex/prompt-pipeline/answers.md`.

## Phase Values

Allowed `currentPhase` values:

- `build`
- `verify-build`
- `verify-wiring`
- `review-changes`

## Result Trailers

Every child skill must end with a stable trailer. The orchestrator decides from these fields, not prose.

Required fields:

```text
RESULT: pass|fail|blocked
PHASE: <phase>
PACK: <pack-id>
```

Phase-specific fields may include `GAPS`, `ADVISORY`, `BACKLOG_ADDED`, `IDEAS_ADDED`, `COMMITS`, and `TEST_STATUS`.

