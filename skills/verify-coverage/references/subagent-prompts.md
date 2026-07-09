# Coverage Audit Subagent Prompt

Use this prompt when `$verify-coverage` needs read-heavy fanout. This is the plugin-bundled equivalent of the repo-local `.codex/agents/coverage-auditor.toml` helper.

```text
Audit specs against prompt packs.

Stay read-only. Do not edit files.

Input:
- Assigned spec files or spec sections
- Prompt-pack directory
- Existing backlog Open titles, if available
- Verdict definitions: OWNED, DEFERRED, TRACKED, PARTIAL, ORPHANED

Task:
Build a spec-side inventory of capabilities from the assigned specs, then map each capability to prompt-pack evidence. Treat grep hits as candidates only; read the candidate pack section before assigning ownership.

Return:
- capability
- spec reference
- verdict
- owner pack or deferred home
- evidence with file path and section/line when possible
- grep patterns tried for any possible PARTIAL or ORPHANED finding

Flag possible orphan and partial findings, but do not treat them as final. The parent agent will adversarially re-check them.
```
