#!/usr/bin/env python3
"""Workspace-bundled memory backup with 7/30/90 retention.

Creates:
- memory/backups/YYYY/MM/backup-<ts>.tar.gz
- memory/backups/YYYY/MM/backup-<ts>.manifest.json

Retention:
- keep last 7 backups (daily)
- keep last 30 ISO-week buckets (one per week)
- keep last 90 month buckets (one per month)

Included paths are workspace-relative and centered on the memory system.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

WORKSPACE = Path.cwd()
MEMORY_DIR = WORKSPACE / "memory"
BACKUP_ROOT = MEMORY_DIR / "backups"

INCLUDE_GLOBS = [
    "MEMORY.md",
    "memory/*.md",
    "memory/topics/**/*.md",
    "memory/staging/**",
    "memory/sensitive/**",
]

EXCLUDE_PREFIXES = [
    "memory/backups/",
]


def now_z() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_excluded(rel: str) -> bool:
    return any(rel.startswith(pref) for pref in EXCLUDE_PREFIXES)


def iter_files() -> List[Path]:
    files: List[Path] = []
    for g in INCLUDE_GLOBS:
        for p in WORKSPACE.glob(g):
            if p.is_dir():
                continue
            rel = str(p.relative_to(WORKSPACE)).replace("\\", "/")
            if is_excluded(rel):
                continue
            files.append(p)
    # de-dupe while preserving order
    seen = set()
    out: List[Path] = []
    for p in sorted(files):
        r = str(p)
        if r not in seen:
            seen.add(r)
            out.append(p)
    return out


@dataclass
class BackupEntry:
    path: str
    bytes: int
    mtime: str
    sha256: str


def build_manifest(file_list: List[Path], ts: str) -> Dict:
    entries: List[Dict] = []
    for p in file_list:
        st = p.stat()
        mtime = dt.datetime.fromtimestamp(st.st_mtime, tz=dt.UTC).isoformat().replace("+00:00", "Z")
        entries.append(
            {
                "path": str(p.relative_to(WORKSPACE)).replace("\\", "/"),
                "bytes": st.st_size,
                "mtime": mtime,
                "sha256": sha256_file(p),
            }
        )
    return {
        "type": "memory.backup.manifest",
        "ts": ts,
        "workspace": str(WORKSPACE),
        "files": entries,
    }


def write_backup(file_list: List[Path], out_tar: Path) -> None:
    out_tar.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(out_tar, "w:gz") as tf:
        for p in file_list:
            arcname = str(p.relative_to(WORKSPACE)).replace("\\", "/")
            tf.add(p, arcname=arcname, recursive=False)


def parse_backup_ts(name: str) -> Optional[dt.datetime]:
    # backup-<ISO>Z.tar.gz
    if not name.startswith("backup-"):
        return None
    core = name[len("backup-") :]
    core = core.replace(".tar.gz", "")
    try:
        if core.endswith("Z"):
            core = core[:-1] + "+00:00"
        return dt.datetime.fromisoformat(core)
    except Exception:
        return None


def list_backups() -> List[Tuple[dt.datetime, Path]]:
    if not BACKUP_ROOT.exists():
        return []
    out: List[Tuple[dt.datetime, Path]] = []
    for p in BACKUP_ROOT.rglob("backup-*.tar.gz"):
        ts = parse_backup_ts(p.name)
        if ts:
            out.append((ts, p))
    out.sort(key=lambda x: x[0])
    return out


def retention_sets(backups: List[Tuple[dt.datetime, Path]], keep_daily: int, keep_weekly: int, keep_monthly: int) -> set[Path]:
    # Daily: last N
    keep: set[Path] = set(p for _, p in backups[-keep_daily:]) if keep_daily > 0 else set()

    # Weekly: keep most recent backup per ISO week, last M weeks
    week_map: Dict[Tuple[int, int], Tuple[dt.datetime, Path]] = {}
    for ts, p in backups:
        iso_year, iso_week, _ = ts.isocalendar()
        k = (iso_year, iso_week)
        if (k not in week_map) or (ts > week_map[k][0]):
            week_map[k] = (ts, p)
    weeks = sorted(week_map.items(), key=lambda kv: kv[1][0])
    for _, (_, p) in weeks[-keep_weekly:]:
        keep.add(p)

    # Monthly: keep most recent backup per month, last K months
    month_map: Dict[Tuple[int, int], Tuple[dt.datetime, Path]] = {}
    for ts, p in backups:
        k = (ts.year, ts.month)
        if (k not in month_map) or (ts > month_map[k][0]):
            month_map[k] = (ts, p)
    months = sorted(month_map.items(), key=lambda kv: kv[1][0])
    for _, (_, p) in months[-keep_monthly:]:
        keep.add(p)

    return keep


def prune(backups: List[Tuple[dt.datetime, Path]], keep: set[Path], write: bool) -> List[Path]:
    removed: List[Path] = []
    for _, p in backups:
        if p in keep:
            continue
        manifest = p.with_suffix("").with_suffix("")  # remove .gz then .tar
        mpath = p.parent / (p.name.replace(".tar.gz", ".manifest.json"))
        if write:
            try:
                p.unlink(missing_ok=True)
            except TypeError:
                if p.exists():
                    p.unlink()
            if mpath.exists():
                mpath.unlink()
        removed.append(p)
    return removed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Write backup and prune old backups")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep-daily", type=int, default=7)
    ap.add_argument("--keep-weekly", type=int, default=30)
    ap.add_argument("--keep-monthly", type=int, default=90)
    args = ap.parse_args()

    if args.dry_run:
        args.write = False

    ts = now_z()
    out_dir = BACKUP_ROOT / f"{dt.datetime.now(dt.UTC).year:04d}" / f"{dt.datetime.now(dt.UTC).month:02d}"
    out_tar = out_dir / f"backup-{ts}.tar.gz"
    out_manifest = out_dir / f"backup-{ts}.manifest.json"

    files = iter_files()
    manifest = build_manifest(files, ts)

    if args.write:
        write_backup(files, out_tar)
        out_manifest.parent.mkdir(parents=True, exist_ok=True)
        out_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    backups = list_backups() + ([(dt.datetime.fromisoformat(ts.replace('Z','+00:00')), out_tar)] if args.write else [])
    backups.sort(key=lambda x: x[0])

    keep = retention_sets(backups, args.keep_daily, args.keep_weekly, args.keep_monthly)
    removed = prune(backups, keep, write=args.write)

    report = {
        "ts": ts,
        "write": bool(args.write),
        "backup": str(out_tar.relative_to(WORKSPACE)) if args.write else None,
        "manifest": str(out_manifest.relative_to(WORKSPACE)) if args.write else None,
        "fileCount": len(files),
        "kept": len(keep),
        "removed": [str(p.relative_to(WORKSPACE)) for p in removed],
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
