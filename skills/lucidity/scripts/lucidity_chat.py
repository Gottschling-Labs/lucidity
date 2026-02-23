#!/usr/bin/env python3
"""Lucidity chat command helper.

This is a small CLI wrapper so chat commands can be executed deterministically.

Example:
  python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace status
  python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace distill-pending --limit 7
  python3 skills/lucidity/scripts/lucidity_chat.py --workspace ~/.openclaw/workspace apply --dry-run

The OpenClaw agent can be instructed in chat to run these commands.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO_ROOT / "skills" / "lucidity"
SCRIPTS_DIR = SKILL_DIR / "memory-architecture" / "scripts"


def run(cmd: list[str]) -> int:
    p = subprocess.run(cmd)
    return p.returncode


def main() -> None:
    ap = argparse.ArgumentParser(prog="lucidity_chat")
    ap.add_argument("--workspace", default=str(Path("~/.openclaw/workspace").expanduser()), help="Workspace root")

    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")

    p = sub.add_parser("backup")
    p.add_argument("--write", action="store_true")

    p = sub.add_parser("distill-pending")
    p.add_argument("--limit", type=int, default=7)

    p = sub.add_parser("dedupe")
    p.add_argument("--write", action="store_true")

    p = sub.add_parser("apply")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--write", action="store_true")

    p = sub.add_parser("prune")
    p.add_argument("--days", type=int, default=14)
    p.add_argument("--write", action="store_true")

    args = ap.parse_args()
    ws = str(Path(args.workspace).expanduser().resolve())

    if args.cmd == "status":
        # best-effort: openclaw may not be installed in all environments
        subprocess.run(["openclaw", "status", "--deep"], check=False)
        raise SystemExit(
            run([sys.executable, str(SCRIPTS_DIR / "memory_stats.py"), "--workspace", ws])
        )

    if args.cmd == "backup":
        cmd = [sys.executable, str(SCRIPTS_DIR / "backup_memory.py"), "--workspace", ws]
        if args.write:
            cmd.append("--write")
        raise SystemExit(run(cmd))

    if args.cmd == "distill-pending":
        raise SystemExit(
            run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "distill_pending.py"),
                    "--workspace",
                    ws,
                    "--limit",
                    str(args.limit),
                ]
            )
        )

    if args.cmd == "dedupe":
        cmd = [sys.executable, str(SCRIPTS_DIR / "dedupe_staging.py"), "--workspace", ws]
        if args.write:
            cmd.append("--write")
        raise SystemExit(run(cmd))

    if args.cmd == "apply":
        cmd = [sys.executable, str(SCRIPTS_DIR / "apply_staging.py"), "--workspace", ws]
        if args.write:
            cmd.append("--write")
        else:
            cmd.append("--dry-run")
        raise SystemExit(run(cmd))

    if args.cmd == "prune":
        cmd = [sys.executable, str(SCRIPTS_DIR / "prune_staging.py"), "--workspace", ws, "--days", str(args.days)]
        if args.write:
            cmd.append("--write")
        raise SystemExit(run(cmd))


if __name__ == "__main__":
    main()
