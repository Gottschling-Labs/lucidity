# Memory Schemas (Episodic, Semantic, Procedural)

Goal: make memory entries consistent, easy to search, easy to compress, and safe to inject.

## Naming conventions

### Files
- Daily logs (T2): `memory/YYYY-MM-DD.md` (append-only)
- Topic briefs (T3): `memory/topics/<topic>.md`
- Archive (T4): `MEMORY.md` plus optional `memory/archive/<year>/<topic>.md`

### IDs
When you need a stable handle inside a file, use:
- `id: <yyyy-mm-dd>-<short-slug>`

Example: `id: 2026-02-19-telegram-token-fix`

## Multi-type model

### Episodic memory (what happened)
**Where it lives**: primarily T2 (daily logs), sometimes distilled into T3.

**Template**
```md
## <timestamp> <short title>

- type: episodic
- id: <id>
- context: <project/system>
- summary: <1-2 lines>
- outcome: <what changed>
- artifacts:
  - <links to PRs, commits, files>
- followups:
  - <next actions>
```

**Rules**
- Keep it factual.
- Link to artifacts.
- Avoid long conversation transcripts.

---

### Semantic memory (what is true)
**Where it lives**: T4 (curated) and T3 (topic briefs). Avoid cluttering T0.

**Template**
```md
## <fact title>

- type: semantic
- id: <id>
- confidence: high|medium|low
- scope: personal|project|system
- statement: <the fact in one sentence>
- evidence:
  - <source paths and dates>
- last_verified: <yyyy-mm-dd>
```

**Rules**
- One fact per entry.
- Confidence must be explicit.
- Include evidence links back to T2 or source docs.

---

### Procedural memory (how to do a thing)
**Where it lives**: T3 (topic briefs) and optionally T0 if it is a global safety rule.

**Template**
```md
## <procedure name>

- type: procedural
- id: <id>
- trigger: <when to use this>
- steps:
  1) <step>
  2) <step>
- guardrails:
  - <what not to do>
- verification:
  - <how to confirm it worked>
```

**Rules**
- Steps must be short and testable.
- Include verification.

## Injection guidance (high level)
- Inject semantic facts when confidence is high and scope matches.
- Inject procedures only when the trigger matches.
- Episodic entries are normally retrieved, not injected wholesale.
