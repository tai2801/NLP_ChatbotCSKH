# -*- coding: utf-8 -*-
"""
Dialogue engine: máy trạng thái hội thoại nhiều lượt + xác thực tra cứu đơn hàng.

Nguyên tắc an toàn (BR cốt lõi của dự án):
- Trạng thái đơn CHỈ lấy từ DB, bot không tự bịa.
- Muốn xem trạng thái đơn phải có ĐỦ mã đơn + SĐT và SĐT phải khớp SĐT đặt hàng.
  Sai bất kỳ thông tin nào -> từ chối chung chung, KHÔNG lộ trạng thái/tên khách.
- Fallback 2 lần liên tiếp hoặc khách yêu cầu/khiếu nại -> chuyển nhân viên (handoff).
"""
from . import db
from .classifier import CONFIDENCE_THRESHOLD, IntentClassifier, KBSearch, extract_entities
from .data import INTENT_LABELS, ORDER_STATUS_VI

SUGGESTIONS = {
    "default": ["Tra cứu đơn hàng", "Phí vận chuyển bao nhiêu?", "Chính sách đổi trả", "Gặp nhân viên"],
    "tra_don_hang": ["Xem chính sách đổi trả", "Phí vận chuyển bao nhiêu?", "Gặp nhân viên"],
    "doi_tra": ["Tra cứu đơn hàng", "Hoàn tiền mất bao lâu?", "Gặp nhân viên"],
    "van_chuyen": ["Tra cứu đơn hàng", "Shop đang có khuyến mãi gì?", "Gặp nhân viên"],
}

KB_INTENTS = {"van_chuyen", "doi_tra", "bao_hanh", "thanh_toan", "khuyen_mai",
              "tai_khoan", "gio_lam_viec", "tu_van_san_pham"}

CANNED = {
    "chao_hoi": "Xin chào! Mình là trợ lý ảo của TechZone. Mình có thể tra cứu đơn hàng, tư vấn vận chuyển, đổi trả, bảo hành và khuyến mãi. Bạn cần hỗ trợ gì ạ?",
    "cam_on": "Rất vui vì được hỗ trợ bạn! Nếu cần gì thêm cứ nhắn cho TechZone nhé.",
    "tam_biet": "Tạm biệt bạn, cảm ơn bạn đã mua sắm tại TechZone. Hẹn gặp lại!",
}


