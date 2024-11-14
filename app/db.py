# -*- coding: utf-8 -*-
"""Tầng dữ liệu SQLite: đơn hàng mẫu, phiên hội thoại, tin nhắn, ticket, KB, câu chưa giải quyết."""
import os
import sqlite3
import threading
from contextlib import contextmanager

from .data import KB_SEED, ORDERS_SEED

DB_PATH = os.environ.get("HELPDESK_DB", os.path.join(os.path.dirname(__file__), "..", "data", "helpdesk.db"))

_lock = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    code TEXT PRIMARY KEY, phone TEXT NOT NULL, customer TEXT, product TEXT,
    qty INTEGER, total INTEGER, status TEXT, tracking TEXT DEFAULT '',
    eta TEXT DEFAULT '', created TEXT
);
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY, state TEXT DEFAULT 'IDLE', pending_order TEXT DEFAULT '',
    pending_phone TEXT DEFAULT '', fallback_count INTEGER DEFAULT 0,
    handoff INTEGER DEFAULT 0, handoff_reason TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, role TEXT,
    content TEXT, intent TEXT DEFAULT '', confidence REAL DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, session_id TEXT,
    content TEXT, status TEXT DEFAULT 'OPEN',
    created_at TEXT DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS kb_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT, intent TEXT, question TEXT, answer TEXT
);
CREATE TABLE IF NOT EXISTS unresolved (
    id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, question TEXT,
    created_at TEXT DEFAULT (datetime('now','localtime'))
);
"""


def _connect():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db():
    with _lock:
        conn = _connect()
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()


def init_db():
    with get_db() as conn:
        conn.executescript(SCHEMA)
        if conn.execute("SELECT COUNT(*) c FROM orders").fetchone()["c"] == 0:
            conn.executemany(
                "INSERT INTO orders VALUES (:code,:phone,:customer,:product,:qty,:total,:status,:tracking,:eta,:created)",
                ORDERS_SEED)
        if conn.execute("SELECT COUNT(*) c FROM kb_entries").fetchone()["c"] == 0:
            conn.executemany("INSERT INTO kb_entries (intent,question,answer) VALUES (:intent,:question,:answer)", KB_SEED)


def find_order(code):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM orders WHERE code=?", (code.upper(),)).fetchone()
        return dict(row) if row else None


def get_session(session_id):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
        if row is None:
            conn.execute("INSERT INTO sessions (id) VALUES (?)", (session_id,))
            row = conn.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
        return dict(row)


def update_session(session_id, **fields):
    if not fields:
        return
    sets = ", ".join(f"{k}=?" for k in fields)
    with get_db() as conn:
        conn.execute(f"UPDATE sessions SET {sets} WHERE id=?", (*fields.values(), session_id))


def log_message(session_id, role, content, intent="", confidence=0.0):
    with get_db() as conn:
        conn.execute("INSERT INTO messages (session_id,role,content,intent,confidence) VALUES (?,?,?,?,?)",
                     (session_id, role, content, intent, confidence))


def log_unresolved(session_id, question):
    with get_db() as conn:
        conn.execute("INSERT INTO unresolved (session_id,question) VALUES (?,?)", (session_id, question))


def create_ticket(session_id, content):
    with get_db() as conn:
        cur = conn.execute("INSERT INTO tickets (session_id,content,code) VALUES (?,?,?)",
                           (session_id, content, "TEMP"))
        tid = cur.lastrowid
        code = f"TC{tid:06d}"
        conn.execute("UPDATE tickets SET code=? WHERE id=?", (code, tid))
        return code


def kb_all():
    with get_db() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM kb_entries ORDER BY id")]


def kb_add(intent, question, answer):
    with get_db() as conn:
        cur = conn.execute("INSERT INTO kb_entries (intent,question,answer) VALUES (?,?,?)",
                           (intent, question, answer))
        return cur.lastrowid


def kb_update(kb_id, intent, question, answer):
    with get_db() as conn:
        cur = conn.execute("UPDATE kb_entries SET intent=?,question=?,answer=? WHERE id=?",
                           (intent, question, answer, kb_id))
        return cur.rowcount > 0


def kb_delete(kb_id):
    with get_db() as conn:
        cur = conn.execute("DELETE FROM kb_entries WHERE id=?", (kb_id,))
        return cur.rowcount > 0


def stats():
    with get_db() as conn:
        total_sessions = conn.execute("SELECT COUNT(*) c FROM sessions").fetchone()["c"]
        total_msgs = conn.execute("SELECT COUNT(*) c FROM messages WHERE role='user'").fetchone()["c"]
        fallbacks = conn.execute("SELECT COUNT(*) c FROM unresolved").fetchone()["c"]
        top_intents = [dict(r) for r in conn.execute(
            "SELECT intent, COUNT(*) c FROM messages WHERE role='user' AND intent!='' "
            "GROUP BY intent ORDER BY c DESC LIMIT 8")]
        tickets = [dict(r) for r in conn.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 50")]
        unresolved = [dict(r) for r in conn.execute("SELECT * FROM unresolved ORDER BY id DESC LIMIT 50")]
        handoffs = conn.execute("SELECT COUNT(*) c FROM sessions WHERE handoff=1").fetchone()["c"]
        return {
            "total_sessions": total_sessions,
            "total_user_messages": total_msgs,
            "fallback_count": fallbacks,
            "fallback_rate": round(fallbacks / total_msgs, 4) if total_msgs else 0.0,
            "handoff_sessions": handoffs,
            "top_intents": top_intents,
            "tickets": tickets,
            "unresolved": unresolved,
        }


def conversations(limit=50):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT s.id, s.handoff, s.handoff_reason, s.created_at, COUNT(m.id) AS msg_count "
            "FROM sessions s LEFT JOIN messages m ON m.session_id=s.id "
            "GROUP BY s.id ORDER BY s.created_at DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]


def conversation_detail(session_id):
    with get_db() as conn:
        msgs = conn.execute("SELECT * FROM messages WHERE session_id=? ORDER BY id", (session_id,)).fetchall()
        return [dict(r) for r in msgs]
