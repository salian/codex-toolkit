---
name: verify-wiring
description: Audit whether prompt-pack features are wired end to end. Use after verify-build to check navigation reachability, API callers, scheduler registration, UI-to-API chains, security middleware, production callers, and advisory product gaps.
---

# Verify Wiring

Audit whether built features are reachable and connected end to end.

## Workflow

1. Locate and read the prompt pack, referenced specs, `AGENTS.md`, and project configs.
2. Detect framework conventions for pages, routes, API handlers, jobs, middleware, navigation, and tests.
3. Build the feature inventory from:
   - the pack's wiring checklist
   - Section 11 mitigation functions
   - user-facing and system-facing features in the pack and specs
4. Run deterministic wiring checks:
   - A: page navigation reachability
   - B: API/webhook caller reachability
   - C: scheduler/job registration
   - D: UI-to-API completeness, including auth, CSRF, validation, and side effects
   - E: production caller detection for library functions
   - F: browser/runtime spot-check when a dev server or browser tool is available
5. Run advisory product-gap checks separately:
   - sibling parity
   - CRUD/lifecycle completeness
   - cross-cutting concerns
   - user journey reachability
   - failure-mode coverage
   - spec-vs-product drift
6. Persist real advisory obligations to `docs/dev/backlog.md` and unspecced suggestions to `docs/dev/ideas.md`.

## Subagents

For large packs or broad UI/API surfaces, explicitly spawn read-only subagents by feature group. Read `references/subagent-prompts.md` for the packaged wiring-auditor prompt. Re-check every deterministic gap in the main thread before reporting.

## Rules

- Checks A-F are failures when broken.
- Advisory findings are not build failures and must not trigger an orchestrator retry.
- Test imports do not count as production callers.
- Missing required security middleware is a wiring gap.
- Do not auto-fix advisory findings.

## Output

End with:

```text
RESULT: pass|fail|blocked
PHASE: verify-wiring
PACK: <pack-id>
GAPS: <count for checks A-F>
ADVISORY: <count for advisory findings>
BACKLOG_ADDED: <comma-separated ids or none>
IDEAS_ADDED: <comma-separated ids or none>
```
