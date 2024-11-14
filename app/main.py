# -*- coding: utf-8 -*-
"""FastAPI app: API chat + API admin (token demo) + phục vụ frontend tĩnh."""
import os
import uuid

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import db
from .engine import HelpDeskEngine

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "admin-demo-token")
BASE = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE, "..", "static")

db.init_db()
engine = HelpDeskEngine()

app = FastAPI(title="HelpDesk NLP - TechZone (minh họa)", version="1.0.0")


class ChatIn(BaseModel):
    message: str
    session_id: str | None = None


class KBIn(BaseModel):
    intent: str
    question: str
    answer: str


def require_admin(x_admin_token: str = Header(default="")):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Admin token không hợp lệ (demo token xem trong README).")
    return True


@app.get("/health")
def health():
    return {"status": "ok", "kb_entries": len(db.kb_all())}


@app.post("/api/chat")
def chat(payload: ChatIn):
    if not payload.message.strip():
        raise HTTPException(status_code=422, detail="Tin nhắn không được để trống.")
    session_id = payload.session_id or uuid.uuid4().hex[:16]
    return engine.chat(session_id, payload.message)


@app.get("/api/suggestions")
def suggestions():
    return {"suggestions": ["Tra cứu đơn hàng", "Phí vận chuyển bao nhiêu?",
                            "Chính sách đổi trả thế nào?", "Shop đang có khuyến mãi gì?",
                            "Tôi muốn khiếu nại", "Gặp nhân viên"]}


# ---------------- Admin API ----------------
@app.get("/api/admin/stats", dependencies=[Depends(require_admin)])
def admin_stats():
    return db.stats()


@app.get("/api/admin/conversations", dependencies=[Depends(require_admin)])
def admin_conversations():
    return db.conversations()


@app.get("/api/admin/conversations/{session_id}", dependencies=[Depends(require_admin)])
def admin_conversation_detail(session_id: str):
    return db.conversation_detail(session_id)


@app.get("/api/admin/kb", dependencies=[Depends(require_admin)])
def admin_kb_list():
    return db.kb_all()


@app.post("/api/admin/kb", dependencies=[Depends(require_admin)])
def admin_kb_add(payload: KBIn):
    kb_id = db.kb_add(payload.intent, payload.question, payload.answer)
    engine.reload_kb()
    return {"id": kb_id}


@app.put("/api/admin/kb/{kb_id}", dependencies=[Depends(require_admin)])
def admin_kb_update(kb_id: int, payload: KBIn):
    if not db.kb_update(kb_id, payload.intent, payload.question, payload.answer):
        raise HTTPException(status_code=404, detail="Không tìm thấy mục KB.")
    engine.reload_kb()
    return {"ok": True}


@app.delete("/api/admin/kb/{kb_id}", dependencies=[Depends(require_admin)])
def admin_kb_delete(kb_id: int):
    if not db.kb_delete(kb_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy mục KB.")
    engine.reload_kb()
    return {"ok": True}


# ---------------- Frontend tĩnh ----------------
@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/admin")
def admin_page():
    return FileResponse(os.path.join(STATIC_DIR, "admin.html"))


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
