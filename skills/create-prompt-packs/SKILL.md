---
name: create-prompt-packs
description: Generate executable prompt packs from project specs for Codex-driven implementation. Use when the user asks to decompose PRDs, roadmaps, AGENTS.md, design docs, or spec folders into milestone prompt-pack files under docs/prompt-packs/.
---

# Create Prompt Packs

Convert project specs into small, executable prompt packs that Codex can build one at a time.

## Workflow

1. Locate specs from the user prompt or by scanning likely files: `docs/specs/`, `docs/PRD*.md`, `docs/ROADMAP*.md`, `AGENTS.md`, and project-specific spec paths named in `AGENTS.md`.
2. Read `AGENTS.md` before writing packs. It is the Codex-side project law.
3. Red-team the specs before decomposition. Batch blocking questions for the user; fix clear spec defects in place; route minor deferred needs to `docs/dev/backlog.md`.
4. Decompose the work into milestone packs under `docs/prompt-packs/`.
5. Generate shared registries:
   - `_SCHEMA_REGISTRY.md` for persistent objects with exactly one owning pack.
   - `_COVERAGE_REGISTRY.md` for spec-to-pack ownership of buildable capabilities.
6. Generate `_PREAMBLE.prompt.md` for shared build discipline.
7. Generate a final hardening/backlog-sweep pack.
8. Run the generator self-audit from `references/prompt-pack-format.md` before reporting completion.

## Required Pack Properties

Each pack must be bounded enough for one Codex build session:

- no more than 12 new files
- no more than 8 expected commits
- no more than 4 spec references
- no more than 200 lines excluding the shared preamble reference

Split large milestones with letter suffixes such as `07a`, `07b`, and `07c`. Do not split a single feature across packs unless each pack leaves the project working.

## References

Read `references/prompt-pack-format.md` before writing pack files.

Read `references/registries.md` before creating or updating `_SCHEMA_REGISTRY.md` or `_COVERAGE_REGISTRY.md`.

## Output

End with:

```text
RESULT: pass|blocked
PHASE: create-prompt-packs
PACKS_CREATED: <count>
BLOCKING_QUESTIONS: <count>
BACKLOG_ADDED: <comma-separated ids or none>
```

