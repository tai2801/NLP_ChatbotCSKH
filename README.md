# HelpDesk NLP: Chatbot chăm sóc khách hàng bằng NLP

Chatbot CSKH cho cửa hàng điện tử giả định **TechZone (minh họa)** — môn *Xử lý ngôn ngữ tự nhiên*, HUIT.

> ⚠️ Toàn bộ dữ liệu (đơn hàng, khách hàng, chính sách) là **dữ liệu demo/minh họa phục vụ đồ án**.

## Tính năng chính
- **Intent classification tiếng Việt** bằng TF-IDF + Logistic Regression (14 intent), kèm confidence score; dưới ngưỡng 0,45 → fallback + gợi ý chủ đề.
- **Entity extraction**: mã đơn `TZxxxxxx`, số điện thoại, tên sản phẩm.
- **Hội thoại nhiều lượt có context**: flow tra đơn hàng theo máy trạng thái phiên — bot hỏi mã đơn, rồi xin SĐT xác thực ở lượt sau.
- **Tra cứu đơn an toàn**: chỉ trả trạng thái khi mã đơn + SĐT khớp DB; sai → từ chối chung chung, **không lộ dữ liệu**. Bot không bao giờ bịa trạng thái.
- **Khiếu nại → tạo ticket** (mã TCxxxxxx) và **chuyển nhân viên** khi khách yêu cầu, khiếu nại, hoặc bot fallback 2 lần liên tiếp.
- **Tìm câu trả lời theo ngữ nghĩa (TF-IDF cosine)** trên knowledge base do admin quản lý (CRUD qua API).
- **Dashboard admin**: KPI hội thoại, intent phổ biến, tỷ lệ fallback, câu hỏi chưa giải quyết, ticket, lịch sử hội thoại.

## Kết quả đánh giá
- Intent accuracy trên tập kiểm tra 45 câu độc lập: **88,9%** (40/45).
- Pytest: **27/27 PASS**. Kịch bản nhiều lượt (đúng/sai SĐT, khiếu nại, fallback): **5/5 PASS**.
- Chi tiết: `docs/MODEL_EVALUATION.md` và `docs/TEST_REPORT.md`.

## Cài đặt & chạy
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8300
```
Mở http://localhost:8300 (trang shop + widget chat góc phải) và http://localhost:8300/admin (dashboard).
Lưu ý: server mất khoảng 10 giây để huấn luyện classifier khi khởi động.

- Admin token demo: `admin-demo-token` (đổi bằng biến môi trường `ADMIN_TOKEN`). Đây là token minh họa cho đồ án, không dùng cho triển khai thật.
- DB SQLite tự tạo + seed tại `data/helpdesk.db` ở lần chạy đầu (đổi đường dẫn bằng `HELPDESK_DB`).

## Thử nhanh flow tra đơn
1. Chat: `kiểm tra đơn hàng TZ100001` → bot xin số điện thoại.
2. Chat tiếp: `0901234567` → bot trả trạng thái Đang giao hàng + mã vận đơn.
3. Thử SĐT sai (vd `0911111111`) với mã đơn trên → bot từ chối, không lộ dữ liệu.

## Kiểm thử & đánh giá
```bash
python -m pytest tests/ -q     # 27 test
python scripts/evaluate.py     # accuracy + kịch bản nhiều lượt
```

## Cấu trúc
```
app/        FastAPI + engine hội thoại + classifier + tầng SQLite
static/     Trang shop demo + widget chat, trang admin dashboard
tests/      Pytest (intent, entity, state machine, xác thực, handoff, admin)
scripts/    evaluate.py — đánh giá accuracy & kịch bản
docs/       Tài liệu: overview, use case, kiến trúc, ERD, model/evaluation, test report...
data/       SQLite DB (tự sinh khi chạy, không commit)
```

## Giấy phép
MIT License (xem `LICENSE`).
