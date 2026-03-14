#!/usr/bin/env python3
"""Session transcript distiller (staging-first).

See the canonical copy in:
- workspace/memory-architecture/scripts/distill_sessions.py

This skill-local copy exists so the Lucidity skill is self-contained.
"""

from __future__ import annotations

# Keep this file intentionally in sync with the canonical script.

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    from zoneinfo import ZoneInfo  # py3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

WORKSPACE = Path(__file__).resolve().parents[4]
MEMORY_DIR = WORKSPACE / "memory"
STAGING_DIR = MEMORY_DIR / "staging"
DEFAULT_SESSIONS_DIR = Path(os.path.expanduser("~/.openclaw/agents/main/sessions"))


def ensure_dirs() -> None:
    (STAGING_DIR / "sessions").mkdir(parents=True, exist_ok=True)
    (STAGING_DIR / "receipts").mkdir(parents=True, exist_ok=True)


def parse_ts(s: str) -> Optional[dt.datetime]:
    if not s:
        return None
    try:
        if s.endswith("Z"):
            return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.datetime.fromisoformat(s)
    except Exception:
        return None


def flatten_message_text(msg: Any, include_thinking: bool) -> str:
    if msg is None:
        return ""
    if isinstance(msg, str):
        return msg
    content = msg.get("content") if isinstance(msg, dict) else None
    if isinstance(content, list):
        parts: List[str] = []
        for c in content:
            if not isinstance(c, dict):
                continue
            if isinstance(c.get("text"), str):
                parts.append(c["text"])
            if include_thinking and isinstance(c.get("thinking"), str):
                parts.append(c["thinking"])
        return "\n".join([p for p in parts if p.strip()])
    if isinstance(msg, dict) and isinstance(msg.get("text"), str):
        return msg["text"]
    return ""


def iter_jsonl(fp: Path) -> Iterable[Dict[str, Any]]:
    for line in fp.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if isinstance(obj, dict):
            yield obj


def extract_events(
    sessions_dir: Path,
    since: Optional[dt.datetime],
    until: Optional[dt.datetime],
    keyword_re: Optional[re.Pattern[str]],
    include_tool_results: bool,
    include_thinking: bool,
    tz_offset_minutes: int,
    max_events: int,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    stats = {
        "files_scanned": 0,
        "events_seen": 0,
        "events_in_window": 0,
        "events_selected": 0,
        "tool_results_skipped": 0,
        "thinking_stripped": 0,
    }

    for fp in sorted(sessions_dir.glob("*.jsonl")):
        stats["files_scanned"] += 1
        for obj in iter_jsonl(fp):
            stats["events_seen"] += 1
            ts_raw = obj.get("timestamp") or obj.get("ts") or obj.get("time") or obj.get("createdAt")
            ts = parse_ts(ts_raw) if isinstance(ts_raw, str) else None
            if ts is None:
                continue
            if since and ts < since:
                continue
            if until and ts >= until:
                continue
            stats["events_in_window"] += 1

            msg = obj.get("message")
            role = msg.get("role") if isinstance(msg, dict) else None
            if role == "toolResult" and not include_tool_results:
                stats["tool_results_skipped"] += 1
                continue

            text = flatten_message_text(msg, include_thinking=include_thinking)
            if not include_thinking and isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "thinking" for c in content):
                    stats["thinking_stripped"] += 1

            blob = text if text else json.dumps(obj, ensure_ascii=False)[:2000]
            if keyword_re and not keyword_re.search(blob):
                continue

            events.append(
                {
                    "timestamp": ts.isoformat(),
                    "role": role or obj.get("type") or "event",
                    "text": text.strip(),
                    "sourceFile": fp.name,
                }
            )
            stats["events_selected"] += 1
            if len(events) >= max_events:
                return events, stats

    return events, stats


