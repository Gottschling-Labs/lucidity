#!/usr/bin/env python3
"""Rollback an apply_staging run using its manifest.

This reverts *whole destination files* to their previous content captured at rollback time.

Important:
- apply_staging manifests currently include before/after hashes but not full file snapshots.
- Therefore, rollback requires a backup archive (recommended) or a baseline snapshot.

This v0 rollback uses the daily backup archives under `memory/backups/`:
- Locate the most recent backup taken before the apply manifest timestamp.
- Restore the destination files listed in the apply manifest from that backup.

Usage:
  python3 memory-architecture/scripts/rollback_apply.py --manifest memory/staging/manifests/apply-<ts>.json --write
  python3 memory-architecture/scripts/rollback_apply.py --manifest ...   # dry-run
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import tarfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WORKSPACE = Path.cwd()
BACKUPS = WORKSPACE / "memory" / "backups"


def parse_ts_z(s: str) -> dt.datetime:
    # expects ISO with Z
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return dt.datetime.fromisoformat(s)


def parse_backup_ts(name: str) -> Optional[dt.datetime]:
    if not name.startswith("backup-") or not name.endswith(".tar.gz"):
        return None
    core = name[len("backup-") :].replace(".tar.gz", "")
    try:
        if core.endswith("Z"):
            core = core[:-1] + "+00:00"
        return dt.datetime.fromisoformat(core)
    except Exception:
        return None


def list_backups() -> List[Tuple[dt.datetime, Path]]:
    if not BACKUPS.exists():
        return []
    out: List[Tuple[dt.datetime, Path]] = []
    for p in BACKUPS.rglob("backup-*.tar.gz"):
        ts = parse_backup_ts(p.name)
        if ts:
            out.append((ts, p))
    out.sort(key=lambda x: x[0])
    return out


def pick_backup(before: dt.datetime, backups: List[Tuple[dt.datetime, Path]]) -> Optional[Path]:
    candidates = [p for ts, p in backups if ts <= before]
    return candidates[-1] if candidates else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    mpath = WORKSPACE / args.manifest
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    run_ts = parse_ts_z(manifest["run_ts"])

    dest_files = [d["dest"] for d in manifest.get("dest_files", [])]
    if not dest_files:
        print("No dest_files in manifest; nothing to rollback")
        return

    backups = list_backups()
    bpath = pick_backup(run_ts, backups)
    if not bpath:
        raise SystemExit("No backup found before apply run; cannot rollback safely")

    report: Dict = {
        "manifest": str(mpath.relative_to(WORKSPACE)),
        "apply_ts": manifest["run_ts"],
        "backup": str(bpath.relative_to(WORKSPACE)),
        "write": bool(args.write),
        "restored": [],
        "missing": [],
    }

    with tarfile.open(bpath, "r:gz") as tf:
        members = {m.name: m for m in tf.getmembers()}
        for rel in dest_files:
            if rel not in members:
                report["missing"].append(rel)
                continue
            if args.write:
                outp = WORKSPACE / rel
                outp.parent.mkdir(parents=True, exist_ok=True)
                f = tf.extractfile(members[rel])
                assert f is not None
                outp.write_bytes(f.read())
            report["restored"].append(rel)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
