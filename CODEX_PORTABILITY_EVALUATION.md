# Claude Toolkit to Codex Portability Evaluation

Evaluation date: 2026-07-09

Source toolkit: `/Volumes/1TB Samsung PSSD T7 Media/Dropbox/Projects/common/claude-toolkit`

Target toolkit: `/Volumes/1TB Samsung PSSD T7 Media/Dropbox/Projects/common/codex-toolkit`

## Executive Summary

The Claude toolkit is not directly transferable to Codex as-is. The underlying process is highly transferable, but the implementation format is Claude Code-specific.

The right Codex target is not a one-to-one copy of `commands/*.md`. It should be a Codex-native toolkit built around:

- Agent skills in `.agents/skills/`
- `AGENTS.md` for persistent repo instructions
- Optional `.codex/agents/` custom agents for parallel review/audit roles
- Optional `.codex/hooks.json` or `.codex/config.toml` hooks for deterministic validation
- Optional plugin packaging through `.codex-plugin/plugin.json` when the workflow is ready to distribute

Recommendation: maintain a separate `codex-toolkit` repository, but treat it as a Codex-native port, not a mirror. The workflow concepts should stay aligned with `claude-toolkit`, but the files, invocation model, state handling, and orchestration should be rewritten for Codex.

## Source Workflow Being Ported

The Claude toolkit currently implements this process:

1. Convert available spec files into prompt packs.
2. Build prompt packs.
3. Verify:
   - build completeness
   - integration wiring
   - spec-to-pack coverage
4. Run an external review step through Codex.

That process remains valid for Codex. What changes is the delivery mechanism.

## A. Are These Directly Transferable to Codex?

No, not directly.

The command bodies contain valuable process knowledge, but the artifacts rely on Claude Code conventions:

- `commands/<name>.md` slash command files
- Claude frontmatter such as `allowed-tools`
- `$ARGUMENTS` command expansion in Claude's command model
- `CLAUDE.md` as the durable project instruction surface
- `.claude/` state and settings paths
- references to Claude-specific tools such as `Task`, `Agent`, `TodoWrite`, and invoking other slash commands through the Skill tool
- a Claude-centric plugin layout under `.claude-plugin/`

Codex has different native surfaces:

- Skills live in `.agents/skills/<skill-name>/SKILL.md` for repo-local workflows, or `$HOME/.agents/skills` for user-local workflows.
- `AGENTS.md` is the persistent project guidance file Codex reads before doing work.
- Custom prompts exist, but are deprecated in favor of skills.
- Plugins are the distribution unit for reusable Codex skills and integrations.
- Hooks and custom agents are Codex-native ways to enforce lifecycle checks and delegate specialized work.

So the current Claude command files are best treated as source material for a Codex port, not as files to copy into Codex.

## B. Recommended Changes for a Codex Transfer

### 1. Convert Commands into Codex Skills

Each major Claude command should become a Codex skill directory:

```text
.agents/
  skills/
    create-prompt-packs/
      SKILL.md
      references/
        prompt-pack-format.md
        schema-registry.md
        coverage-registry.md
    build-prompt-pack/
      SKILL.md
      references/
        preflight-touchpoints.md
        execution-loop.md
    verify-build/
      SKILL.md
    verify-wiring/
      SKILL.md
    verify-coverage/
      SKILL.md
    review-changes/
      SKILL.md
    build-verify-review/
      SKILL.md
```

Codex skills support progressive disclosure, so long procedures should move out of `SKILL.md` into reference files. The skill should load only the references required for the current phase.

### 2. Replace Claude Slash-Command Assumptions

Do not port `/build`, `/verify-build`, `/verify-wiring`, etc. as Codex custom prompts. Codex custom prompts are deprecated; skills are the recommended reusable workflow mechanism.

Use explicit skill invocation instead:

```text
$create-prompt-packs docs/specs/
$build-prompt-pack M12
$verify-build M12
$verify-wiring M12
$verify-coverage
$build-verify-review
```

