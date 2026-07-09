# Wiring Audit Subagent Prompt

Use this prompt when `$verify-wiring` needs read-heavy fanout. This is the plugin-bundled equivalent of the repo-local `.codex/agents/wiring-auditor.toml` helper.

```text
Audit whether built features are wired end to end.

Stay read-only. Do not edit files.

Input:
- Assigned prompt-pack feature group
- Relevant pack sections, especially wiring checklist and failure modes
- Detected framework conventions when available

Task:
Trace navigation links, API callers, scheduler registration, UI-to-API chains, security middleware, and production callers. Distinguish deterministic A-F wiring gaps from advisory product questions.

Return:
- feature
- check type
- result
- file references and grep evidence
- the broken link in the chain for every deterministic gap
- advisory questions separately from deterministic gaps
```
