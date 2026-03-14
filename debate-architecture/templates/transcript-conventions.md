# Debate Architecture — Transcript Conventions (v0)

This document defines **filenames, schemas, and redaction rules** for debate runs.

## File naming

Run folder:
- `debate-architecture/runs/<runId>/`

Round folders:
- `round-01/`, `round-02/`, … `round-0N/`

Role outputs (lowercase, hyphenated):
- `proponent.md`
- `critic.md`
- `fact-checker.md`
- `executor.md`
- `judge.md` (optional)

Orchestrator artifacts:
- `round-XX/synthesis.md` (round synthesis)
- `consensus.md` (final)
- `inputs.md` (sanitized task + constraints)
- `meta.json`
- `trace.jsonl`
- `redaction.md` (if redaction enabled)

## Required frontmatter

All Markdown artifacts saved under a run MUST include frontmatter:

```yaml
---
role: proponent|critic|fact-checker|executor|judge|orchestrator
run_id: <runId>
round: <int|null>
created_at: <ISO-8601>
model: <string>
---
```

- `round` may be `null` for `inputs.md`, `meta.json` (not md), or final `consensus.md` (if desired).

## Transcript schema expectations

Role output sections (recommended):
- `# Summary`
- `# Key Points`
- `# Evidence / Citations`
- `# Risks / Unknowns`
- `# Questions for other roles`

Citations format:
- Prefer:
  - `https://...` (web)
  - `/abs/path/to/file.md#L120-L140` (local)
  - `Source: <path#line>` (OpenClaw memory snippets)

If a claim cannot be cited:
- Mark as **uncertain**.

## Redaction rules (default on “unknown sensitivity” tasks)

### What to redact
Replace sensitive strings with typed placeholders:
- Email → `[REDACTED:EMAIL]`
- Phone → `[REDACTED:PHONE]`
- API keys/tokens → `[REDACTED:SECRET]`
- Addresses → `[REDACTED:ADDRESS]`
- Names (if required) → `[REDACTED:NAME]`

### Where redaction happens
- `inputs.md` is the *primary* redaction target before anything is sent to role sessions.
- Role outputs may contain additional redactions if roles inadvertently echo sensitive strings.

### Redaction ledger
If redaction is enabled:
- Write `redaction.md` containing:
  - what placeholder types were used
  - count of replacements per type
  - *no raw secrets* (never store the original values here)

### Safety invariants
- Never send `redaction.md` content into other sessions.
- Never store plaintext secrets in debate traces.
- If encryption is enabled, encrypt the whole run folder after completion.
