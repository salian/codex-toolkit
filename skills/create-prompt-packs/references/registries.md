# Prompt-Pack Registries

## Schema Registry

Path: `docs/prompt-packs/_SCHEMA_REGISTRY.md`

Create the schema registry for projects with persistent storage. It records one row per table, enum, shared reference table, or other persistent schema object.

Columns:

```text
| object concept | kind | owner pack | canonical name | one-line shape | consumer packs |
```

Rules:

- One owner per object.
- Domain-prefix generic or collision-prone names.
- Consumers must use the canonical name verbatim.
- A downstream pack extends an owned object; it does not re-declare it.
- Built code wins during retrofit; route risky renames to backlog.

## Coverage Registry

Path: `docs/prompt-packs/_COVERAGE_REGISTRY.md`

Create the coverage registry from the spec side, not by summarizing packs.

Columns:

```text
| capability | spec ref | kind | phase | owner pack(s) | status | notes |
```

Inventory:

- pages/screens
- workflows
- state machines
- engines and background behaviors
- concrete NFRs
- cross-cutting obligations such as auth screens, account lifecycle, app shell, search, notifications, settings, audit logs, permissions, rate limits, backups, observability, and legal/consent pages

Statuses:

- `owned`: names an existing pack.
- `DEFERRED`: names a future home and backlog entry.
- No blank status is allowed.

## Backlog and Ideas

Use `docs/dev/backlog.md` for spec'd-but-deferred obligations.

Use `docs/dev/ideas.md` for unspecced suggestions that need user product triage.

Never build directly from `ideas.md`.

