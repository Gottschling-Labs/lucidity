#!/usr/bin/env python3
"""Deduplicate and canonicalize staged memory outputs.

Reads:
- memory/staging/receipts/*.json
- memory/staging/topics/*.md
- memory/staging/MEMORY.candidates.md

Writes:
- memory/staging/deduped/topics/*.md
- memory/staging/deduped/MEMORY.candidates.md
- memory/staging/reports/dedupe-report.json

This is conservative: it never edits canonical memory files.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

WORKSPACE = Path(__file__).resolve().parents[2]
MEMORY_DIR = WORKSPACE / "memory"
STAGING = MEMORY_DIR / "staging"


def norm_ws(s: str) -> str:
    s = re.sub(r"[ \t]+$", "", s, flags=re.M)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip() + "\n"


def split_blocks(md: str) -> List[str]:
    """Split by H2 headings into blocks including heading line."""
    md = md.strip()
    if not md:
        return []

    # Keep the file header (H1 etc.) as a prefix block.
    m = re.search(r"^##\s+", md, flags=re.M)
    if not m:
        return [md + "\n"]

    prefix = md[: m.start()].strip()
    rest = md[m.start() :]

    blocks: List[str] = []
    if prefix:
        blocks.append(prefix + "\n\n")

    parts = re.split(r"(?m)^(?=##\s+)", rest)
    for p in parts:
        p = p.strip()
        if p:
            blocks.append(p + "\n\n")
    return blocks


def block_key(block: str) -> Tuple[str, str]:
    """Return (type, normalized heading)"""
    heading = ""
    typ = ""
    lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
    if lines and lines[0].startswith("##"):
        heading = re.sub(r"\s+", " ", lines[0][2:].strip()).lower()
    for ln in lines[:20]:
        m = re.match(r"-\s*type:\s*(\w+)", ln, flags=re.I)
        if m:
            typ = m.group(1).lower()
            break
    return (typ or "unknown", heading)


def load_receipts() -> List[Dict]:
    receipts: List[Dict] = []
    for p in sorted((STAGING / "receipts").glob("*.json")):
        try:
            receipts.extend(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    return receipts


@dataclass
class DedupeStats:
    blocks_in: int = 0
    blocks_out: int = 0
    dropped_hard: int = 0
    dropped_soft: int = 0
    dropped_heur: int = 0


def dedupe_blocks(blocks: List[str]) -> Tuple[List[str], DedupeStats]:
    stats = DedupeStats(blocks_in=len(blocks))

    out: List[str] = []
    seen_exact = set()
    seen_key = set()

    for b in blocks:
        b2 = norm_ws(b)
        if b2 in seen_exact:
            stats.dropped_soft += 1
            continue
        k = block_key(b2)
        if k in seen_key and k[1]:
            # heuristic duplicate inside a topic file
            stats.dropped_heur += 1
            continue
        out.append(b2)
        seen_exact.add(b2)
        seen_key.add(k)

    stats.blocks_out = len(out)
    return out, stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", help="Workspace root (default: auto-detected)")
    ap.add_argument("--write", action="store_true", help="Write deduped outputs")
    args = ap.parse_args()

    global WORKSPACE, MEMORY_DIR, STAGING
    if args.workspace:
        WORKSPACE = Path(args.workspace).expanduser().resolve()
        MEMORY_DIR = WORKSPACE / "memory"
        STAGING = MEMORY_DIR / "staging"

    (STAGING / "deduped" / "topics").mkdir(parents=True, exist_ok=True)
    (STAGING / "reports").mkdir(parents=True, exist_ok=True)

    receipts = load_receipts()
    hard_seen_sources = set()
    hard_seen_outputs = set()

    hard_dupes = 0
    for r in receipts:
        sh = (r.get("source") or {}).get("sha256")
        oh = (r.get("output") or {}).get("sha256")
        if sh:
            if sh in hard_seen_sources:
                hard_dupes += 1
            hard_seen_sources.add(sh)
        if oh:
            hard_seen_outputs.add(oh)

    report: Dict = {
        "workspace": str(WORKSPACE),
        "receipts": {
            "count": len(receipts),
            "duplicate_sources": hard_dupes,
        },
        "files": {},
    }

    # Dedup topics
    for tp in sorted((STAGING / "topics").glob("*.md")):
        blocks = split_blocks(tp.read_text(encoding="utf-8"))
        deduped, stats = dedupe_blocks(blocks)
        report["files"][str(tp.relative_to(WORKSPACE))] = stats.__dict__
        if args.write:
            outp = STAGING / "deduped" / "topics" / tp.name
            outp.write_text("".join(deduped), encoding="utf-8")

    # Dedup MEMORY candidates
    memc = STAGING / "MEMORY.candidates.md"
    if memc.exists():
        blocks = split_blocks(memc.read_text(encoding="utf-8"))
        deduped, stats = dedupe_blocks(blocks)
        report["files"][str(memc.relative_to(WORKSPACE))] = stats.__dict__
        if args.write:
            outp = STAGING / "deduped" / "MEMORY.candidates.md"
            outp.write_text("".join(deduped), encoding="utf-8")

    (STAGING / "reports" / "dedupe-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
