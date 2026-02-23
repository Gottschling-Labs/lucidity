# Tiered Memory Design (T0 to T4)

Goal: keep memory local-first, auditable, and cheap by default while still enabling deep recall when needed.

## Tier overview

### T0: Foundation (always-loaded)
**Purpose**: stable identity and operating constraints that should be present in nearly every run.

**Contents**
- Identity and tone
- Safety rails
- User preferences that change rarely
- High-level mission and operating rules

**Files (source of truth)**
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `AGENTS.md`
- `TOOLS.md`

**Notes**
- Keep this small and stable.
- No secrets.

---

### T1: Working context (session-scoped)
**Purpose**: what we are actively doing right now.

**Contents**
- Current goals
- Active tasks and decisions
- Short-lived context

**Files (source of truth)**
- `HEARTBEAT.md`
- `NIGHTSHIFT.md`
- `request-queue.md`
- Optional: `workspace/state/*.json` for small structured state

**Notes**
- This tier should decay quickly.
- Prefer structured state for counters and timestamps.

---

### T2: Daily logs (append-only, uncompressed)
**Purpose**: raw episodic record of what happened.

**Contents**
- Events, decisions, and outcomes
- Links to artifacts (PRs, commits, notes)

**Files (source of truth)**
- `memory/YYYY-MM-DD.md`

**Notes**
- Append-only.
- This is not "curated." It is the paper trail.

---

### T3: Topic briefs (compressed, short-term)
**Purpose**: keep useful, recent knowledge in a compact form without bloating T0 or T4.

**Contents**
- Distilled notes by topic, project, or system
- Updated as facts evolve

**Files (source of truth)**
- `memory/topics/<topic>.md`

**Suggested topics (initial)**
- `memory/topics/openclaw-setup.md`
- `memory/topics/ops-deck.md`
- `memory/topics/browser-and-research.md`
- `memory/topics/security-and-secrets.md`

**Notes**
- These are maintained documents.
- They should cite sources (paths and dates) back into T2.

---

### T4: Archive (compressed, long-term)
**Purpose**: long-term semantic memory that is stable and broadly useful.

**Contents**
- Facts and preferences that remain true
- Durable decisions
- Long-lived project context

**Files (source of truth)**
- `MEMORY.md`
- Optional: `memory/archive/<year>/<topic>.md`

**Notes**
- This tier should be small and high signal.
- Everything here should be true "for a long time."

## Access patterns
- Default prompt injection should prefer T0 plus a very small slice of T1.
- Retrieval (memory_search) should index T2, T3, and T4 and return snippets, not whole files.
- Human editable markdown remains the source of truth.

## Security constraints
- Secrets are never stored in T0, T3, or T4.
- If we later add a sensitive tier, it must be encrypted and excluded from default injection.
