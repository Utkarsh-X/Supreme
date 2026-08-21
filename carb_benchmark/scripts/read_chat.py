#!/usr/bin/env python3
"""Read the Freebuff chat database and print the AI model + human/AI chat.

The Freebuff desktop app stores every conversation in the SQLite database at
.freebuff/desktop-v2.db:

  * threads   - one row per chat thread (title, model, status, ...)
  * messages  - one row per chat message (role: user=human, assistant=AI)

Usage:
    python read_chat.py                # list all threads
    python read_chat.py --thread ID    # print one thread's full chat
    python read_chat.py --all          # print the full chat of every thread
    python read_chat.py --raw          # include reasoning / tool-call parts
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

# Windows consoles default to cp1252, which chokes on chat text containing
# characters like →. Emit UTF-8 (replacing anything unrepresentable).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_DB = Path(__file__).resolve().parent / ".freebuff" / "desktop-v2.db"

# Part kinds that carry the actual conversation (everything else is internal noise).
CHAT_KINDS = {"text"}


def _ts(ms: int) -> str:
    if not ms:
        return "?"
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _role_label(role: str) -> str:
    return {"user": "HUMAN", "assistant": "AI"}.get(role, role.upper())


def load_threads(db: Path) -> list[sqlite3.Row]:
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    return con.execute(
        """
        SELECT t.*,
               (SELECT COUNT(*) FROM messages m WHERE m.thread_id = t.id) AS message_count
        FROM threads t
        ORDER BY COALESCE(t.last_prompt_at, t.updated_at, t.created_at) DESC
        """
    ).fetchall()


def parts_text(parts_json: str, raw: bool = False) -> str:
    """Flatten a message's parts into readable text (chat-only unless --raw)."""
    try:
        parts = json.loads(parts_json or "[]")
    except json.JSONDecodeError:
        return parts_json or ""

    out = []
    for p in parts:
        kind = p.get("kind")
        if raw or kind in CHAT_KINDS:
            if kind == "tool":
                name = p.get("name") or p.get("toolName") or "tool"
                out.append(f"[tool: {name}]")
            elif kind == "reasoning":
                out.append("[reasoning]")
            else:
                out.append(p.get("text", ""))
    return "\n".join(t for t in out if t).strip()


def print_threads(db: Path) -> None:
    threads = load_threads(db)
    if not threads:
        print("No threads found in the database.")
        return
    print(f"Found {len(threads)} thread(s) in {db}\n")
    for i, t in enumerate(threads, 1):
        model = t["model"] or "(default model)"
        print(
            f"[{i}] {t['id']}\n"
            f"    title : {t['title']}\n"
            f"    model : {model}\n"
            f"    status: {t['status']}  |  messages: {t['message_count']}  |  "
            f"updated: {_ts(t['updated_at'] or t['created_at'])}\n"
        )


def print_thread(db: Path, thread: sqlite3.Row, raw: bool = False) -> None:
    print("=" * 80)
    print(f"THREAD: {thread['title']}")
    print(f"  id       : {thread['id']}")
    print(f"  model    : {thread['model'] or '(default model)'}")
    print(f"  status   : {thread['status']}")
    print(f"  project  : {thread['project_path']}")
    print(f"  branch   : {thread['branch'] or '(none)'}")
    print("=" * 80)

    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT * FROM messages WHERE thread_id = ? ORDER BY seq", (thread["id"],)
    ).fetchall()
    if not rows:
        print("(no messages in this thread)")
        return

    for m in rows:
        text = parts_text(m["parts_json"], raw=raw)
        if not text and not raw:
            continue
        print(f"\n----- {_role_label(m['role'])}  [{_ts(m['ts'])}] -----")
        print(text)
    print()


def main() -> None:
    ap = argparse.ArgumentParser(description="Read the Freebuff chat database.")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="path to desktop-v2.db")
    ap.add_argument("--thread", help="thread id (or index from the list) to print")
    ap.add_argument("--all", action="store_true", help="print the full chat of every thread")
    ap.add_argument("--raw", action="store_true", help="also show reasoning/tool-call parts")
    args = ap.parse_args()

    db = Path(args.db)
    if not db.exists():
        ap.error(f"database not found: {db}")

    threads = load_threads(db)
    if args.thread:
        match = next(
            (t for t in threads if t["id"] == args.thread),
            None,
        )
        if match is None and args.thread.isdigit():
            idx = int(args.thread) - 1
            if 0 <= idx < len(threads):
                match = threads[idx]
        if match is None:
            ap.error(f"no thread found for {args.thread!r} (use `python read_chat.py` to list them)")
        print_thread(db, match, raw=args.raw)
    elif args.all:
        for t in threads:
            print_thread(db, t, raw=args.raw)
    else:
        print_threads(db)
        print("Tip: pass --thread <id> (or list index) to read a chat, or --all for everything.")


if __name__ == "__main__":
    main()
