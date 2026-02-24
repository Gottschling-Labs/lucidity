#!/usr/bin/env python3
"""Apply deduped staging candidates into canonical topic briefs and MEMORY.md.

This is the productionizing step that moves content from:
- memory/staging/deduped/topics/*.md
into:
- memory/topics/*.md

Merge scope:
- Procedural candidates -> `memory/topics/*.md` (implemented)
- Semantic candidates -> `MEMORY.md` (implemented with stricter gates)

Key properties:
- High-confidence gating (configurable)
- Non-destructive merge: appends blocks that don't already exist
- Writes a manifest with before/after hashes and decisions

Usage:
  python3 memory-architecture/scripts/apply_staging.py --dry-run
  python3 memory-architecture/scripts/apply_staging.py --write
  python3 memory-architecture/scripts/apply_staging.py --config memory-architecture/config/auto-merge.json --write
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from telemetry import append_jsonl, env_session_key

WORKSPACE = Path(__file__).resolve().parents[2]


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256_text(read_text(p))


def now_z() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def split_blocks(md: str) -> List[str]:
    md = md.strip("\n")
    if not md.strip():
        return []
    m = re.search(r"^##\s+", md, flags=re.M)
    if not m:
        return [md.strip() + "\n"]

    prefix = md[: m.start()].strip("\n")
    rest = md[m.start() :]

    blocks: List[str] = []
    if prefix.strip():
        blocks.append(prefix.strip() + "\n\n")

    parts = re.split(r"(?m)^(?=##\s+)", rest)
    for p in parts:
        p = p.strip("\n")
        if p.strip():
            blocks.append(p.strip() + "\n\n")
    return blocks


def norm_block(s: str) -> str:
    s = re.sub(r"[ \t]+$", "", s, flags=re.M)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip() + "\n\n"


def extract_type(block: str) -> str:
    for ln in block.splitlines()[:30]:
        m = re.match(r"-\s*type:\s*(\w+)", ln.strip(), flags=re.I)
        if m:
            return m.group(1).lower()
    return "unknown"


def has_field(block: str, field: str) -> bool:
    pat = re.compile(rf"^\s*-\s*{re.escape(field)}\s*:\s*.+$", flags=re.I | re.M)
    return bool(pat.search(block))


def has_steps(block: str) -> bool:
    return bool(re.search(r"(?m)^\s*\d+\)\s+", block)) or ("steps:" in block.lower())


def contains_time_bound(block: str, phrases: List[str]) -> bool:
    b = block.lower()
    return any(p in b for p in phrases)


def blocked_by_safety(block: str, deny_patterns: List[str], deny_if_contains: List[str]) -> Optional[str]:
    for s in deny_if_contains:
        if s.lower() in block.lower():
            return f"denyIfContains:{s}"
    for pat in deny_patterns:
        try:
            if re.search(pat, block, flags=re.I):
                return f"denyPattern:{pat}"
        except re.error:
            # If a regex is invalid, fail closed by blocking.
            return f"denyPatternInvalid:{pat}"
    return None


@dataclass
class Decision:
    accepted: bool
    reason: str
    score: int
    kind: str


def score_block(block: str, cfg: Dict) -> Decision:
    safety = cfg.get("safety", {})
    scoring = cfg.get("scoring", {})
    hi = int(scoring.get("highConfidenceScore", 4))

    deny = blocked_by_safety(block, safety.get("denyPatterns", []), safety.get("denyIfContains", []))
    if deny:
        return Decision(False, f"blocked:{deny}", score=-999, kind=extract_type(block))

    kind = extract_type(block)

    if kind == "procedural":
        pcfg = scoring.get("procedural", {})
        points = pcfg.get("points", {})
        score = 0
        if has_field(block, "source") or has_field(block, "evidence"):
            score += int(points.get("hasEvidence", 0))
        if has_field(block, "trigger"):
            score += int(points.get("hasTrigger", 0))
        if "verification:" in block.lower() or has_field(block, "verification"):
            score += int(points.get("hasVerification", 0))
        if has_steps(block):
            score += int(points.get("hasSteps", 0))

        if pcfg.get("requireTrigger", False):
            if not has_field(block, "trigger"):
                return Decision(False, "missing:trigger", score=score, kind=kind)
            if not pcfg.get("allowTriggerPlaceholder", False):
                if re.search(r"^\s*-\s*trigger:\s*\(.*\)\s*$", block, flags=re.I | re.M):
                    return Decision(False, "placeholder:trigger", score=score, kind=kind)

        if pcfg.get("requireVerification", False):
            if "verification" not in block.lower():
                return Decision(False, "missing:verification", score=score, kind=kind)
            if not pcfg.get("allowVerificationPlaceholder", False):
                if re.search(r"^\s*-\s*verification:\s*\(.*\)\s*$", block, flags=re.I | re.M):
                    return Decision(False, "placeholder:verification", score=score, kind=kind)

        return Decision(score >= hi, "score" if score >= hi else "score-too-low", score=score, kind=kind)

    if kind == "semantic":
        scfg = scoring.get("semantic", {})
        points = scfg.get("points", {})
        score = 0
        has_ev = has_field(block, "evidence") or has_field(block, "source")
        if has_ev:
            score += int(points.get("hasEvidence", 0))
        if scfg.get("denyTimeBoundLanguage", False):
            phrases = scfg.get("timeBoundPhrases", [])
            if not contains_time_bound(block, phrases):
                score += int(points.get("noTimeBoundLanguage", 0))
            else:
                return Decision(False, "time-bound-language", score=score, kind=kind)
        if scfg.get("requireEvidence", False) and not has_ev:
            return Decision(False, "missing:evidence", score=score, kind=kind)

        return Decision(score >= hi, "score" if score >= hi else "score-too-low", score=score, kind=kind)

    # Episodic and unknown: not auto-promoted
    return Decision(False, f"kind:{kind}-not-auto", score=0, kind=kind)


def canonical_key(block: str) -> str:
    """Stable dedupe key for a block.

    We intentionally ignore volatile metadata that changes across runs (e.g. generated_at).
    This makes apply idempotent even if distill is re-run.
    """

    b = norm_block(block)
    # Drop volatile lines
    b = re.sub(r"(?im)^\s*-\s*generated_at\s*:\s*.*$\n?", "", b)
    # Normalize whitespace again after removals
    b = norm_block(b)
    return sha256_text(b.strip())


def merge_into_topic(dest_path: Path, new_blocks: List[str]) -> Tuple[int, int, str, str, str, int]:
    before = read_text(dest_path)
    before_hash = sha256_text(before)

    existing_blocks = split_blocks(before)
    existing_keys = {canonical_key(b) for b in existing_blocks if b.lstrip().startswith("##")}

    existing = before
    added = 0
    skipped_existing = 0

    for b in new_blocks:
        if not b.lstrip().startswith("##"):
            continue
        key = canonical_key(b)
        if key in existing_keys:
            skipped_existing += 1
            continue
        b_norm = norm_block(b)
        if existing and not existing.endswith("\n"):
            existing += "\n"
        existing += b_norm
        existing_keys.add(key)
        added += 1

    after_hash = sha256_text(existing)
    return (len(split_blocks(before)), len(split_blocks(existing)), before_hash, after_hash, existing, skipped_existing)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", help="Workspace root (default: auto-detected)")
    ap.add_argument("--config", default="memory-architecture/config/auto-merge.json")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    global WORKSPACE
    if args.workspace:
        WORKSPACE = Path(args.workspace).expanduser().resolve()

    cfg_path = WORKSPACE / args.config
    if not cfg_path.exists():
        # Fallback: config shipped with the skill (memory-architecture/config)
        fallback = Path(__file__).resolve().parents[1] / "config" / Path(args.config).name
        if fallback.exists():
            cfg_path = fallback

    cfg = json.loads(read_text(cfg_path) or "{}")

    apply_cfg = cfg.get("apply", {})
    targets = cfg.get("targets", {})

    src_topics = WORKSPACE / apply_cfg.get("sourceDedupedTopicsDir", "memory/staging/deduped/topics")
    dst_topics = WORKSPACE / targets.get("topicsDir", "memory/topics")

    src_mem_candidates = WORKSPACE / apply_cfg.get(
        "sourceDedupedMemoryCandidates", "memory/staging/deduped/MEMORY.candidates.md"
    )
    dst_memory = WORKSPACE / targets.get("memoryFile", "MEMORY.md")

    manifests_dir = WORKSPACE / apply_cfg.get("manifestsDir", "memory/staging/manifests")
    manifests_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        args.write = False

    run_ts = now_z()

    manifest: Dict = {
        "run_ts": run_ts,
        "config": str(cfg_path) if not str(cfg_path).startswith(str(WORKSPACE)) else str(cfg_path.relative_to(WORKSPACE)),
        "write": bool(args.write),
        "applied": [],
        "skipped": [],
    }

    telemetry_path = WORKSPACE / "state" / "memory-recall-events.jsonl"
    session_key = env_session_key()
    append_jsonl(
        telemetry_path,
        {
            "type": "maintenance.apply_staging.start",
            "ts": run_ts,
            "session": session_key,
            "config": manifest["config"],
            "write": bool(args.write),
        },
    )

    if not src_topics.exists():
        manifest["error"] = f"missing source topics dir: {src_topics.relative_to(WORKSPACE)}"
        out = manifests_dir / f"apply-{run_ts}.json"
        write_text(out, json.dumps(manifest, indent=2) + "\n")
        print(json.dumps(manifest, indent=2))
        return

    # Apply topic candidates
    for src in sorted(src_topics.glob("*.md")):
        topic_name = src.stem
        dest = dst_topics / f"{topic_name}.md"

        blocks = split_blocks(read_text(src))
        candidate_blocks = [b for b in blocks if b.lstrip().startswith("##")]

        accepted: List[str] = []
        for b in candidate_blocks:
            dec = score_block(b, cfg)
            entry = {
                "source": str(src.relative_to(WORKSPACE)),
                "topic": topic_name,
                "kind": dec.kind,
                "score": dec.score,
                "decision": "accept" if dec.accepted else "skip",
                "reason": dec.reason,
                "block_sha256": sha256_text(norm_block(b)),
            }
            if dec.accepted:
                accepted.append(b)
                manifest["applied"].append(entry)
            else:
                manifest["skipped"].append(entry)

        if accepted:
            before_blocks, after_blocks, h_before, h_after, merged, skipped_existing = merge_into_topic(dest, accepted)
            file_entry = {
                "dest": str(dest.relative_to(WORKSPACE)),
                "before_blocks": before_blocks,
                "after_blocks": after_blocks,
                "before_sha256": h_before,
                "after_sha256": h_after,
                "skipped_existing": skipped_existing,
            }
            manifest.setdefault("dest_files", []).append(file_entry)
            if args.write:
                write_text(dest, merged)

    # Apply MEMORY semantic candidates (stricter gating)
    if src_mem_candidates.exists():
        mem_blocks = split_blocks(read_text(src_mem_candidates))
        mem_candidate_blocks = [b for b in mem_blocks if b.lstrip().startswith("##")]

        mem_accepted: List[str] = []
        for b in mem_candidate_blocks:
            dec = score_block(b, cfg)
            # Only allow semantic blocks into MEMORY.md
            if dec.kind != "semantic":
                dec = Decision(False, f"memory-only-semantic (was {dec.kind})", dec.score, dec.kind)

            entry = {
                "source": str(src_mem_candidates.relative_to(WORKSPACE)),
                "topic": "MEMORY.md",
                "kind": dec.kind,
                "score": dec.score,
                "decision": "accept" if dec.accepted else "skip",
                "reason": dec.reason,
                "block_sha256": sha256_text(norm_block(b)),
            }
            if dec.accepted:
                mem_accepted.append(b)
                manifest["applied"].append(entry)
            else:
                manifest["skipped"].append(entry)

        if mem_accepted:
            before_blocks, after_blocks, h_before, h_after, merged, skipped_existing = merge_into_topic(dst_memory, mem_accepted)
            file_entry = {
                "dest": str(dst_memory.relative_to(WORKSPACE)),
                "before_blocks": before_blocks,
                "after_blocks": after_blocks,
                "before_sha256": h_before,
                "after_sha256": h_after,
                "skipped_existing": skipped_existing,
            }
            manifest.setdefault("dest_files", []).append(file_entry)
            if args.write:
                write_text(dst_memory, merged)

    # Ensure dest_files exists even when no writes occurred (rollback tooling expects it)
    manifest.setdefault("dest_files", [])

    out_manifest = manifests_dir / f"apply-{run_ts}.json"
    write_text(out_manifest, json.dumps(manifest, indent=2) + "\n")

    append_jsonl(
        telemetry_path,
        {
            "type": "maintenance.apply_staging.complete",
            "ts": now_z(),
            "session": session_key,
            "manifest": str(out_manifest.relative_to(WORKSPACE)),
            "write": bool(args.write),
            "applied": len(manifest["applied"]),
            "skipped": len(manifest["skipped"]),
        },
    )

    cfg_disp = str(cfg_path) if not str(cfg_path).startswith(str(WORKSPACE)) else str(cfg_path.relative_to(WORKSPACE))
    print(f"Apply staging: write={args.write} config={cfg_disp}")
    print(f"Manifest: {out_manifest.relative_to(WORKSPACE)}")
    print(f"Applied blocks: {len(manifest['applied'])}; skipped blocks: {len(manifest['skipped'])}")


if __name__ == "__main__":
    main()
