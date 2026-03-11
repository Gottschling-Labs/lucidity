#!/usr/bin/env python3
"""Dream job: daily recall + long-term storage staging.

See canonical copy in:
- workspace/memory-architecture/scripts/dream_daily.py

This skill-local copy exists so the Lucidity skill is self-contained.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[4]
MEMORY_DIR = WORKSPACE / "memory"
SCRIPTS_DIR = WORKSPACE / "skills" / "lucidity" / "memory-architecture" / "scripts"


def run(cmd: list[str]) -> None:
    p = subprocess.run(cmd, cwd=str(WORKSPACE))
    if p.returncode != 0:
        raise SystemExit(p.returncode)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--tz-offset-minutes", type=int, default=0)
    ap.add_argument("--keyword-regex", help="Optional filter for transcript extraction")
    args = ap.parse_args()

    day = args.date

    run([
        "python3",
        str(SCRIPTS_DIR / "distill_sessions.py"),
        "--date",
        day,
        "--tz-offset-minutes",
        str(args.tz_offset_minutes),
        *(["--keyword-regex", args.keyword_regex] if args.keyword_regex else []),
    ])

    daily = MEMORY_DIR / f"{day}.md"
    if daily.exists():
        run(["python3", str(SCRIPTS_DIR / "distill_daily.py"), "--path", f"memory/{day}.md"])

    transcript_md = MEMORY_DIR / "staging" / "sessions" / f"{day}.sessions.md"
    if transcript_md.exists():
        rel = transcript_md.relative_to(WORKSPACE)
        run(["python3", str(SCRIPTS_DIR / "distill_daily.py"), "--path", str(rel)])

    run(["python3", str(SCRIPTS_DIR / "dedupe_staging.py"), "--write"])

    ts = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    print(f"Dream complete for {day} at {ts}")


if __name__ == "__main__":
    main()