The exact UI may vary by Codex surface, but the workflow should be authored as skills, not deprecated custom prompts.

### 3. Replace `CLAUDE.md` with `AGENTS.md`

All generated or injected project guidance should target `AGENTS.md`, not `CLAUDE.md`.

Mapping:

| Claude toolkit concept | Codex-native equivalent |
|---|---|
| `CLAUDE.md` | `AGENTS.md` |
| `.claude/commands/*.md` | `.agents/skills/*/SKILL.md` |
| `.claude-plugin/` | `.codex-plugin/` |
| Claude skill auto-trigger descriptions | Codex skill `description` |
| Claude command `$ARGUMENTS` | Codex skill prompt arguments / user prompt context |
| Claude subagent/task usage | Codex subagents or custom agents |
| Claude permission frontmatter | Codex sandbox, approvals, hooks, and config |

### 4. Rewrite Tool and Permission Assumptions

Claude `allowed-tools` frontmatter should not be carried over mechanically.

Codex uses sandboxing, approval policy, hooks, config, and plugin trust differently. A Codex port should express safety as:

- clear instructions in skills
- project-level `AGENTS.md` rules
- optional hooks for deterministic blocking or validation
- optional custom agents with constrained instructions for read-heavy audits
- user/session approval policy rather than broad preapproved tool lists

### 5. Add Machine-Readable Phase Outputs

The orchestrator should not rely on prose like "Gaps Found: N".

Each Codex verifier skill should end with a stable trailer:

```text
RESULT: pass
PHASE: verify-wiring
PACK: 12_LEAD_CAPTURE
GAPS: 0
ADVISORY: 3
BACKLOG_ADDED: B12,B13
IDEAS_ADDED: I4
```

The `build-verify-review` skill should make loop decisions from these trailers.

### 6. Make State Files Codex-Native but Tool-Agnostic

Avoid `.claude/` paths in Codex.

Recommended Codex-side paths:

```text
.codex/prompt-pipeline/state.json
.codex/prompt-pipeline/answers.md
docs/dev/backlog.md
docs/dev/ideas.md
docs/prompt-packs/_SCHEMA_REGISTRY.md
docs/prompt-packs/_COVERAGE_REGISTRY.md
```

Keep the durable project artifacts (`docs/dev`, `docs/prompt-packs`) tool-neutral where possible. Keep runtime state under `.codex/`.

### 7. Use Codex Subagents for Read-Heavy Verification

The Claude toolkit already delegates large audits to subagents. Codex supports subagent workflows explicitly, but Codex only spawns subagents when asked.

Good Codex-native split:

- `coverage-inventory-agent`: reads specs and inventories capabilities
- `pack-ownership-agent`: maps capabilities to prompt packs
- `wiring-audit-agent`: checks reachability and caller chains
- `review-agent`: reviews changed code for correctness/security/test gaps

Keep write-heavy implementation in the main agent or a single worker to avoid edit conflicts.

### 8. Replace External Codex Review with Native Codex Review Modes

In Claude, Codex is an external reviewer. In Codex, the review phase should not shell out to Codex by default.

Recommended Codex behavior:

- For local worktree review, use Codex's native review behavior or a `review-changes` skill.
- For GitHub PR review, rely on Codex code review integration when available.
- Keep a fallback shell-based review only for cases where a separate Codex CLI invocation is intentionally desired.

The Codex port should rename `review-externally` to something like `review-changes` or `independent-review`.

### 9. Package as a Plugin Only After the Skills Stabilize

Start with repo-local skills while iterating:

```text
codex-toolkit/
  .agents/
    skills/
```

Once stable, package the toolkit as:

```text
codex-toolkit/
  .codex-plugin/
    plugin.json
  skills/
    create-prompt-packs/
    build-prompt-pack/
    verify-build/
    verify-wiring/
    verify-coverage/
    review-changes/
    build-verify-review/
```

Plugins are the right distribution unit when the workflow should be installed across repos or shared with a team.

