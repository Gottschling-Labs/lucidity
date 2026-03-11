#!/usr/bin/env python3
"""Dream job: daily recall + long-term storage staging.

This is the missing glue for the "context fell through the gaps" scenario.

What it does (safe defaults)
- Extracts a markdown snapshot from session transcripts for a given day (T2-like).
- Runs the existing distiller on BOTH:
  - the user's daily log (if present)
  - the transcript snapshot (always present if sessions exist)
- Runs dedupe on staging outputs.
- Does NOT auto-apply by default (review gate remains).

Usage
  python3 memory-architecture/scripts/dream_daily.py --date 2026-03-11 --tz-offset-minutes -240

Intended automation
- Run nightly (e.g., 04:15 local): dream yesterday.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
MEMORY_DIR = WORKSPACE / "memory"
SCRIPTS_DIR = WORKSPACE / "memory-architecture" / "scripts"


def run(cmd: list[str]) -> None:
    p = subprocess.run(cmd, cwd=str(WORKSPACE))
    if p.returncode != 0:
        raise SystemExit(p.returncode)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--tz", help="IANA timezone name for day bucketing (preferred)")
    ap.add_argument("--tz-offset-minutes", type=int, default=0, help="Legacy; prefer --tz")
    ap.add_argument("--keyword-regex", help="Optional filter for transcript extraction")
    args = ap.parse_args()

    day = args.date

    # 1) Extract transcript snapshot (staged)
    cmd = [
        "python3",
        str(SCRIPTS_DIR / "distill_sessions.py"),
        "--date",
        day,
    ]
    if args.tz:
        cmd += ["--tz", args.tz]
    else:
        cmd += ["--tz-offset-minutes", str(args.tz_offset_minutes)]
    if args.keyword_regex:
        cmd += ["--keyword-regex", args.keyword_regex]
    run(cmd)

    # 2) Distill the daily log if it exists
    daily = MEMORY_DIR / f"{day}.md"
    if daily.exists():
        run(["python3", str(SCRIPTS_DIR / "distill_daily.py"), "--path", f"memory/{day}.md"])

    # 3) Distill the transcript snapshot
    transcript_md = MEMORY_DIR / "staging" / "sessions" / f"{day}.sessions.md"
    if transcript_md.exists():
        rel = transcript_md.relative_to(WORKSPACE)
        run(["python3", str(SCRIPTS_DIR / "distill_daily.py"), "--path", str(rel)])

    # 4) Dedupe staged candidates
    run(["python3", str(SCRIPTS_DIR / "dedupe_staging.py"), "--write"])

    ts = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    print(f"Dream complete for {day} at {ts}")


if __name__ == "__main__":
    main()
