#!/usr/bin/env python3
"""Deterministically distill any unprocessed daily logs.

Problem this solves:
- A scheduled distill job that tries to guess "yesterday" may miss days if the
  agent was offline, rate-limited, or a prior run failed.

This script:
- Scans `memory/YYYY-MM-DD.md` files under a workspace root
- Checks for corresponding receipts under `memory/staging/receipts/YYYY-MM-DD.json`
- Runs distill for any missing receipts (oldest-first by default)

It is local-first and idempotent at the day level (a day with receipts is
considered processed).

Usage:
  python3 memory-architecture/scripts/distill_pending.py --workspace ~/.openclaw/workspace
  python3 memory-architecture/scripts/distill_pending.py --workspace ~/.openclaw/workspace --limit 3

Exit codes:
- 0: success
- 2: no pending days
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def list_daily_logs(memory_dir: Path) -> List[str]:
    out: List[str] = []
    for p in sorted(memory_dir.glob("*.md")):
        stem = p.stem
        if DATE_RE.match(stem):
            out.append(stem)
    return out


def has_receipt(staging_receipts: Path, day: str) -> bool:
    return (staging_receipts / f"{day}.json").exists()


def run_distill(skill_dir: Path, workspace: Path, day: str) -> None:
    cmd = [
        sys.executable,
        str(skill_dir / "memory-architecture" / "scripts" / "distill_daily.py"),
        "--workspace",
        str(workspace),
        "--date",
        day,
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr)
        raise SystemExit(p.returncode)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True, help="Workspace root (e.g. ~/.openclaw/workspace)")
    ap.add_argument("--limit", type=int, default=7, help="Max days to process per run")
    ap.add_argument(
        "--order",
        choices=["oldest", "newest"],
        default="oldest",
        help="Process order for pending days",
    )
    args = ap.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    memory_dir = workspace / "memory"
    staging_receipts = memory_dir / "staging" / "receipts"

    if not memory_dir.exists():
        raise SystemExit(f"memory dir not found: {memory_dir}")

    # skill_dir is the directory that contains memory-architecture/
    skill_dir = Path(__file__).resolve().parents[2]

    days = list_daily_logs(memory_dir)
    pending = [d for d in days if not has_receipt(staging_receipts, d)]
    if args.order == "newest":
        pending = list(reversed(pending))

    pending = pending[: max(0, args.limit)]

    report = {
        "workspace": str(workspace),
        "dailyCount": len(days),
        "pendingCount": len([d for d in days if not has_receipt(staging_receipts, d)]),
        "runCount": len(pending),
        "processed": [],
    }

    if not pending:
        print(json.dumps({**report, "status": "no-pending"}, indent=2))
        raise SystemExit(2)

    for d in pending:
        run_distill(skill_dir, workspace, d)
        report["processed"].append(d)

    report["status"] = "ok"
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
