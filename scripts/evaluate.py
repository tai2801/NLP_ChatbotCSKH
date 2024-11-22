# -*- coding: utf-8 -*-
"""
Đánh giá HelpDesk NLP:
1) Intent accuracy trên tập kiểm tra độc lập (>=40 câu, cách diễn đạt khác câu huấn luyện).
2) Kịch bản hội thoại nhiều lượt: tra đơn đúng / sai SĐT / đơn không tồn tại / khiếu nại / fallback x2.
Chạy: python scripts/evaluate.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ["HELPDESK_DB"] = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name

from app import db  # noqa: E402
from app.classifier import IntentClassifier  # noqa: E402
from app.engine import HelpDeskEngine  # noqa: E402

EVAL_SET = [
    ("ship về đà nẵng bao nhiêu tiền", "van_chuyen"),
    ("giao hàng tới cần thơ mấy ngày", "van_chuyen"),
    ("đơn vị nào vận chuyển cho shop vậy", "van_chuyen"),
    ("hàng bị móp hộp có được đổi không", "doi_tra"),
    ("mua rồi không ưng có trả lại được không shop", "doi_tra"),
    ("đổi hàng thì mang ra cửa hàng hay gửi ship", "doi_tra"),
    ("điện thoại mua ở shop bảo hành bao lâu", "bao_hanh"),
    ("máy hư mang đi sửa ở đâu", "bao_hanh"),
    ("hết hạn bảo hành shop có nhận sửa không", "bao_hanh"),
    ("trả góp qua thẻ tín dụng được không", "thanh_toan"),
    ("mình chuyển khoản trước có được không", "thanh_toan"),
    ("có thanh toán lúc nhận hàng không shop", "thanh_toan"),
    ("dạo này có chương trình sale nào hot không", "khuyen_mai"),
    ("khách hàng mới có ưu đãi gì", "khuyen_mai"),
    ("điểm thành viên đổi được gì", "khuyen_mai"),
    ("đơn của tôi bao giờ mới giao tới", "tra_don_hang"),
    ("check giúp mình đơn hàng với", "tra_don_hang"),
    ("hàng tôi đặt từ thứ hai sao chưa thấy", "tra_don_hang"),
    ("tư vấn mình tai nghe nào nghe nhạc hay", "tu_van_san_pham"),
    ("ngân sách 15 triệu nên mua laptop gì", "tu_van_san_pham"),
    ("có đồng hồ thông minh nào pin trâu không", "tu_van_san_pham"),
    ("tôi rất không hài lòng với cách phục vụ", "khieu_nai"),
    ("giao nhầm hàng cho tôi rồi đấy", "khieu_nai"),
    ("tôi muốn phản ánh thái độ nhân viên giao hàng", "khieu_nai"),
    ("không đăng nhập vào tài khoản được", "tai_khoan"),
    ("mình muốn đổi email cho tài khoản", "tai_khoan"),
    ("xem điểm thưởng của tôi ở chỗ nào", "tai_khoan"),
    ("thứ bảy shop có mở cửa không", "gio_lam_viec"),
    ("mấy giờ shop đóng cửa vậy", "gio_lam_viec"),
    ("tết shop có nghỉ không", "gio_lam_viec"),
    ("kết nối giúp tôi với tư vấn viên", "lien_he_nhan_vien"),
    ("bot không giúp được tôi cần người thật", "lien_he_nhan_vien"),
    ("cho mình xin gặp bộ phận hỗ trợ", "lien_he_nhan_vien"),
    ("chào shop mình có việc muốn hỏi", "chao_hoi"),
    ("alo có ai ở đó không", "chao_hoi"),
    ("cám ơn bạn đã tư vấn", "cam_on"),
    ("ok mình cảm ơn nhé", "cam_on"),
    ("thôi chào shop mình đi đây", "tam_biet"),
    ("hẹn lần sau gặp lại nhé", "tam_biet"),
    ("mình muốn xem đơn hàng đã giao chưa", "tra_don_hang"),
    ("phí giao hàng hỏa tốc là bao nhiêu", "van_chuyen"),
    ("sản phẩm lỗi trong 30 ngày đầu có đổi mới không", "bao_hanh"),
    ("voucher sinh nhật dùng thế nào", "khuyen_mai"),
    ("đổi mật khẩu tài khoản ở đâu", "tai_khoan"),
    ("giờ hỗ trợ trực tuyến đến mấy giờ", "gio_lam_viec"),
]


def main():
    db.init_db()
    clf = IntentClassifier()
    correct, wrong = 0, []
    for text, expected in EVAL_SET:
        pred, conf = clf.predict(text)
        if pred == expected:
            correct += 1
        else:
            wrong.append((text, expected, pred, round(conf, 3)))
    acc = correct / len(EVAL_SET)
    print(f"Tap kiem tra: {len(EVAL_SET)} cau")
    print(f"Intent accuracy: {correct}/{len(EVAL_SET)} = {acc:.1%}")
    if wrong:
        print("Cau sai:")
        for w in wrong:
            print("  -", w)

    eng = HelpDeskEngine()
    print("\nKich ban nhieu luot:")
    s = "eval-flow"
    eng.chat(s, "kiểm tra đơn hàng của tôi")
    eng.chat(s, "TZ100001")
    r = eng.chat(s, "0901234567")
    print("  Tra don dung SDT:", "PASS" if "Đang giao hàng" in r["reply"] and "GHN88210001" in r["reply"] else "FAIL")

    s2 = "eval-wrong"
    eng.chat(s2, "tra đơn TZ100001")
    r = eng.chat(s2, "0900000000")
    ok = "chưa khớp" in r["reply"] and "GHN88210001" not in r["reply"]
    print("  Sai SDT khong lo du lieu:", "PASS" if ok else "FAIL")

    r = eng.chat("eval-404", "tra đơn TZ999999 sđt 0901234567")
    print("  Don khong ton tai:", "PASS" if "chưa khớp" in r["reply"] else "FAIL")

    r = eng.chat("eval-complaint", "tôi muốn khiếu nại dịch vụ quá tệ")
    print("  Khieu nai tao ticket:", "PASS" if r.get("ticket_code") and r["handoff"] else "FAIL")

    s3 = "eval-fb"
    eng.chat(s3, "xyz abc 987 vô nghĩa")
    r = eng.chat(s3, "lại một câu vô nghĩa nữa nè")
    print("  Fallback 2 lan -> handoff:", "PASS" if r["handoff"] else "FAIL")


if __name__ == "__main__":
    main()
