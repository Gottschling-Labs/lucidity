#!/usr/bin/env python3
"""Dream reflection: deterministically process any unreflected daily logs.

This script is the deterministic, catch-up capable scheduler for the LLM reflection step.

It does NOT call an LLM itself. Instead, it:
- finds pending days (daily logs missing a reflection receipt)
- prints a JSON plan for what to reflect

A separate step (typically an OpenClaw agent turn) should:
- read each daily log
- produce structured semantic/procedural candidates WITH evidence pointers
- submit them to `reflect_apply_candidates.py`

Usage:
  python3 reflect_pending.py --workspace ~/.openclaw/workspace
  python3 reflect_pending.py --workspace ~/.openclaw/workspace --limit 3

Exit codes:
- 0: success (pending list may be empty)
- 2: no pending days
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import List

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def list_daily_logs(memory_dir: Path) -> List[str]:
    out: List[str] = []
    for p in sorted(memory_dir.glob("*.md")):
        if DATE_RE.match(p.stem):
            out.append(p.stem)
    return out


def has_reflect_receipt(receipts_dir: Path, day: str) -> bool:
    return (receipts_dir / f"{day}.json").exists()


def main() -> None:
    ap = argparse.ArgumentParser(prog="reflect_pending")
    ap.add_argument("--workspace", required=True, help="Workspace root")
    ap.add_argument("--limit", type=int, default=1, help="Max days to reflect per run")
    ap.add_argument("--order", choices=["oldest", "newest"], default="oldest")
    args = ap.parse_args()

    ws = Path(args.workspace).expanduser().resolve()
    mem = ws / "memory"
    if not mem.exists():
        raise SystemExit(f"memory dir not found: {mem}")

    receipts_dir = mem / "staging" / "reflect" / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)

    days = list_daily_logs(mem)
    pending = [d for d in days if not has_reflect_receipt(receipts_dir, d)]
    if args.order == "newest":
        pending = list(reversed(pending))

    planned = pending[: max(0, args.limit)]

    report = {
        "workspace": str(ws),
        "dailyCount": len(days),
        "pendingCount": len(pending),
        "plannedCount": len(planned),
        "planned": [
            {
                "day": d,
                "path": f"memory/{d}.md",
                "receipt": f"memory/staging/reflect/receipts/{d}.json",
            }
            for d in planned
        ],
        "status": "ok" if planned else "no-pending",
    }

    print(json.dumps(report, indent=2))

    if not planned:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
