#!/usr/bin/env python3
"""Sanitize evidence quotes in existing staging files.

This is a one-off maintenance utility.

It scans:
- memory/staging/topics/*.md
- memory/staging/MEMORY.candidates.md

and rewrites `evidence_quote: |` blocks in-place.

Usage:
  python3 sanitize_staging_quotes.py --workspace ~/.openclaw/workspace --dry-run
  python3 sanitize_staging_quotes.py --workspace ~/.openclaw/workspace --write
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from staging_sanitizer import sanitize_evidence_quote


QUOTE_BLOCK_RE = re.compile(
    r"(?ms)^\s*-\s*evidence_quote\s*:\s*\|\s*\n(?P<body>(?:^\s{2}.*\n?)*)"
)


def sanitize_file(p: Path) -> tuple[bool, int, int, bool]:
    txt = p.read_text(encoding="utf-8")
    changed = False
    redacted_lines = 0
    redacted_secrets = 0
    truncated_any = False

    def repl(m: re.Match) -> str:
        nonlocal changed, redacted_lines, redacted_secrets, truncated_any
        body = m.group("body")
        # de-indent two spaces
        raw = "\n".join([ln[2:] if ln.startswith("  ") else ln for ln in body.splitlines()]).strip("\n")
        res = sanitize_evidence_quote(raw)
        redacted_lines += res.redacted_lines
        redacted_secrets += res.redacted_secrets
        truncated_any = truncated_any or res.truncated
        changed = True
        indented = "\n".join(["  " + ln for ln in res.text.splitlines()])
        return f"- evidence_quote: |\n{indented}\n"

    out = QUOTE_BLOCK_RE.sub(repl, txt)
    if changed:
        p.write_text(out, encoding="utf-8")
    return changed, redacted_lines, redacted_secrets, truncated_any


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ws = Path(args.workspace).expanduser().resolve()
    staging = ws / "memory" / "staging"

    if args.dry_run:
        args.write = False

    files = []
    if (staging / "topics").exists():
        files.extend(sorted((staging / "topics").glob("*.md")))
    if (staging / "MEMORY.candidates.md").exists():
        files.append(staging / "MEMORY.candidates.md")

    total_changed = 0
    for f in files:
        before = f.read_text(encoding="utf-8")
        # Run sanitize in-memory by writing to temp then optionally committing
        # We'll just reuse sanitize_file but restore if not write.
        changed, rl, rs, trunc = sanitize_file(f)
        after = f.read_text(encoding="utf-8") if changed else before

        if changed and not args.write:
            f.write_text(before, encoding="utf-8")
        if changed:
            total_changed += 1

        if changed:
            print(f"{f.relative_to(ws)}: sanitized (redacted_lines={rl} redacted_secrets={rs} truncated={trunc})")

    if total_changed == 0:
        print("No evidence_quote blocks found to sanitize.")


if __name__ == "__main__":
    main()
