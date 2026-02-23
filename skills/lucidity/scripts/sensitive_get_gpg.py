#!/usr/bin/env python3
"""Lucidity - decrypt sensitive text encrypted with GPG.

Usage:
  python3 skills/lucidity/scripts/sensitive_get_gpg.py --in path/to/file.gpg

You can also write decrypted output to a file:
  python3 skills/lucidity/scripts/sensitive_get_gpg.py --in file.gpg --out -

IMPORTANT:
- Treat decrypted output as sensitive. Do not paste into always-loaded tiers.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True, help="Input .gpg path")
    ap.add_argument("--out", default="-", help="Output path or '-' for stdout")
    args = ap.parse_args()

    in_path = Path(args.in_path).expanduser()
    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")

    cmd = ["gpg", "--batch", "--decrypt", str(in_path)]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf-8", errors="replace"))
        raise SystemExit(p.returncode)

    if args.out == "-":
        sys.stdout.buffer.write(p.stdout)
    else:
        out_path = Path(args.out).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(p.stdout)


if __name__ == "__main__":
    main()
