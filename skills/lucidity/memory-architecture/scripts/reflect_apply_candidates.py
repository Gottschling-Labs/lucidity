#!/usr/bin/env python3
"""Dream reflection: apply LLM-produced candidates into Lucidity staging.

This script is a deterministic writer. It takes a JSON payload (typically produced
by an OpenClaw agent turn) and writes:
- memory/staging/topics/<topic>.md (procedural candidates)
- memory/staging/MEMORY.candidates.md (semantic candidates)
- memory/staging/reflect/receipts/<day>.json (receipt + hashes)

It never writes canonical memory.

Input JSON schema (minimal):
{
  "day": "YYYY-MM-DD",
  "source": {"path": "memory/YYYY-MM-DD.md", "headings": ["..."]},
  "candidates": [
    {
      "kind": "semantic"|"procedural",
      "topic": "openclaw"|"general"|..., 
      "title": "...",
      "evidence": [{"path":"memory/YYYY-MM-DD.md", "heading":"Some Heading"}],
      "statement": "...",               # semantic
      "confidence": "high|medium|low",  # semantic
      "trigger": "...",                 # procedural
      "steps": ["...", "..."],          # procedural
      "verification": "...",            # procedural
      "guardrails": ["...", "..."]      # optional
    }
  ]
}

Usage:
  python3 reflect_apply_candidates.py --workspace ~/.openclaw/workspace --in payload.json
  cat payload.json | python3 reflect_apply_candidates.py --workspace ~/.openclaw/workspace --in -
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def now_z() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def split_sections(md: str) -> Dict[str, str]:
    """Map H2 heading -> body."""
    parts = re.split(r"^##\s+", md, flags=re.M)
    out: Dict[str, str] = {}
    if len(parts) <= 1:
        return out
    for p in parts[1:]:
        lines = p.splitlines()
        heading = lines[0].strip() if lines else ""
        body = "\n".join(lines[1:]).strip()
        if heading:
            out[heading] = body
    return out


def append_topic_candidate(workspace: Path, topic: str, content: str) -> str:
    staging = workspace / "memory" / "staging" / "topics"
    out = staging / f"{topic}.md"
    if out.exists():
        prev = read_text(out)
    else:
        prev = f"# Topic Candidate: {topic}\n\n(Generated; review before promoting to memory/topics/)\n\n"
    write_text(out, prev + content)
    return str(out.relative_to(workspace))


def append_memory_candidates(workspace: Path, content: str) -> str:
    out = workspace / "memory" / "staging" / "MEMORY.candidates.md"
    if out.exists():
        prev = read_text(out)
    else:
        prev = "# MEMORY.md Candidates\n\n(Generated; review before promoting to MEMORY.md)\n\n"
    write_text(out, prev + content)
    return str(out.relative_to(workspace))


def main() -> None:
    ap = argparse.ArgumentParser(prog="reflect_apply_candidates")
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--in", dest="in_path", default="-", help="JSON input path or '-' for stdin")
    args = ap.parse_args()

    ws = Path(args.workspace).expanduser().resolve()

    if args.in_path == "-":
        payload = json.loads(Path("/dev/stdin").read_text(encoding="utf-8"))
    else:
        payload = json.loads(Path(args.in_path).expanduser().read_text(encoding="utf-8"))

    day = payload.get("day")
    if not day or not re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        raise SystemExit("payload.day must be YYYY-MM-DD")

    src_path = ws / "memory" / f"{day}.md"
    if not src_path.exists():
        raise SystemExit(f"source daily log not found: {src_path}")

    headings = split_sections(read_text(src_path))

    receipts_dir = ws / "memory" / "staging" / "reflect" / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)

    run_ts = now_z()
    receipt: Dict[str, Any] = {
        "run_ts": run_ts,
        "day": day,
        "source": {
            "path": str(src_path.relative_to(ws)),
            "sha256": sha256_text(read_text(src_path)),
        },
        "outputs": [],
        "candidates": [],
    }

    for c in payload.get("candidates", []):
        kind = (c.get("kind") or "").lower()
        title = (c.get("title") or "").strip() or "(untitled)"
        topic = (c.get("topic") or "general").strip() or "general"
        evidence = c.get("evidence") or []

        if kind == "semantic":
            stmt = (c.get("statement") or "").strip()
            conf = (c.get("confidence") or "medium").strip()
            if not stmt:
                continue
            if not evidence:
                # A-mode: require evidence
                continue

            ev_lines = "\n".join(
                [f"  - {e.get('path')}#{e.get('heading')}" for e in evidence if e.get("path") and e.get("heading")]
            )
            block = (
                f"\n## Semantic candidate: {title}\n\n"
                f"- type: semantic\n"
                f"- confidence: {conf}\n"
                f"- scope: project\n"
                f"- statement: {stmt}\n"
                f"- evidence:\n{ev_lines}\n"
                f"- generated_at: {run_ts}\n\n"
            )
            out_path = append_memory_candidates(ws, block)
            receipt["outputs"].append(out_path)
            receipt["candidates"].append(
                {
                    "kind": "semantic",
                    "title": title,
                    "topic": "MEMORY.md",
                    "block_sha256": sha256_text(block),
                }
            )

        elif kind == "procedural":
            trig = (c.get("trigger") or "").strip()
            steps = c.get("steps") or []
            verification = (c.get("verification") or "").strip()
            guardrails = c.get("guardrails") or []

            if not trig or not steps or not verification:
                continue
            if not evidence:
                continue

            steps_md = "\n".join([f"  {i+1}) {s}" for i, s in enumerate([x.strip() for x in steps if str(x).strip()])])
            guard_md = "\n".join([f"  - {g}" for g in [x.strip() for x in guardrails if str(x).strip()]])
            if not guard_md:
                guard_md = "  - (what not to do)"

            ev_ref = evidence[0]
            ev_path = ev_ref.get("path")
            ev_heading = ev_ref.get("heading")

            block = (
                f"\n## Procedure (candidate): {title}\n\n"
                f"- type: procedural\n"
                f"- source: {ev_path}#{ev_heading}\n"
                f"- trigger: {trig}\n"
                f"- guardrails:\n{guard_md}\n"
                f"- verification: {verification}\n"
                f"- generated_at: {run_ts}\n\n"
                f"Steps:\n{steps_md}\n\n"
            )

            out_path = append_topic_candidate(ws, topic, block)
            receipt["outputs"].append(out_path)
            receipt["candidates"].append(
                {
                    "kind": "procedural",
                    "title": title,
                    "topic": topic,
                    "block_sha256": sha256_text(block),
                }
            )

    receipt_path = receipts_dir / f"{day}.json"
    write_text(receipt_path, json.dumps(receipt, indent=2) + "\n")

    print(json.dumps({"status": "ok", "receipt": str(receipt_path.relative_to(ws)), "candidates": receipt["candidates"]}, indent=2))


if __name__ == "__main__":
    main()
