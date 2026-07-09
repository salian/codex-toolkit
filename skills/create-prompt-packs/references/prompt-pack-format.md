# Prompt Pack Format

Prompt packs live in `docs/prompt-packs/` and use the suffix `.prompt.md`.

## Required Files

```text
docs/prompt-packs/
  _PREAMBLE.prompt.md
  _SCHEMA_REGISTRY.md
  _COVERAGE_REGISTRY.md
  README.md
  01_PROJECT_BOOTSTRAP.prompt.md
  ...
  NN_HARDENING_BACKLOG_SWEEP.prompt.md
```

## Required Sections

Every feature pack contains sections 1-12, followed by a reference to the shared preamble.

1. Milestone ID
2. Context Snapshot
3. Spec References
4. Objective
5. Non-Goals
6. Stack Constraints
7. Required Deliverables
8. Integration Wiring Checklist
9. Documentation Requirements
10. Testing Requirements
11. Failure Modes
12. Acceptance Criteria
13-18. Shared Preamble Reference

## Section Rules

- Section 2 lists prior packs as complete and names consumed schema objects from `_SCHEMA_REGISTRY.md`.
- Section 3 uses full repo-relative spec paths in backticks.
- Section 5 gives explicit non-goals with named future homes when deferred.
- Section 7 lists concrete files and persistent objects the pack owns.
- Section 8 lists export/caller/grep-pattern wiring rows.
- Section 10 names unit, integration, state-matrix, and interleaving tests as needed.
- Section 11 lists failure modes for outbound fetches, workers, webhooks, imports, file handling, stateful protocols, and external side effects. Pure UI or type-only packs may include a one-line N/A justification.
- Section 12 restates acceptance criteria including failure-mode and state-matrix obligations.

## Context Budget

Split any pack that exceeds any limit:

- more than 12 new files
- more than 8 expected commits
- more than 4 spec references
- more than 200 lines excluding the preamble reference

## Final Pack

Always generate a final `NN_HARDENING_BACKLOG_SWEEP.prompt.md` pack. It reads `docs/dev/backlog.md` and, if present, `docs/dev/ideas.md`. It triages open backlog entries as build-now, won't-build, or re-defer-with-named-home. It presents ideas for user product decisions before building any accepted idea.

## Generator Self-Audit

Before reporting success:

- Confirm every pack has sections 1-12 in order.
- Confirm `_PREAMBLE.prompt.md`, `_SCHEMA_REGISTRY.md`, and `_COVERAGE_REGISTRY.md` exist when applicable.
- Confirm every pack is within the context budget.
- Confirm every section 8 library export has a production caller row.
- Confirm every populated section 11 row has a matching section 12 acceptance criterion.
- Confirm README lists packs in execution order.
- Confirm deferral chains terminate in an accepting pack or a coverage-registry/backlog entry.
- Confirm no example-only identifiers were copied into packs unless they exist in the target project.

