#!/usr/bin/env python3
"""Debate Orchestrator artifact persistence utilities.

Local-first, auditable transcript persistence.

This module does NOT run debates. It provides:
- run id creation
- transcript path conventions
- JSONL append writer

Intended to be used by the orchestrator once session orchestration is implemented.

Storage location (workspace-relative):
- debate-architecture/runs/<run_id>/
  - meta.json
  - transcript.jsonl
  - consensus.json

This follows the conventions described in:
- debate-architecture/templates/transcript-conventions.md
"""

from __future__ import annotations

import json
import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


def now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_run_id(prefix: str = "debate") -> str:
    # Human-ish sortable id: debate-YYYYMMDD-HHMMSSZ-<rand>
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    rand = secrets.token_hex(4)
    return f"{prefix}-{ts}-{rand}"


@dataclass
class RunPaths:
    workspace: Path
    run_id: str

    @property
    def run_dir(self) -> Path:
        return self.workspace / "debate-architecture" / "runs" / self.run_id

    @property
    def meta_json(self) -> Path:
        return self.run_dir / "meta.json"

    @property
    def transcript_jsonl(self) -> Path:
        return self.run_dir / "transcript.jsonl"

    @property
    def consensus_json(self) -> Path:
        return self.run_dir / "consensus.json"


def resolve_workspace(explicit: Optional[str] = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    # Default: assume script lives at <workspace>/skills/debate-orchestrator/scripts/
    return Path(__file__).resolve().parents[3]


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def init_run(workspace: Path, topic: str, rounds: int, model: str) -> RunPaths:
    run_id = new_run_id()
    rp = RunPaths(workspace=workspace, run_id=run_id)

    meta = {
        "run_id": run_id,
        "ts": now_z(),
        "topic": topic,
        "rounds": rounds,
        "model": model,
        "cwd": os.getcwd(),
        "status": "initialized",
    }
    write_json(rp.meta_json, meta)
    return rp
