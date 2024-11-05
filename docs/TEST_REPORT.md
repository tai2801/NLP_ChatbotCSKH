# Test Report — HelpDesk NLP

Ngày chạy: 22/11/2024 · Môi trường: Windows 10, Python 3.11, FastAPI, scikit-learn, uvicorn, pytest, httpx.

## 1. Pytest — 27/27 PASS
Lệnh: `python -m pytest tests/ -q` → **27 passed**.
Bao phủ: trích xuất entity (mã đơn thường/hoa, SĐT, sản phẩm, chống bắt nhầm số tiền thành SĐT), 10 ca intent mẫu, flow tra đơn 3 lượt thành công, cung cấp đủ thông tin trong 1 câu, SĐT trước–mã đơn sau, **sai SĐT không lộ dữ liệu** (không có trạng thái/vận đơn/tên khách trong câu trả lời), đơn không tồn tại, khiếu nại tạo ticket + handoff (kiểm tra ticket trong DB), xin gặp nhân viên, fallback 2 lần → handoff + câu chưa giải quyết được ghi, trả lời KB phí ship, tin nhắn trống bị 422, health, admin thiếu/sai token bị 401, CRUD KB qua API rồi chat dùng ngay KB mới.

## 2. Đánh giá mô hình — `python scripts/evaluate.py`
- Intent accuracy trên 45 câu kiểm tra độc lập: **40/45 = 88,9%** (chi tiết trong `MODEL_EVALUATION.md`).
- 5/5 kịch bản nhiều lượt PASS: tra đơn đúng, sai SĐT, đơn không tồn tại, khiếu nại→ticket, fallback×2→handoff.

## 3. Kiểm thử tích hợp API (uvicorn + curl)
- `GET /health` → `{"status":"ok","kb_entries":17}`.
- Chat 1 lượt `"phí ship bao nhiêu"` → intent `van_chuyen`, confidence 0,6517, trả đúng chính sách phí ship từ KB.
- Tra đơn 2 lượt: lượt 1 gửi mã `TZ100001` → bot xin SĐT; lượt 2 gửi `0901234567` → trả `"Đang giao hàng"`, vận đơn `GHN88210001`, ETA `2024-11-22`.
- Sai SĐT (`0911111111`) → bị từ chối `"thông tin chưa khớp"`, không lộ trạng thái.
- Trang shop `/` HTTP 200, trang `/admin` HTTP 200, API admin stats với token demo trả số liệu đầy đủ.
