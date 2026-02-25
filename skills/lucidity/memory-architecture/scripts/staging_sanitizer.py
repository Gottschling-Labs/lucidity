#!/usr/bin/env python3
"""Staging sanitizer utilities.

Purpose:
- Reduce prompt-injection risk by sanitizing untrusted excerpts stored in staging.

This is NOT a security boundary. It is a best-effort defense-in-depth measure.

Policy (v1):
- redact lines that look like prompt injection attempts or sensitive directives
- redact obvious secret-like patterns
- clamp quote length

The sanitizer should preserve enough context for human review while removing
imperative or credential-like content.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


DEFAULT_MAX_CHARS = 600

INJECTION_LINE_PATTERNS = [
    # common jailbreak / instruction override patterns
    r"(?i)^\s*(ignore|disregard)\s+(all|any|previous|prior)\s+(instructions|rules|prompts).*$",
    r"(?i)^\s*you\s+are\s+(now|a)\b.*$",
    r"(?i)^\s*system\s+prompt\s*:\s*.*$",
    r"(?i)^\s*developer\s+message\s*:\s*.*$",
    r"(?i)^\s*role\s*:\s*(system|developer)\b.*$",
    r"(?i)^\s*BEGIN\s+SYSTEM\s+PROMPT.*$",
    # dangerous imperative ops
    r"(?i)^\s*run\s+this\s+command\s*:\s*.*$",
    r"(?i)^\s*(rm\s+-rf|sudo\s+rm\s+-rf)\b.*$",
    r"(?i)^\s*(curl|wget)\b.*\|\s*(sh|bash)\b.*$",
    # exfil attempts
    r"(?i)^\s*(send|exfiltrate|upload)\b.*(secrets?|tokens?|keys?).*$",
]

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"AIza[0-9A-Za-z-_]{35}",
    r"xox[baprs]-[0-9A-Za-z-]{10,}",
    r"(?:^|\b)ghp_[0-9A-Za-z]{30,}",
    r"(?:^|\b)github_pat_[0-9A-Za-z_]{20,}",
    r"sk-[0-9A-Za-z]{20,}",
    r"(?i)password\s*[:=]\s*\S+",
    r"(?i)api[_ -]?key\s*[:=]\s*\S+",
    r"(?i)secret\s*[:=]\s*\S+",
    r"(?i)token\s*[:=]\s*\S+",
]


@dataclass
class SanitizeResult:
    text: str
    redacted_lines: int
    redacted_secrets: int
    truncated: bool


def sanitize_evidence_quote(text: str, max_chars: int = DEFAULT_MAX_CHARS) -> SanitizeResult:
    redacted_lines = 0
    redacted_secrets = 0

    lines = text.splitlines()
    out_lines = []

    inj_res = [re.compile(p) for p in INJECTION_LINE_PATTERNS]
    sec_res = [re.compile(p) for p in SECRET_PATTERNS]

    for ln in lines:
        # redact injection-like lines
        if any(r.search(ln) for r in inj_res):
            out_lines.append("[REDACTED: potential prompt injection line]")
            redacted_lines += 1
            continue

        # redact secrets in-line
        ln2 = ln
        for r in sec_res:
            if r.search(ln2):
                ln2 = r.sub("[REDACTED_SECRET]", ln2)
                redacted_secrets += 1
        out_lines.append(ln2)

    out = "\n".join(out_lines).strip()

    truncated = False
    if len(out) > max_chars:
        out = out[: max_chars].rstrip() + "\n[TRUNCATED]"
        truncated = True

    return SanitizeResult(text=out, redacted_lines=redacted_lines, redacted_secrets=redacted_secrets, truncated=truncated)