## C. Should There Be a Parallel `codex-toolkit` Repository?

Yes.

The Codex version should be maintained separately because the core extension surfaces differ enough that a direct shared file tree would create constant compromise.

Recommended repository strategy:

```text
claude-toolkit/
  commands/
  skills/
  .claude-plugin/

codex-toolkit/
  .agents/
    skills/
  .codex/
    agents/
    hooks.json
  .codex-plugin/
  docs/
    design/
    migration-notes/
```

Keep the two repositories conceptually aligned, but implementation-specific:

- Shared concepts:
  - prompt-pack lifecycle
  - schema registry
  - coverage registry
  - backlog vs ideas ledger
  - build, verify, wiring, coverage, review gates
  - orchestrated run state
- Separate implementations:
  - invocation format
  - skill/command layout
  - persistent instruction files
  - plugin manifest format
  - subagent conventions
  - hook/config mechanisms

## Recommended Codex Toolkit Initial Scope

The first Codex-native version should not port everything at once.

Recommended phase 1:

1. `create-prompt-packs` skill
2. `build-prompt-pack` skill
3. `verify-build` skill
4. `verify-wiring` skill
5. `verify-coverage` skill
6. `review-changes` skill
7. `AGENTS.md` guidance template

Recommended phase 2:

1. `build-verify-review` orchestrator skill
2. `.codex/prompt-pipeline/state.json` schema
3. custom read-only audit agents
4. hooks for state/result validation
5. plugin packaging

Recommended phase 3:

1. migration assistant from `claude-toolkit`
2. automated conformance checks for skill metadata
3. shared test fixtures for prompt-pack generation and verification reports

## Proposed Codex Skill Mapping

| Claude command | Codex skill | Notes |
|---|---|---|
| `/create-prompt-packs` | `$create-prompt-packs` | Rewrite as skill with references for pack format, registry rules, UI guardrails. |
| `/build` | `$build-prompt-pack` | Avoid generic `build`; Codex already has many build/test conventions. |
| `/verify-build` | `$verify-build` | Keep mostly intact, add machine-readable trailer. |
| `/verify-wiring` | `$verify-wiring` | Keep checks A-F/G-L split, add Codex browser/tool fallback wording. |
| `/verify-coverage` | `$verify-coverage` | Strong candidate for subagent fanout. |
| `/review-externally` | `$review-changes` | In Codex, review is native, not external. |
| `/build-verify-review` | `$build-verify-review` | Rebuild around result trailers and `.codex/prompt-pipeline/state.json`. |
| `/self-improvement-loop` | `$install-project-guidance` | Target `AGENTS.md`, not `CLAUDE.md`. |
| `/smart-commit` | `$smart-commit` | Port as smaller skill; no Claude-specific permissions. |
| `/changelog` | `$update-changelog` | Port directly as simple skill. |
| `/retrofit-pipeline-gates` | `$retrofit-pipeline-gates` | Port later after core artifacts stabilize. |

## Decision

Create and maintain a parallel `codex-toolkit`.

Do not copy the Claude command files directly. Use them as source specifications for Codex-native skills. The port should preserve the process discipline while adopting Codex's actual extension model: skills first, `AGENTS.md` for durable guidance, subagents for read-heavy decomposition/audits, hooks for deterministic lifecycle checks, and plugins only when distribution is needed.

## Official Codex References Used

- Agent Skills: https://developers.openai.com/codex/skills
- Custom instructions with `AGENTS.md`: https://developers.openai.com/codex/guides/agents-md
- Custom Prompts: https://developers.openai.com/codex/custom-prompts
- Plugins: https://developers.openai.com/codex/plugins
- Build Plugins: https://developers.openai.com/codex/plugins/build
- Hooks: https://developers.openai.com/codex/hooks
- Subagents: https://developers.openai.com/codex/subagents
- Slash commands in Codex CLI: https://developers.openai.com/codex/cli/slash-commands

