"""Tiny JSONL telemetry helper for memory architecture.

Writes append-only JSON lines under `workspace/state/`.

We keep this dependency-free and intentionally simple.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(obj, ensure_ascii=False)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def env_session_key() -> str | None:
    # Best-effort. Cron/agent runs may not expose this.
    return os.environ.get("OPENCLAW_SESSION_KEY")
