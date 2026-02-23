# Tier Transition Rules (Thresholds + Promotion/Demotion)

This document defines *when* information moves between tiers (T0-T4) and how it is kept compact, auditable, and safe.

Design goals:
- Keep always-loaded content small.
- Prefer retrieval over injection.
- Never lose data: every transform must cite sources.
- Promote only what stays true or keeps paying rent.

---

## Config knobs (defaults)

These are intended as config values later (env/config). For now, treat as project defaults.

- **T0 max size (soft)**: 20 KB per file (SOUL/USER/IDENTITY/AGENTS/TOOLS)
- **T1 max injection budget (soft)**: 1,000 tokens combined
- **T2 daily log max (soft)**: 150 KB per day before prompting distillation
- **T3 topic brief max**: 30 KB per topic file
- **T4 curated max**: 80 KB total before requiring pruning into archive

Time thresholds:
- **T1 decay**: items older than 14 days should be removed or moved to T3/T4 (unless actively referenced)
- **T3 refresh**: if a topic hasn’t been referenced in 90 days, mark it "stale" and consider archiving to T4 archive

Recall thresholds (tracked via retrieval logs later):
- **Promote to T3**: referenced/retrieved ≥3 times in 30 days OR required for an active project
- **Promote to T4**: still true + referenced ≥5 times across ≥60 days OR explicitly designated as durable by human
- **Demote from T4**: confidence drops to low OR not referenced in 180 days (move to archive or topic)

---

## Promotion rules

### T1 → T2 (working context → daily log)
**Trigger**: end of day (or when a task closes) and the content is episodic (what happened).

**Action**: append a short episodic entry to `memory/YYYY-MM-DD.md`.

**Receipt requirement**: include artifact links and/or file paths.

---

### T2 → T3 (daily log → topic brief)
**Trigger** (any):
- A repeated concept shows up across ≥2 days, or
- A procedure is used more than once, or
- A project decision impacts future work.

**Action**:
- Create/update `memory/topics/<topic>.md` with:
  - semantic facts (confidence + evidence)
  - procedures (trigger + verification)
  - short "what changed" notes

**Compression**:
- Prefer bullet lists.
- Strip timestamps unless they matter.
- Keep direct quotes out; summarize.

**Receipt requirement**:
- Add `evidence:` links back to the originating T2 entries (date + heading).

---

### T3 → T4 (topic brief → curated long-term)
**Trigger**:
- Fact remains true over time and useful across contexts, or
- Preference is stable and user-affecting, or
- Safety/operating constraint should persist.

**Action**:
- Add to `MEMORY.md` as a semantic entry (or incorporate into an existing section).

**Constraints**:
- Only high-confidence statements.
- Must include evidence.

---

### T4 → T0 (curated → foundational)
**Trigger**: only when the information is required *nearly every run* (identity, tone, safety rails) and is not sensitive.

**Action**:
- Update `SOUL.md` / `USER.md` / `IDENTITY.md` / `AGENTS.md` / `TOOLS.md`.

**Rule**:
- T0 is *not* a dumping ground. If it’s not needed constantly, keep it in T4 and retrieve when needed.

---

## Demotion / pruning rules

### T1 pruning
**Trigger**: items older than 14 days and not referenced in the last 7 days.

**Action**:
- If episodic: ensure logged in T2, then delete from T1.
- If procedural/semantic: promote to T3/T4 first, then delete from T1.

---

### T3 pruning
**Trigger**: topic file > 30 KB OR has sections not referenced in 90 days.

**Action**:
- Split into subtopics (`<topic>-<subtopic>.md`) OR move older sections to `memory/archive/<year>/<topic>.md`.

**Receipt**:
- Keep an "Archive map" section listing what moved where.

---

### T4 pruning (curated)
**Trigger**: `MEMORY.md` exceeds 80 KB OR becomes hard to scan.

**Action**:
- Move older, less frequently used sections to `memory/archive/<year>/<topic>.md`.
- Keep a short pointer in `MEMORY.md`.

---

## Sensitive data rules (forward-compatible)

Until an encrypted tier exists:
- Do not store secrets in any tier.
- If the user provides secrets, keep them out of files and instead ask for a secure channel/process.

When an encrypted sensitive tier is implemented later:
- Sensitive memory becomes **T-S (Sensitive)**, excluded from default injection and from broad search.
- Access requires explicit tool flow and redaction-by-default.

---

## Examples

- "Brandon prefers being called Brando": likely T4; only move to T0 (USER.md) if it’s stable and always relevant.
- "The cron tool requires sessionTarget=isolated for agentTurn": procedural → T3 topic brief.
- "We restarted OpenClaw due to config.patch": episodic → T2, maybe distilled into T3 ops topic.
