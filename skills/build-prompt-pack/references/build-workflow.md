# Build Workflow

## Pre-Flight Touchpoints

Before implementation, inspect the pack and referenced specs for nouns and verbs that imply integration points outside the deliverable list.

Look for:

- background work: worker, handler, job, queue, scheduled, cron
- AI/LLM: model, prompt, embedding, completion
- external IO: webhook, publish, subscribe, connector
- delivery: deploy, migration, env var, secret, Docker, CI
- auth/access: auth, session, CSRF, permission, role, tenant
- surfacing: dashboard, nav, link, page, route, API
- observability: log, metric, analytics, telemetry
- state: migration, schema, seed, backfill

Grep the repo for the most relevant terms, then create a touchpoint checklist. Every item is either assigned to a build step or explicitly deferred to `docs/dev/backlog.md`.

## Sibling Write-Path Parity

When a new path writes to a shared persistent entity or repeats an existing operation, compare it to existing sibling write paths.

Check:

- quota or limit enforcement
- input validation
- authorization and tenancy
- compliance, suppression, PII, erasure, consent
- normalization and coercion
- idempotency and dedupe
- audit and observability

Any relevant missing guard is a build obligation unless explicitly deferred with a defensible reason.

## Stateful Protocol Sketch

Run this only for packs involving claim, lease, lock, cursor, checkpoint, retry, dedupe, state machine, concurrent, backfill, or external side effects.

Before coding, sketch:

- states and transitions
- invariants
- concurrency hazards
- crash/retry/replay behavior
- stale data behavior
- partial failure behavior
- external side-effect semantics
- blast-radius and alert behavior

Convert each invariant and hazard into a named test.

## Commit Discipline

- One logical change per commit.
- Tests ship with the code they test.
- Stage only relevant files.
- Update `CHANGELOG.md` for user-visible changes when the project uses one.
- Do not use `git add .`.

