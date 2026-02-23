#!/usr/bin/env python3
"""Regression test: apply_staging is idempotent (no duplicates across repeated runs).

Creates a temporary workspace-like directory with:
- memory/staging/deduped/topics/demo.md containing a procedural block
- memory/topics/ as target

Runs apply twice with --write and verifies the destination file hash is unchanged
after the second run.

Usage:
  python3 memory-architecture/scripts/test_apply_idempotency.py
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
WORKSPACE = HERE.parents[2]
APPLY = WORKSPACE / "memory-architecture" / "scripts" / "apply_staging.py"
CFG = WORKSPACE / "memory-architecture" / "config" / "auto-merge.json"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td) / "workspace"
        (ws / "memory-architecture" / "scripts").mkdir(parents=True, exist_ok=True)
        (ws / "memory-architecture" / "config").mkdir(parents=True, exist_ok=True)
        (ws / "memory" / "staging" / "deduped" / "topics").mkdir(parents=True, exist_ok=True)
        (ws / "memory" / "topics").mkdir(parents=True, exist_ok=True)
        (ws / "state").mkdir(parents=True, exist_ok=True)

        # Copy apply + telemetry helper into temp workspace
        shutil.copy2(APPLY, ws / "memory-architecture" / "scripts" / "apply_staging.py")
        shutil.copy2(WORKSPACE / "memory-architecture" / "scripts" / "telemetry.py", ws / "memory-architecture" / "scripts" / "telemetry.py")
        shutil.copy2(CFG, ws / "memory-architecture" / "config" / "auto-merge.json")

        demo = ws / "memory" / "staging" / "deduped" / "topics" / "demo.md"
        demo.write_text(
            "# Topic Candidate: demo\n\n"
            "## Procedure (candidate): Demo\n\n"
            "- type: procedural\n"
            "- source: memory/2099-01-01.md#Demo\n"
            "- trigger: when running a demo\n"
            "- verification: it works\n"
            "- generated_at: 2099-01-01T00:00:00Z\n\n"
            "1) Do thing\n"
            "2) Verify thing\n\n",
            encoding="utf-8",
        )

        # Run apply twice
        cmd = ["python3", "memory-architecture/scripts/apply_staging.py", "--config", "memory-architecture/config/auto-merge.json", "--write"]
        run(cmd, ws)
        out = ws / "memory" / "topics" / "demo.md"
        h1 = sha256_file(out)

        # Modify only generated_at in staging (should still be idempotent)
        demo.write_text(demo.read_text(encoding="utf-8").replace("2099-01-01T00:00:00Z", "2099-01-01T00:00:01Z"), encoding="utf-8")

        run(cmd, ws)
        h2 = sha256_file(out)

        if h1 != h2:
            raise SystemExit(f"FAIL: apply not idempotent (hash changed)\n{h1}\n{h2}")

        print("PASS: apply_staging idempotent")


if __name__ == "__main__":
    main()
