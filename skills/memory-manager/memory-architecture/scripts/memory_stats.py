#!/usr/bin/env python3
"""Lucidity /memory-stats: local observability snapshot.

This is a lightweight, dependency-free stats reporter intended to be wired to a
command/hook later. For now, it can be run manually or from cron.

Outputs JSON by default.

What it reports (workspace-relative):
- last backup archive + timestamp
- last apply manifest + timestamp + applied/skipped
- staging sizes (topics/receipts/reports/manifests)
- telemetry tail counts (maintenance.apply_staging.*)

Usage:
  python3 memory-architecture/scripts/memory_stats.py
  python3 memory-architecture/scripts/memory_stats.py --text
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WORKSPACE = Path.cwd()


def parse_ts_from_name(prefix: str, name: str, suffix: str) -> Optional[str]:
    if not name.startswith(prefix) or not name.endswith(suffix):
        return None
    core = name[len(prefix) : -len(suffix)]
    return core


def newest_file(pattern: str) -> Optional[Path]:
    paths = [Path(p) for p in glob.glob(str(WORKSPACE / pattern))]
    if not paths:
        return None
    paths.sort(key=lambda p: p.stat().st_mtime)
    return paths[-1]


def dir_size(p: Path) -> int:
    if not p.exists():
        return 0
    total = 0
    for f in p.rglob("*"):
        if f.is_file():
            total += f.stat().st_size
    return total


def count_events(jsonl: Path, types: List[str]) -> Dict[str, int]:
    out = {t: 0 for t in types}
    if not jsonl.exists():
        return out
    for line in jsonl.read_text(encoding="utf-8").splitlines():
        try:
            obj = json.loads(line)
        except Exception:
            continue
        t = obj.get("type")
        if t in out:
            out[t] += 1
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", action="store_true")
    args = ap.parse_args()

    last_backup = newest_file("memory/backups/**/backup-*.tar.gz")
    last_apply = newest_file("memory/staging/manifests/apply-*.json")

    apply_summary = None
    if last_apply and last_apply.exists():
        try:
            m = json.loads(last_apply.read_text(encoding="utf-8"))
            apply_summary = {
                "run_ts": m.get("run_ts"),
                "write": m.get("write"),
                "applied": len(m.get("applied", [])),
                "skipped": len(m.get("skipped", [])),
            }
        except Exception:
            apply_summary = {"error": "failed-to-parse"}

    telemetry = WORKSPACE / "state" / "memory-recall-events.jsonl"
    event_counts = count_events(
        telemetry,
        [
            "maintenance.apply_staging.start",
            "maintenance.apply_staging.complete",
        ],
    )

    staging = WORKSPACE / "memory" / "staging"
    stats = {
        "workspace": str(WORKSPACE),
        "now": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "lastBackup": str(last_backup.relative_to(WORKSPACE)) if last_backup else None,
        "lastApplyManifest": str(last_apply.relative_to(WORKSPACE)) if last_apply else None,
        "lastApply": apply_summary,
        "staging": {
            "exists": staging.exists(),
            "bytes": dir_size(staging),
            "topicsBytes": dir_size(staging / "topics"),
            "dedupedBytes": dir_size(staging / "deduped"),
            "receiptsBytes": dir_size(staging / "receipts"),
            "reportsBytes": dir_size(staging / "reports"),
            "manifestsBytes": dir_size(staging / "manifests"),
        },
        "telemetry": {
            "path": str(telemetry.relative_to(WORKSPACE)),
            "counts": event_counts,
        },
    }

    if args.text:
        print("Lucidity /memory-stats")
        print(f"- last backup: {stats['lastBackup']}")
        print(f"- last apply manifest: {stats['lastApplyManifest']}")
        if apply_summary and isinstance(apply_summary, dict):
            print(f"- last apply: applied={apply_summary.get('applied')} skipped={apply_summary.get('skipped')} write={apply_summary.get('write')}")
        print(f"- staging bytes: {stats['staging']['bytes']}")
        print(f"- telemetry: {stats['telemetry']['counts']}")
    else:
        print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
