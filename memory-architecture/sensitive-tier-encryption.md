# Phase 7 — Sensitive Tier Design + Encryption Approach

This document defines how OpenClaw memory should handle **sensitive** information in a way that is:
- local-first
- encrypted at rest
- excluded from default injection + broad retrieval
- auditable (receipts) without leaking content

---

## Problem statement
Some user-provided details are legitimately useful but too sensitive to store in plain Markdown that may be:
- always-loaded (T0)
- routinely retrieved/snippeted (T2/T3/T4)
- indexed for semantic search (embeddings)

Examples:
- API keys / tokens / passwords
- medical or financial data
- private addresses
- information that should not be surfaced in group chats

---

## Tier model: add **T-S (Sensitive)**

Introduce a dedicated tier:
- **T‑S: Sensitive memory (encrypted)**

Properties:
- Not part of T0–T4.
- Not indexed by default.
- Not injected by default.
- Access requires explicit intent and explicit tool flow.

Filesystem layout (proposal):
- `memory/sensitive/` (contains encrypted blobs only)
- `memory/sensitive/index.json` (optional, contains *non-sensitive metadata only*)

---

## Storage format

### Canonical content: encrypted Markdown
- Each sensitive note stored as an encrypted file:
  - `memory/sensitive/<yyyy>/<mm>/<id>.md.age` (or `.gpg` depending on tool)

The plaintext is Markdown following the same schemas (semantic/procedural/episodic), but is never written unencrypted.

### Metadata index (non-sensitive)
Optional index file in plaintext:
- `memory/sensitive/index.json`

Allowed fields:
- id
- created_at
- tags (non-sensitive)
- redacted description (safe)
- encryption scheme (age/gpg)

Forbidden fields:
- raw secrets
- full freeform text

---

## Encryption approach

### Preferred: `age` (simple, modern)
- Encrypt with recipient public key(s) or a passphrase.
- Good UX for file-based encryption.

Key management options:
1) **Recipient keys (recommended)**
   - Store recipients list in config or a local file readable only to the user.
   - Allows rotation and multi-device without sharing passphrases.

2) **Passphrase mode (fallback)**
   - Easier to start.
   - Requires careful handling to avoid passphrase exposure.

### Alternative: GPG
- Widely available.
- More complex UX.

---

## Retrieval + injection rules

### Default behavior
- T‑S is **never** included in:
  - default injection sets
  - `memory_search` indexing inputs
  - routine retrieval

### Explicit access flow (future implementation)
To use sensitive memory, require:
1) user explicitly requests it (e.g., "use my API key" is NOT enough; they must confirm they want it stored/used)
2) agent decrypts locally (tooling) into ephemeral memory
3) agent uses it for the immediate task
4) plaintext is not persisted to disk

### Group chat constraint
Even if sensitive memory is accessed, it must never be surfaced in group contexts.

---

## Indexing constraints (embeddings)
Sensitive plaintext must not be embedded remotely.

Rules:
- No vectorization of decrypted sensitive text.
- If we ever support local-only embeddings for sensitive tier, it must be opt-in and still excluded from general search.

---

## Auditability (without leakage)
Every sensitive write produces a receipt (safe metadata only):
- source: where it came from (session key + timestamp)
- dest: encrypted file path
- plaintext hash (sha256 of plaintext) recorded **only as hash**
- encryption scheme + recipients fingerprint(s)

Receipt location (proposal):
- `memory/sensitive/receipts/<yyyy-mm>.jsonl`

---

## Operational guidance (human-facing)
- If the user provides secrets, do not store them in T0–T4.
- Offer T‑S storage only when the user requests it.
- Prefer storing *procedures that reference where to find a secret* (e.g., "token stored in 1Password") in T3/T4 rather than storing the secret itself.

---

## Implementation deferred
This project milestone defines the design.
Actual implementation requires:
- selecting an encryption tool available on the host (age/gpg)
- adding config options
- adding a safe decrypt/use flow
- adding tests that verify: no plaintext leaks, no indexing of sensitive tier
