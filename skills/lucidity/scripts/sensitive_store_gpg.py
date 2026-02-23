#!/usr/bin/env python3
"""Lucidity - store sensitive text encrypted with GPG.

This is an optional helper for deployments that want an encrypted-at-rest tier.

Requirements:
- `gpg` installed and configured on the host.

Usage:
  python3 skills/lucidity/scripts/sensitive_store_gpg.py \
    --out ~/.openclaw/workspace/memory/sensitive/example.txt.gpg \
    --recipient you@example.com \
    --in -

Notes:
- This script does not integrate with OpenClaw indexing automatically.
- Do not place decrypted secrets into always-loaded tiers.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], stdin_bytes: bytes | None = None) -> None:
    p = subprocess.run(cmd, input=stdin_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf-8", errors="replace"))
        raise SystemExit(p.returncode)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output .gpg path")
    ap.add_argument("--recipient", required=True, help="GPG recipient (key id or email)")
    ap.add_argument("--in", dest="in_path", default="-", help="Input file path or '-' for stdin")
    args = ap.parse_args()

    out_path = Path(args.out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.in_path == "-":
        data = sys.stdin.buffer.read()
    else:
        data = Path(args.in_path).expanduser().read_bytes()

    cmd = [
        "gpg",
        "--batch",
        "--yes",
        "--encrypt",
        "--recipient",
        args.recipient,
        "--output",
        str(out_path),
        "-",
    ]
    run(cmd, stdin_bytes=data)


if __name__ == "__main__":
    main()
