---
name: verify-build
description: Audit whether a prompt pack was completely built. Use after building a prompt pack to verify deliverable files, exports, tests, failure-mode mitigations, acceptance criteria, and registry-owned capabilities.
---

# Verify Build

Audit pack-to-code completeness. This answers: did the implementation build everything the pack and referenced specs require?

## Workflow

1. Locate the pack by id or path using the same normalization as `$build-prompt-pack`.
2. Read the pack, `AGENTS.md`, referenced specs, and `_COVERAGE_REGISTRY.md` if present.
3. Build an audit inventory from:
   - Section 7 deliverables
   - Section 10 tests
   - Section 11 failure modes
   - Section 12 acceptance criteria
   - coverage registry rows owned by this pack
   - referenced spec requirements not restated in the pack
4. Verify each file exists and implements the named behavior. Do not pass based on existence alone.
5. Verify tests exist, cover the specified scenarios, and run when feasible.
6. Verify failure-mode mitigations and their tests. Missing mitigation tests are build gaps.
7. Verify sibling write-path parity for new writes to shared persistent entities.
8. Report every gap with evidence and a concrete fix location.

## Rules

- Read the specs, not only the pack.
- Count partial implementations as gaps.
- Do not audit features the pack explicitly excludes, but backlog real future obligations with named homes.
- When invoked by `$build-verify-review`, do not ask whether to fix gaps; report them and end with the result trailer.

## Output

End with:

```text
RESULT: pass|fail|blocked
PHASE: verify-build
PACK: <pack-id>
GAPS: <count>
BACKLOG_ADDED: <comma-separated ids or none>
```

