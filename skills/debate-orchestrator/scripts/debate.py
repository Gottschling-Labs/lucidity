#!/usr/bin/env python3
"""Debate Orchestrator (scaffold).

This CLI is a placeholder entrypoint for the debate architecture project.

It will eventually:
- spawn role sub-sessions (proponent/critic/fact-checker/executor)
- run multiple rounds with compaction
- persist transcripts and artifacts under debate-architecture/

For the spec and transcript schema, see:
- debate-architecture/spec.md
- debate-architecture/templates/transcript-conventions.md
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone


def now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    ap = argparse.ArgumentParser(prog="debate")
    ap.add_argument("--topic", help="Debate topic / question")
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--model", default="default", help="Optional model override")
    ap.add_argument("--dry-run", action="store_true", help="Do not spawn sessions; print plan")
    args = ap.parse_args()

    from artifacts import init_run, resolve_workspace

    ws = resolve_workspace()
    rp = init_run(workspace=ws, topic=args.topic or "(none)", rounds=args.rounds, model=args.model)

    plan = {
        "ts": now_z(),
        "topic": args.topic,
        "rounds": args.rounds,
        "model": args.model,
        "status": "scaffold",
        "run_id": rp.run_id,
        "run_dir": str(rp.run_dir.relative_to(ws)),
        "next": "Implement orchestration via OpenClaw sessions_spawn + artifact persistence per spec.",
    }

    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
