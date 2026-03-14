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
    ap.add_argument("--topic", required=True, help="Debate topic / question")
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--model", default="default", help="Optional model override")
    ap.add_argument("--agent", default="main", help="OpenClaw agent id to use for role turns")
    ap.add_argument("--dry-run", action="store_true", help="Do not run agent turns; only init run + print plan")
    args = ap.parse_args()

    from artifacts import init_run, resolve_workspace, append_jsonl, write_json

    ws = resolve_workspace()
    rp = init_run(workspace=ws, topic=args.topic, rounds=args.rounds, model=args.model)

    plan = {
        "ts": now_z(),
        "topic": args.topic,
        "rounds": args.rounds,
        "model": args.model,
        "agent": args.agent,
        "run_id": rp.run_id,
        "run_dir": str(rp.run_dir.relative_to(ws)),
    }

    if args.dry_run:
        plan["status"] = "initialized"
        plan["next"] = "Run without --dry-run to execute role turns via `openclaw agent --json` and persist transcript + consensus."
        print(json.dumps(plan, indent=2))
        return

    import subprocess

    def run_role(role: str, instruction: str) -> dict:
        session_id = f"{rp.run_id}:{role}"
        msg = f"ROLE: {role}\n\nTOPIC:\n{args.topic}\n\nINSTRUCTIONS:\n{instruction}\n\nReturn a concise, structured answer."
        cmd = [
            "openclaw",
            "agent",
            "--agent",
            args.agent,
            "--session-id",
            session_id,
            "--message",
            msg,
            "--json",
        ]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if p.returncode != 0:
            raise RuntimeError(f"openclaw agent failed for {role}: {p.stderr.strip()}")
        return json.loads(p.stdout)

    # Round 1 (minimal implementation)
    prompts = {
        "proponent": "Argue for the best possible approach. List benefits and a concrete proposal.",
        "critic": "Identify risks, failure modes, and what could go wrong. Suggest mitigations.",
        "fact_checker": "Flag claims needing verification. If unsure, label uncertainty and suggest checks.",
        "executor": "Synthesize into an actionable plan (steps, sequencing, guardrails).",
    }

    results = {}
    for role, instr in prompts.items():
        res = run_role(role, instr)
        results[role] = res
        append_jsonl(
            rp.transcript_jsonl,
            {
                "ts": now_z(),
                "role": role,
                "session_id": f"{rp.run_id}:{role}",
                "request": {"topic": args.topic, "instruction": instr},
                "response": res,
            },
        )

    consensus = {
        "ts": now_z(),
        "topic": args.topic,
        "run_id": rp.run_id,
        "model": args.model,
        "agent": args.agent,
        "roles": list(prompts.keys()),
        "executor": results.get("executor"),
    }
    write_json(rp.consensus_json, consensus)

    plan["status"] = "completed_round_1"
    plan["consensus"] = str(rp.consensus_json.relative_to(ws))
    plan["transcript"] = str(rp.transcript_jsonl.relative_to(ws))
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
