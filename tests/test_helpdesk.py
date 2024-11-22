# -*- coding: utf-8 -*-
"""Test cho HelpDesk NLP: intent, entity, state machine, xác thực đơn, handoff, admin API."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["HELPDESK_DB"] = _tmp.name

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import db  # noqa: E402
from app.classifier import extract_entities  # noqa: E402
from app.main import app  # noqa: E402

db.init_db()
client = TestClient(app)


def chat(session, msg):
    r = client.post("/api/chat", json={"session_id": session, "message": msg})
    assert r.status_code == 200, r.text
    return r.json()


# ---------------- Entity extraction ----------------
def test_entity_order_code_and_phone():
    e = extract_entities("tra đơn TZ100001 giúp tôi, sđt 0901234567")
    assert e["order_code"] == "TZ100001"
    assert e["phone"] == "0901234567"


def test_entity_order_code_lowercase_and_space():
    e = extract_entities("đơn tz 100007 sao rồi")
    assert e["order_code"] == "TZ100007"


def test_entity_no_false_phone():
    e = extract_entities("đơn này giá 14990000 đồng")
    assert "phone" not in e


def test_entity_product():
    e = extract_entities("sonicbuds pro còn hàng không shop")
    assert e.get("product") == "Tai Nghe Không Dây SonicBuds Pro"


# ---------------- Intent classification ----------------
@pytest.mark.parametrize("text,intent", [
    ("phí ship bao nhiêu vậy shop", "van_chuyen"),
    ("chính sách đổi trả thế nào", "doi_tra"),
    ("laptop bảo hành mấy năm", "bao_hanh"),
    ("shop có trả góp không", "thanh_toan"),
    ("có mã giảm giá nào không", "khuyen_mai"),
    ("shop mở cửa mấy giờ", "gio_lam_viec"),
    ("cho tôi gặp nhân viên", "lien_he_nhan_vien"),
    ("quên mật khẩu thì làm sao", "tai_khoan"),
    ("cảm ơn shop nhiều nhé", "cam_on"),
    ("kiểm tra đơn hàng của tôi", "tra_don_hang"),
])
def test_intent_samples(text, intent):
    out = chat(f"intent-{intent}-{abs(hash(text)) % 9999}", text)
    assert out["intent"] == intent, out


# ---------------- Flow tra đơn nhiều lượt + xác thực ----------------
def test_order_flow_three_turns_success():
    s = "flow-ok"
    r1 = chat(s, "kiểm tra đơn hàng của tôi")
    assert "mã đơn" in r1["reply"].lower()
    r2 = chat(s, "TZ100001")
    assert "số điện thoại" in r2["reply"].lower()
    assert "GHN88210001" not in r2["reply"]  # chưa xác thực -> chưa lộ vận đơn
    r3 = chat(s, "0901234567")
    assert "Đang giao hàng" in r3["reply"]
    assert "GHN88210001" in r3["reply"]
    assert "Laptop Học Tập Pro 14" in r3["reply"]


def test_order_flow_all_in_one_message():
    out = chat("flow-one", "tra cứu đơn TZ100002 số điện thoại 0912345678")
    assert "Đã giao thành công" in out["reply"]


def test_order_wrong_phone_no_data_leak():
    s = "flow-wrong"
    chat(s, "kiểm tra đơn hàng TZ100001")
    out = chat(s, "0999999999")
    assert "chưa khớp" in out["reply"]
    assert "Đang giao hàng" not in out["reply"]
    assert "GHN88210001" not in out["reply"]
    assert "Nguyễn Văn An" not in out["reply"]


def test_order_nonexistent_code_no_leak():
    out = chat("flow-404", "tra đơn TZ999999 sđt 0901234567")
    assert "chưa khớp" in out["reply"]
    assert "trạng thái" not in out["reply"].lower() or "chưa thể" in out["reply"]


def test_order_phone_first_then_code():
    s = "flow-phone-first"
    r1 = chat(s, "tra đơn hàng giúp tôi, sđt của tôi là 0933456789")
    assert "mã đơn" in r1["reply"].lower()
    r2 = chat(s, "TZ100004")
    assert "Đang đóng gói" in r2["reply"]


# ---------------- Khiếu nại / handoff / fallback ----------------
def test_complaint_creates_ticket_and_handoff():
    out = chat("complaint-1", "tôi muốn khiếu nại, giao hàng quá chậm tôi rất bực")
    assert out["handoff"] is True
    assert out.get("ticket_code", "").startswith("TC")
    t = db.stats()["tickets"]
    assert any(x["code"] == out["ticket_code"] for x in t)


def test_ask_human_handoff():
    out = chat("human-1", "cho tôi gặp nhân viên hỗ trợ trực tiếp")
    assert out["handoff"] is True


def test_fallback_twice_triggers_handoff():
    s = "fallback-1"
    r1 = chat(s, "asdf qwer zxcv 12345")
    assert r1["fallback"] is True and r1["handoff"] is False
    r2 = chat(s, "blabla không liên quan gì hết luôn á")
    assert r2["handoff"] is True
    unres = db.stats()["unresolved"]
    assert any("asdf" in u["question"] for u in unres)


def test_kb_answer_shipping_fee():
    out = chat("kb-1", "phí vận chuyển tính thế nào vậy")
    assert "25.000đ" in out["reply"] or "miễn phí" in out["reply"].lower()


# ---------------- API / Admin ----------------
def test_empty_message_rejected():
    r = client.post("/api/chat", json={"message": "   "})
    assert r.status_code == 422


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_admin_requires_token():
    assert client.get("/api/admin/stats").status_code == 401
    assert client.get("/api/admin/stats", headers={"X-Admin-Token": "sai-token"}).status_code == 401


def test_admin_stats_and_kb_crud():
    h = {"X-Admin-Token": "admin-demo-token"}
    s = client.get("/api/admin/stats", headers=h).json()
    assert s["total_sessions"] >= 1
    r = client.post("/api/admin/kb", headers=h,
                    json={"intent": "van_chuyen", "question": "Shop có giao ra đảo không?",
                          "answer": "TechZone có giao ra đảo qua Viettel Post, thời gian 5-7 ngày (minh họa)."})
    assert r.status_code == 200
    kb_id = r.json()["id"]
    out = chat("kb-new", "shop có giao hàng ra đảo không")
    assert "đảo" in out["reply"]
    assert client.delete(f"/api/admin/kb/{kb_id}", headers=h).status_code == 200
