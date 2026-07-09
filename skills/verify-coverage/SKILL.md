---
name: verify-coverage
description: Audit spec-to-pack ownership coverage. Use after prompt-pack generation, after material spec changes, or at phase boundaries to find spec capabilities with no owning prompt pack or no verified deferred home.
---

# Verify Coverage

Audit specs to prompt packs. This catches capabilities that no pack owns, which pack-scoped verification cannot see.

## Workflow

1. Locate prompt packs using the standard pack search order.
2. Locate specs from pack Section 3 references, `docs/specs/`, roadmap files, and `AGENTS.md`.
3. Read `docs/dev/backlog.md` if present so already tracked gaps are classified as tracked.
4. Build a spec-side capability inventory:
   - pages and nav nodes
   - end-to-end workflows
   - entity state machines
   - module behaviors and engines
   - concrete NFRs
   - mandatory cross-cutting items such as auth screens, account lifecycle, app shell, search, notifications, settings, audit logs, permissions, public rate limits, backups, observability, and legal/consent pages
5. Resolve each capability to exactly one verdict:
   - OWNED
   - DEFERRED with verified named home
   - TRACKED in backlog
   - PARTIAL
   - ORPHANED
6. Walk every pack deferral chain to its terminus. A deferral only counts if the target pack accepts the scope.
7. Adversarially re-check every PARTIAL or ORPHANED finding with extra grep variants and plausible owner pack reads.
8. Update `_COVERAGE_REGISTRY.md` and backlog confirmed PARTIAL/ORPHANED findings.

## Subagents

For large corpora, explicitly spawn read-only subagents by spec area. Read `references/subagent-prompts.md` for the packaged coverage-auditor prompt. Ask subagents to return capability inventories with cited pack evidence. Re-check their orphan claims in the main thread before reporting.

## Output

End with:

```text
RESULT: pass|fail|blocked
PHASE: verify-coverage
CAPABILITIES: <count>
OWNED: <count>
DEFERRED: <count>
TRACKED: <count>
PARTIAL: <count>
ORPHANED: <count>
BACKLOG_ADDED: <comma-separated ids or none>
```
