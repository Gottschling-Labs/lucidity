#!/usr/bin/env python3
"""Archive (prune) staging artifacts without data loss.

Moves files older than N days from `memory/staging/**` into
`memory/archive/staging/YYYY/MM/...` with a manifest.

Canonical memory files are never touched.

Usage:
  python3 memory-architecture/scripts/prune_staging.py --days 14 --write
  python3 memory-architecture/scripts/prune_staging.py --days 14   # dry run
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List

WORKSPACE = Path(__file__).resolve().parents[2]
MEMORY = WORKSPACE / "memory"
STAGING = MEMORY / "staging"
ARCHIVE_ROOT = MEMORY / "archive" / "staging"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def month_bucket(ts: dt.datetime) -> Path:
    return ARCHIVE_ROOT / f"{ts.year:04d}" / f"{ts.month:02d}"


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", help="Workspace root (default: auto-detected)")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    global WORKSPACE, MEMORY, STAGING, ARCHIVE_ROOT
    if args.workspace:
        WORKSPACE = Path(args.workspace).expanduser().resolve()
        MEMORY = WORKSPACE / "memory"
        STAGING = MEMORY / "staging"
        ARCHIVE_ROOT = MEMORY / "archive" / "staging"

    if not STAGING.exists():
        print("No staging directory; nothing to prune")
        return

    now = dt.datetime.now(dt.UTC)
    cutoff = now - dt.timedelta(days=args.days)

    moved: List[Dict] = []
    skipped: List[Dict] = []

    for p in sorted(STAGING.rglob("*")):
        if p.is_dir():
            continue
        if p.name == ".gitkeep":
            continue
        if not is_under(p, STAGING):
            continue

        st = p.stat()
        mtime = dt.datetime.fromtimestamp(st.st_mtime, tz=dt.UTC)
        if mtime >= cutoff:
            continue

        rel = p.relative_to(STAGING)
        bucket = month_bucket(mtime)
        dest = bucket / rel
        dest.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "source": str(p.relative_to(WORKSPACE)),
            "dest": str(dest.relative_to(WORKSPACE)),
            "bytes": st.st_size,
            "mtime": mtime.isoformat().replace("+00:00", "Z"),
            "sha256": sha256_file(p),
        }

        if dest.exists():
            # Avoid overwrite; keep the existing dest and skip.
            skipped.append({**entry, "reason": "dest-exists"})
            continue

        if args.write:
            p.rename(dest)
            if not dest.exists():
                raise SystemExit(f"Move failed: {p} -> {dest}")
            moved.append(entry)
        else:
            moved.append({**entry, "dry_run": True})

    # Write manifest even in dry-run (useful audit)
    run_ts = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    bucket = month_bucket(now)
    manifest_dir = bucket / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"prune-{run_ts}.json"

    manifest = {
        "run_ts": run_ts,
        "cutoff": cutoff.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "days": args.days,
        "write": bool(args.write),
        "moved": moved,
        "skipped": skipped,
    }

    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"Prune staging: days={args.days} write={args.write}")
    print(f"Moved candidates: {len(moved)} (skipped {len(skipped)})")
    print(f"Manifest: {manifest_path.relative_to(WORKSPACE)}")


if __name__ == "__main__":
    main()