class HelpDeskEngine:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.kb = KBSearch(db.kb_all())

    def reload_kb(self):
        self.kb = KBSearch(db.kb_all())

    # ---------- tra cứu đơn hàng có xác thực ----------
    def _verify_and_answer(self, session_id, sess):
        code, phone = sess["pending_order"], sess["pending_phone"]
        order = db.find_order(code)
        if order and order["phone"] == phone:
            db.update_session(session_id, state="IDLE", pending_order="", pending_phone="", fallback_count=0)
            status_vi = ORDER_STATUS_VI.get(order["status"], order["status"])
            lines = [
                f"Đơn hàng {order['code']} — {status_vi}.",
                f"Sản phẩm: {order['product']} × {order['qty']}, tổng {order['total']:,}đ.".replace(",", "."),
                f"Ngày đặt: {order['created']}.",
            ]
            if order["tracking"]:
                lines.append(f"Mã vận đơn: {order['tracking']}.")
            if order["eta"]:
                lines.append(f"Dự kiến giao: {order['eta']}.")
            if order["status"] == "DELIVERED":
                lines.append("Đơn đã giao thành công. Bạn cần hỗ trợ thêm về bảo hành/đổi trả không?")
            return "\n".join(lines), True
        # Sai mã đơn hoặc sai SĐT: từ chối chung, không lộ dữ liệu nào của đơn.
        db.update_session(session_id, state="AWAIT_PHONE", pending_phone="")
        return ("Thông tin bạn cung cấp chưa khớp với dữ liệu đơn hàng, nên mình chưa thể tra cứu. "
                "Bạn kiểm tra lại số điện thoại đã dùng khi đặt hàng rồi gửi lại giúp mình nhé "
                "(hoặc gõ mã đơn khác)."), False

    def _order_flow(self, session_id, sess, entities):
        """Cập nhật entity đã có, quyết định hỏi tiếp hay xác thực."""
        code = entities.get("order_code") or sess["pending_order"]
        phone = entities.get("phone") or sess["pending_phone"]
        db.update_session(session_id, pending_order=code or "", pending_phone=phone or "")
        sess = dict(sess, pending_order=code or "", pending_phone=phone or "")
        if code and phone:
            reply, _ok = self._verify_and_answer(session_id, sess)
            return reply
        if code:
            db.update_session(session_id, state="AWAIT_PHONE")
            return (f"Mình đã ghi nhận mã đơn {code}. Để bảo mật, bạn cho mình xin thêm "
                    "số điện thoại đã dùng khi đặt hàng để xác thực nhé.")
        if phone:
            db.update_session(session_id, state="AWAIT_ORDER")
            return "Mình đã ghi nhận số điện thoại. Bạn cho mình xin mã đơn hàng (dạng TZxxxxxx) nữa nhé."
        db.update_session(session_id, state="AWAIT_ORDER")
        return ("Để tra cứu đơn hàng, bạn cho mình xin mã đơn hàng (dạng TZxxxxxx, có trong SMS/email xác nhận) nhé. "
                "Sau đó mình sẽ xin thêm số điện thoại để xác thực.")

    # ---------- xử lý 1 lượt chat ----------
    def chat(self, session_id, message):
        message = (message or "").strip()
        sess = db.get_session(session_id)
        entities = extract_entities(message)
        intent, confidence = self.classifier.predict(message) if message else ("", 0.0)

        # Đang giữa flow tra đơn: ưu tiên entity của lượt này hơn intent mới.
        if sess["state"] in ("AWAIT_ORDER", "AWAIT_PHONE") and (entities.get("order_code") or entities.get("phone")):
            reply = self._order_flow(session_id, sess, entities)
            return self._finish(session_id, message, reply, "tra_don_hang", max(confidence, 0.99))

        # Intent tra đơn (kể cả khi khách đã kèm mã đơn/SĐT ngay trong câu hỏi).
        if intent == "tra_don_hang" and confidence >= 0.30:
            reply = self._order_flow(session_id, sess, entities)
            return self._finish(session_id, message, reply, intent, confidence)

        # Khiếu nại -> tạo ticket + chuyển nhân viên.
        if intent == "khieu_nai" and confidence >= CONFIDENCE_THRESHOLD:
            code = db.create_ticket(session_id, message)
            db.update_session(session_id, handoff=1, handoff_reason="Khiếu nại của khách hàng",
                              state="IDLE", fallback_count=0)
            reply = (f"TechZone rất xin lỗi vì trải nghiệm chưa tốt của bạn. Mình đã ghi nhận khiếu nại "
                     f"và tạo phiếu hỗ trợ {code}. Nhân viên CSKH sẽ liên hệ lại với bạn trong thời gian sớm nhất.")
            return self._finish(session_id, message, reply, intent, confidence, ticket=code, handoff=True)

        # Khách xin gặp nhân viên.
        if intent == "lien_he_nhan_vien" and confidence >= CONFIDENCE_THRESHOLD:
            db.update_session(session_id, handoff=1, handoff_reason="Khách yêu cầu gặp nhân viên", fallback_count=0)
            reply = ("Mình đã chuyển cuộc trò chuyện của bạn cho nhân viên CSKH. "
                     "Nhân viên sẽ tiếp nhận ngay trong giờ hỗ trợ 8h-22h. Bạn mô tả thêm vấn đề cần hỗ trợ trong lúc chờ nhé.")
            return self._finish(session_id, message, reply, intent, confidence, handoff=True)

        # Câu trả lời từ KB cho các intent chính sách/tư vấn.
        if intent in KB_INTENTS and confidence >= CONFIDENCE_THRESHOLD:
            hits = self.kb.search(message, intent=intent, top_k=1)
            if hits and hits[0][1] > 0.03:
                db.update_session(session_id, fallback_count=0)
                return self._finish(session_id, message, hits[0][0]["answer"], intent, confidence)
            db.update_session(session_id, fallback_count=0)
            return self._finish(session_id, message,
                                f"Về chủ đề {INTENT_LABELS.get(intent, intent)}, bạn mô tả cụ thể hơn giúp mình nhé, "
                                "mình sẽ tra trong kho tri thức của shop.", intent, confidence)

        # Intent đơn giản có câu trả lời mẫu.
        if intent in CANNED and confidence >= CONFIDENCE_THRESHOLD:
            db.update_session(session_id, fallback_count=0)
            return self._finish(session_id, message, CANNED[intent], intent, confidence)

        # Fallback: confidence thấp hoặc intent không xử lý được.
        return self._fallback(session_id, sess, message, intent, confidence)

    def _fallback(self, session_id, sess, message, intent, confidence):
        count = (sess["fallback_count"] or 0) + 1
        db.log_unresolved(session_id, message)
        if count >= 2:
            db.update_session(session_id, fallback_count=0, handoff=1,
                              handoff_reason="Bot không hiểu 2 lần liên tiếp")
            reply = ("Mình chưa hiểu rõ ý bạn sau vài lần thử, nên mình chuyển cuộc trò chuyện cho nhân viên CSKH "
                     "để hỗ trợ chính xác hơn. Bạn cứ để lại nội dung cần hỗ trợ tại đây nhé.")
            return self._finish(session_id, message, reply, intent, confidence, handoff=True)
        db.update_session(session_id, fallback_count=count)
        reply = ("Xin lỗi, mình chưa hiểu rõ câu hỏi của bạn. Bạn có thể hỏi về: tra cứu đơn hàng, "
                 "vận chuyển, đổi trả, bảo hành, thanh toán, khuyến mãi — hoặc gõ 'gặp nhân viên' để được hỗ trợ trực tiếp.")
        return self._finish(session_id, message, reply, intent, confidence, fallback=True)

    def _finish(self, session_id, user_msg, reply, intent, confidence, ticket=None, handoff=False, fallback=False):
        db.log_message(session_id, "user", user_msg, intent, confidence)
        db.log_message(session_id, "bot", reply, intent, confidence)
        sess = db.get_session(session_id)
        out = {
            "session_id": session_id,
            "reply": reply,
            "intent": intent,
            "intent_label": INTENT_LABELS.get(intent, intent),
            "confidence": round(float(confidence), 4),
            "suggestions": SUGGESTIONS.get(intent, SUGGESTIONS["default"]),
            "handoff": bool(sess["handoff"]) or handoff,
            "fallback": fallback,
        }
        if ticket:
            out["ticket_code"] = ticket
        return out
