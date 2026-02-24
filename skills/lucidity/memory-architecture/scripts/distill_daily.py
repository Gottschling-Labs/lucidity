#!/usr/bin/env python3
"""Non-destructive daily memory distiller.

Reads a T2 daily log (memory/YYYY-MM-DD.md) and writes staged candidates into:
- memory/staging/topics/<topic>.md
- memory/staging/MEMORY.candidates.md
- memory/staging/receipts/<date>.json

Design goals:
- Conservative, local-first (no LLM calls)
- Staging-only (never writes canonical memory)
- Deterministic heuristics that promote *structure*:
  - procedural candidates from Steps/How-to sections
  - semantic candidates from Decision/Policy/Preference/Fact statements
  - episodic notes remain retrievable but are not auto-promoted by default

Usage:
  python3 memory-architecture/scripts/distill_daily.py --workspace ~/.openclaw/workspace --date 2026-02-16
  python3 memory-architecture/scripts/distill_daily.py --workspace ~/.openclaw/workspace --path memory/2026-02-16.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
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
    "gpl": "lucidity",
    "lucidity": "lucidity",
}

SEMANTIC_PREFIXES = (
    "decision:",
    "policy:",
    "preference:",
    "fact:",
    "rule:",
    "canonical:",
)

PROCEDURAL_PREFIXES = (
    "procedure:",
    "how to:",
    "steps:",
    "run:",
    "command:",
)


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
    pre = parts[0].strip()
    if pre:
        out.append(("(preamble)", pre))
    for p in parts[1:]:
        lines = p.splitlines()
        heading = lines[0].strip() if lines else "(empty)"
        body = "\n".join(lines[1:]).strip()
        out.append((heading, body))
    return out


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


def summarize_episodic(body: str) -> str:
    # pick first non-empty bullet/line
    for line in body.splitlines():
        t = line.strip().lstrip("- ").strip()
        if not t:
            continue
        if t.lower().startswith(SEMANTIC_PREFIXES) or t.lower().startswith(PROCEDURAL_PREFIXES):
            continue
        return (t[:140] + "...") if len(t) > 140 else t
    return "(fill in)"


def extract_semantic_lines(body: str) -> List[str]:
    lines = []
    for raw in body.splitlines():
        s = raw.strip().lstrip("- ").strip()
        if not s:
            continue
        lo = s.lower()
        if lo.startswith(SEMANTIC_PREFIXES):
            # strip prefix label
            lines.append(s.split(":", 1)[1].strip() or s)
    return lines


def has_steps_block(body: str) -> bool:
    if re.search(r"^\s*steps:\s*$", body, flags=re.I | re.M):
        return True
    if re.search(r"^\s*\d+[\).]\s+", body, flags=re.M):
        return True
    if re.search(r"^\s*1\)\s+", body, flags=re.M):
        return True
    return False


def extract_verify_text(body: str) -> str | None:
    # Capture lines after a "Verify:" marker.
    m = re.search(r"^\s*(verify|verification)\s*:\s*$", body, flags=re.I | re.M)
    if not m:
        return None
    tail = body[m.end() :].strip("\n")
    lines: List[str] = []
    for ln in tail.splitlines():
        if not ln.strip():
            break
        # stop if a new section-like label starts
        if re.match(r"^\s*(prereqs|steps|title)\s*:\s*$", ln, flags=re.I):
            break
        lines.append(ln.rstrip())
    txt = "\n".join(lines).strip()
    return txt or None


def extract_procedural_block(body: str) -> str | None:
    # If there's a Steps: section, take from that line onward
    m = re.search(r"^\s*steps:\s*$", body, flags=re.I | re.M)
    if m:
        return body[m.start() :].strip()
    # Otherwise if there are numbered steps, include the whole body (it is likely already a SOP)
    if has_steps_block(body):
        return body.strip()
    # If the body has an explicit procedural prefix line, treat as procedural
    for raw in body.splitlines():
        s = raw.strip().lstrip("- ").strip().lower()
        if any(s.startswith(p) for p in PROCEDURAL_PREFIXES):
            return body.strip()
    return None


def now_ts() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", help="Workspace root (default: auto-detected)")
    ap.add_argument(
        "--staging-only",
        action="store_true",
        help="Accepted for compatibility; distill is always staging-first",
    )
    ap.add_argument("--date", help="YYYY-MM-DD")
    ap.add_argument("--path", help="Path to daily md, relative to workspace")
    args = ap.parse_args()

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

        ts = now_ts()
        rel = in_path.relative_to(WORKSPACE)
        topic = infer_topic(heading + "\n" + body)

        source_excerpt = ("## " + heading + "\n" + body).strip()
        source_hash = sha256_text(source_excerpt)

        # 1) Semantic candidates extracted from explicit lines (Decision/Policy/Preference/etc.)
        semantic_lines = extract_semantic_lines(body)
        for i, stmt in enumerate(semantic_lines):
            title = heading if len(semantic_lines) == 1 else f"{heading} ({i+1})"
            block = (
                f"\n## Semantic candidate: {title}\n\n"
                f"- type: semantic\n"
                f"- confidence: medium\n"
                f"- scope: project\n"
                f"- statement: {stmt}\n"
                f"- evidence:\n"
                f"  - {rel}#{heading}\n"
                f"- generated_at: {ts}\n\n"
            )
            out_path = append_memory_candidates(block)
            receipts.append(
                {
                    "source": {"path": str(rel), "heading": heading, "sha256": source_hash},
                    "output": {
                        "path": str(out_path.relative_to(WORKSPACE)),
                        "sha256": sha256_text(block),
                        "kind": "semantic",
                        "topic": topic,
                    },
                }
            )

        # 2) Procedural candidate from a steps block / numbered list
        proc = extract_procedural_block(body)
        if proc:
            verify_txt = extract_verify_text(body)
            trigger_txt = f"When you need: {heading}" if heading and heading != "(no heading)" else "When this procedure is needed"
            if verify_txt:
                # Keep the required field as a single non-placeholder line for apply scoring.
                verification_line = "- verification: verification steps listed below\n"
            else:
                verification_line = "- verification: (how do we confirm it worked?)\n"

            block = (
                f"\n## Procedure (candidate): {heading}\n\n"
                f"- type: procedural\n"
                f"- source: {rel}#{heading}\n"
                f"- trigger: {trigger_txt}\n"
                f"- guardrails:\n  - (what not to do)\n"
                f"{verification_line}"
                f"- generated_at: {ts}\n\n"
                f"{proc}\n\n"
            )

            # If we extracted Verify text, append it as a separate section (does not affect scoring).
            if verify_txt:
                block += f"\nVerification details (from daily log):\n{verify_txt}\n\n"
            out_path = append_topic_candidate(topic, block)
            receipts.append(
                {
                    "source": {"path": str(rel), "heading": heading, "sha256": source_hash},
                    "output": {
                        "path": str(out_path.relative_to(WORKSPACE)),
                        "sha256": sha256_text(block),
                        "kind": "procedural",
                        "topic": topic,
                    },
                }
            )

        # 3) Always stage a minimal episodic note as retrievable context (not auto-promoted)
        summary = summarize_episodic(body)
        ep_block = (
            f"\n## Episodic note (candidate): {heading}\n\n"
            f"- type: episodic\n"
            f"- source: {rel}#{heading}\n"
            f"- generated_at: {ts}\n\n"
            f"- summary: {summary}\n\n"
        )
        out_path = append_topic_candidate(topic, ep_block)
        receipts.append(
            {
                "source": {"path": str(rel), "heading": heading, "sha256": source_hash},
                "output": {
                    "path": str(out_path.relative_to(WORKSPACE)),
                    "sha256": sha256_text(ep_block),
                    "kind": "episodic",
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
