# Lucidity ↔ Anima interface (draft)

This document defines the **boundary** between Lucidity and a future portable identity layer such as Anima.

## Intent

- **Lucidity** owns local memory operations: distill, dedupe, apply, backup, rollback, and retrieval hygiene.
- **Anima** owns portable companion essence: identity, persona, durable preferences, portability metadata, and restore/import expectations.

The goal is to let a companion survive host loss **without** pretending every runtime detail is portable.

## Separation of concerns

### Lucidity owns
- local Markdown memory corpus under a workspace
- staging-first maintenance pipeline
- receipts/manifests for auditability
- backup + rollback flows
- retrieval policy and memory hygiene
- profile-driven guidance for retrieval/runtime constraints

### Anima owns
- portable identity bundle / essence package
- persona and identity metadata
- durable preference export/import
- references to a Lucidity workspace or exported memory snapshot
- restore semantics when rehydrating on a new host

## Proposed contract

An Anima bundle should be able to carry:
- identity files (`SOUL.md`, `IDENTITY.md`, `USER.md` or equivalents)
- selected curated memory (`MEMORY.md`)
- optional topic briefs / procedural notes
- portability metadata
- a pointer to a full Lucidity workspace backup when available
- optional profile hints for target runtime/retrieval behavior

Lucidity should be able to consume:
- a restored workspace root
- imported curated files
- profile hints that shape retrieval posture
- optional migration metadata describing source host/runtime

## Non-goals

Anima should **not** require Lucidity to export:
- raw ephemeral session state
- provider-specific hidden memory
- exact model weights or host-bound runtime internals
- every transient cache/artifact

Those may be useful operationally, but they are not the companion's essential continuity.

## Minimal portability model

A practical first version of portability is:

1. Preserve identity files
2. Preserve curated long-term memory
3. Preserve topic/procedural notes when useful
4. Preserve receipts/manifests and backup metadata
5. Reattach on a new host
6. Rebuild indexes locally

That gives continuity of **essence + memory** even if the runtime stack changes.

## Profile hints

Anima may optionally declare profile hints such as:
- `runtimeProfile`: `openclaw-default`, `llama-local-8k`, `offline-voice-low-latency`
- `retrievalProfile`: `balanced`, `compact`, `latency-first`

Lucidity treats these as **hints**, not hard guarantees.

## Suggested future manifest fields

```json
{
  "animaVersion": 1,
  "identity": {
    "name": "Gordon"
  },
  "lucidity": {
    "workspaceLayout": "openclaw-markdown-v1",
    "curatedMemory": ["MEMORY.md"],
    "topicDirs": ["memory/topics"],
    "backupRef": "backups/latest.json"
  },
  "profiles": {
    "runtimeProfile": "openclaw-default",
    "retrievalProfile": "balanced"
  }
}
```

## Near-term implementation guidance

Before Anima exists as a formal spec/project, Lucidity should:
- keep Markdown as the source of truth
- make backups/restores deterministic and documented
- expose profile examples without locking into a rigid runtime abstraction
- keep the portability boundary explicit in docs

That preserves flexibility while still making future companion migration realistic.