def write_sessions_md(out_path: Path, title: str, events: List[Dict[str, Any]], meta: Dict[str, Any]) -> None:
    lines: List[str] = []
    lines.append(f"# {title}\n")
    lines.append("(Generated from OpenClaw session transcripts; review before promoting. Tool results may be omitted.)\n")
    lines.append("## Metadata\n")
    lines.append("```json")
    lines.append(json.dumps(meta, indent=2))
    lines.append("```\n")
    lines.append("## Extracted events\n")

    for ev in events:
        ts = ev.get("timestamp", "")
        role = ev.get("role", "")
        src = ev.get("sourceFile", "")
        lines.append(f"### {ts} | {role} | {src}\n")
        lines.append("```")
        t = ev.get("text") or "[no extracted text]"
        if len(t) > 4000:
            t = t[:4000] + "…"
        lines.append(t)
        lines.append("```\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-dir", default=str(DEFAULT_SESSIONS_DIR))
    ap.add_argument("--date", help="YYYY-MM-DD (local day if tz offset set)")
    ap.add_argument("--since", help="ISO timestamp (inclusive)")
    ap.add_argument("--until", help="ISO timestamp (exclusive)")
    ap.add_argument("--since-days", type=int, help="Look back N days from now")
    ap.add_argument("--keyword-regex", help="Only include events whose extracted text matches regex")
    ap.add_argument("--include-tool-results", action="store_true")
    ap.add_argument("--include-thinking", action="store_true")
    ap.add_argument("--tz", help="IANA timezone name for day bucketing (e.g. America/New_York)")
    ap.add_argument("--tz-offset-minutes", type=int, default=0, help="Legacy; prefer --tz")
    ap.add_argument("--max-events", type=int, default=4000)
    args = ap.parse_args()

    sessions_dir = Path(args.sessions_dir).expanduser().resolve()
    if not sessions_dir.exists():
        raise SystemExit(f"sessions dir not found: {sessions_dir}")

    ensure_dirs()
    (STAGING_DIR / "reports").mkdir(parents=True, exist_ok=True)

    now = dt.datetime.now(dt.UTC)
    since: Optional[dt.datetime] = None
    until: Optional[dt.datetime] = None

    if args.since_days is not None:
        since = now - dt.timedelta(days=args.since_days)
    if args.since:
        since = parse_ts(args.since)
    if args.until:
        until = parse_ts(args.until)

    if args.date:
        d = dt.date.fromisoformat(args.date)
        if args.tz:
            if ZoneInfo is None:
                raise SystemExit("zoneinfo unavailable; use --tz-offset-minutes instead")
            tz = ZoneInfo(args.tz)
            local_start = dt.datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=tz)
            local_end = local_start + dt.timedelta(days=1)
            since = local_start.astimezone(dt.UTC)
            until = local_end.astimezone(dt.UTC)
        else:
            since = dt.datetime(d.year, d.month, d.day, tzinfo=dt.UTC)
            until = since + dt.timedelta(days=1)

    keyword_re = re.compile(args.keyword_regex, flags=re.I) if args.keyword_regex else None

    events, stats = extract_events(
        sessions_dir=sessions_dir,
        since=since,
        until=until,
        keyword_re=keyword_re,
        include_tool_results=args.include_tool_results,
        include_thinking=args.include_thinking,
        tz_offset_minutes=args.tz_offset_minutes,
        max_events=args.max_events,
    )

    tag = args.date or (since.date().isoformat() if since else now.date().isoformat())
    out_md = STAGING_DIR / "sessions" / f"{tag}.sessions.md"
    out_json = STAGING_DIR / "reports" / f"sessions-{tag}.meta.json"

    meta = {
        "generated_at": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "sessions_dir": str(sessions_dir),
        "date": args.date,
        "since": since.isoformat() if since else None,
        "until": until.isoformat() if until else None,
        "keyword_regex": args.keyword_regex,
        "include_tool_results": args.include_tool_results,
        "include_thinking": args.include_thinking,
        "tz": args.tz,
        "tz_offset_minutes": args.tz_offset_minutes,
        "stats": stats,
        "selected_events": len(events),
    }

    write_sessions_md(out_md, title=f"Session Extract: {tag}", events=events, meta=meta)
    out_json.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote: {out_md.relative_to(WORKSPACE)}")
    print(f"Meta:  {out_json.relative_to(WORKSPACE)}")
    print(f"Selected events: {len(events)}")


if __name__ == "__main__":
    main()
