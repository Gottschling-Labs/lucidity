#!/usr/bin/env python3
"""Non-destructive daily memory distiller.

Reads a T2 daily log (memory/YYYY-MM-DD.md) and writes staged candidates into:
- memory/staging/topics/<topic>.md
- memory/staging/MEMORY.candidates.md
- memory/staging/receipts/<date>.json

This is a conservative v0:
- no LLM calls
- heuristic classification
- does not modify canonical memory files

Usage:
  python3 memory-architecture/scripts/distill_daily.py --date 2026-02-16
  python3 memory-architecture/scripts/distill_daily.py --path memory/2026-02-16.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

WORKSPACE = Path(__file__).resolve().parents[2]
MEMORY_DIR = WORKSPACE / "memory"
STAGING_DIR = MEMORY_DIR / "staging"

TOPIC_KEYWORDS = {
    "openclaw": "openclaw",
    "gateway": "openclaw",
    "telegram": "messaging",
    "whatsapp": "messaging",
    "discord": "messaging",
    "memory": "memory-architecture",
    "lancedb": "memory-architecture",
    "fts": "memory-architecture",
    "bm25": "memory-architecture",
    "cron": "automation",
    "heartbeat": "automation",
    "security": "security",
}


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_daily(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_sections(md: str) -> List[Tuple[str, str]]:
    """Return list of (heading, body) for H2 sections."""
    parts = re.split(r"^##\s+", md, flags=re.M)
    if len(parts) <= 1:
        return [("(no heading)", md.strip())]
    out: List[Tuple[str, str]] = []
    # parts[0] is preamble (before first ##)
    pre = parts[0].strip()
    if pre:
        out.append(("(preamble)", pre))
    for p in parts[1:]:
        lines = p.splitlines()
        heading = lines[0].strip() if lines else "(empty)"
        body = "\n".join(lines[1:]).strip()
        out.append((heading, body))
    return out


def classify(body: str) -> str:
    b = body.lower()
    if re.search(r"\n\s*steps:\s*\n", body, flags=re.I) or re.search(r"\n\s*1\)\s+", body):
        return "procedural"
    if re.search(r"\n\s*statement:\s+", body, flags=re.I) or re.search(r"\btype:\s*semantic\b", b):
        return "semantic"
    if re.search(r"\btype:\s*procedural\b", b):
        return "procedural"
    if re.search(r"\btype:\s*episodic\b", b):
        return "episodic"
    return "episodic"


def infer_topic(text: str) -> str:
    t = text.lower()
    for k, topic in TOPIC_KEYWORDS.items():
        if k in t:
            return topic
    return "general"


def ensure_dirs() -> None:
    (STAGING_DIR / "topics").mkdir(parents=True, exist_ok=True)
    (STAGING_DIR / "receipts").mkdir(parents=True, exist_ok=True)


def append_topic_candidate(topic: str, content: str) -> Path:
    out = STAGING_DIR / "topics" / f"{topic}.md"
    if out.exists():
        prev = out.read_text(encoding="utf-8")
    else:
        prev = f"# Topic Candidate: {topic}\n\n(Generated; review before promoting to memory/topics/)\n\n"
    out.write_text(prev + content, encoding="utf-8")
    return out


def append_memory_candidates(content: str) -> Path:
    out = STAGING_DIR / "MEMORY.candidates.md"
    if out.exists():
        prev = out.read_text(encoding="utf-8")
    else:
        prev = "# MEMORY.md Candidates\n\n(Generated; review before promoting to MEMORY.md)\n\n"
    out.write_text(prev + content, encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", help="Workspace root (default: auto-detected)")
    ap.add_argument("--staging-only", action="store_true", help="Accepted for compatibility; distill is always staging-first")
    ap.add_argument("--date", help="YYYY-MM-DD")
    ap.add_argument("--path", help="Path to daily md, relative to workspace")
    args = ap.parse_args()

    # Allow running against an arbitrary workspace root (e.g., demo-workspace or ~/.openclaw/workspace)
    global WORKSPACE, MEMORY_DIR, STAGING_DIR
    if args.workspace:
        WORKSPACE = Path(args.workspace).expanduser().resolve()
        MEMORY_DIR = WORKSPACE / "memory"
        STAGING_DIR = MEMORY_DIR / "staging"

    if args.path:
        in_path = (WORKSPACE / args.path).resolve()
    elif args.date:
        in_path = MEMORY_DIR / f"{args.date}.md"
    else:
        ap.error("Provide --date or --path")

    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")

    ensure_dirs()

    md = load_daily(in_path)
    sections = split_sections(md)

    receipts: List[Dict] = []
    for heading, body in sections:
        if not body.strip():
            continue
        kind = classify(body)
        topic = infer_topic(heading + "\n" + body)

        source_excerpt = ("## " + heading + "\n" + body).strip()
        source_hash = sha256_text(source_excerpt)

        ts = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z')

        if kind == "procedural":
            block = f"\n## Procedure (candidate): {heading}\n\n- type: procedural\n- source: {in_path.relative_to(WORKSPACE)}#{heading}\n- trigger: (when should this be used?)\n- verification: (how do we confirm it worked?)\n- generated_at: {ts}\n\n{body}\n\n"
            out_path = append_topic_candidate(topic, block)
            out_excerpt = block
        elif kind == "semantic":
            block = f"\n## Semantic candidate: {heading}\n\n- type: semantic\n- confidence: low\n- evidence:\n  - {in_path.relative_to(WORKSPACE)}#{heading}\n- generated_at: {ts}\n\n{body}\n\n"
            out_path = append_memory_candidates(block)
            out_excerpt = block
        else:
            # episodic: do not promote by default; just create a tiny topic note
            block = f"\n## Episodic note (candidate): {heading}\n\n- type: episodic\n- source: {in_path.relative_to(WORKSPACE)}#{heading}\n- generated_at: {ts}\n\n- summary: (fill in)\n\n"
            out_path = append_topic_candidate(topic, block)
            out_excerpt = block

        receipts.append(
            {
                "source": {
                    "path": str(in_path.relative_to(WORKSPACE)),
                    "heading": heading,
                    "sha256": source_hash,
                },
                "output": {
                    "path": str(out_path.relative_to(WORKSPACE)),
                    "sha256": sha256_text(out_excerpt),
                    "kind": kind,
                    "topic": topic,
                },
            }
        )

    out_receipts = STAGING_DIR / "receipts" / (in_path.stem + ".json")
    out_receipts.write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")

    print(f"Staged {len(receipts)} candidates")
    print(f"- receipts: {out_receipts.relative_to(WORKSPACE)}")
    print(f"- topics:   {(STAGING_DIR/'topics').relative_to(WORKSPACE)}/")
    print(f"- memory:   {(STAGING_DIR/'MEMORY.candidates.md').relative_to(WORKSPACE)}")


if __name__ == "__main__":
    main()
