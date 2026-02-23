#!/usr/bin/env python3
"""Lucidity update check (notification-only).

This script checks whether the local checkout is behind the latest GitHub tag.

- It does NOT update code.
- It is safe to run from cron.

Usage:
  python3 skills/lucidity/scripts/check_update.py

Exit codes:
- 0: up to date (or best-effort check could not determine)
- 10: update available
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[3]


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def local_version() -> Optional[str]:
    vpath = REPO_ROOT / "VERSION"
    if vpath.exists():
        return vpath.read_text(encoding="utf-8").strip() or None
    return None


def latest_tag_via_gh() -> Optional[str]:
    if run(["bash", "-lc", "command -v gh >/dev/null 2>&1"]).returncode != 0:
        return None
    # Use `gh api` to avoid parsing human output.
    p = run([
        "gh",
        "api",
        "repos/Gottschling-Labs/lucidity/releases/latest",
        "--jq",
        ".tag_name",
    ])
    if p.returncode == 0:
        tag = (p.stdout or "").strip()
        return tag or None

    # Fallback: latest tag by ref listing
    p2 = run([
        "gh",
        "api",
        "repos/Gottschling-Labs/lucidity/tags",
        "--jq",
        ".[0].name",
    ])
    if p2.returncode == 0:
        tag = (p2.stdout or "").strip()
        return tag or None
    return None


def normalize_tag(tag: str) -> str:
    return tag[1:] if tag.startswith("v") else tag


def main() -> None:
    lv = local_version()
    rt = latest_tag_via_gh()

    out = {
        "repo": "Gottschling-Labs/lucidity",
        "localVersion": lv,
        "latestTag": rt,
    }

    # If we cannot determine latest tag, do not fail.
    if not rt:
        out["status"] = "unknown"
        print(json.dumps(out, indent=2))
        raise SystemExit(0)

    latest = normalize_tag(rt)
    out["latestVersion"] = latest

    if lv and lv != latest:
        out["status"] = "update-available"
        out["recommended"] = {
            "commands": [
                "cd ~/code/gottschling-labs/lucidity",
                "git pull --ff-only",
                "./skills/lucidity/install.sh  # to refresh cron block if needed",
            ]
        }
        print(json.dumps(out, indent=2))
        raise SystemExit(10)

    out["status"] = "up-to-date"
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
