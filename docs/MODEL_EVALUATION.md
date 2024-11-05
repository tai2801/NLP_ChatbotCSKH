# Model + Evaluation

## Mô hình đã dùng (ghi rõ)
- **Intent classification**: TF-IDF (word n-gram 1–2, trên văn bản tiếng Việt đã chuẩn hóa: thường hóa, bỏ dấu câu thừa) + **Logistic Regression** (scikit-learn). Confidence = `predict_proba` lớn nhất.
- **Tìm kiếm ngữ nghĩa (xấp xỉ)**: TF-IDF cosine similarity giữa câu hỏi và các câu hỏi trong knowledge base, lọc theo intent đã phân loại.
- **KHÔNG dùng sentence-transformers** trong bản này: thư viện nặng và cần tải model từ internet; TF-IDF cosine đáp ứng phạm vi đồ án và chạy offline. Xem LIMITATIONS.

## Ngưỡng tin cậy
- `CONFIDENCE_THRESHOLD = 0.45` (trong `app/classifier.py`): dưới ngưỡng → fallback + gợi ý chủ đề + ghi câu chưa giải quyết.
- Intent tra đơn được ưu tiên nhận diện từ 0.30 vì có entity mã đơn hỗ trợ và flow xác thực phía sau bảo vệ dữ liệu.

## Kết quả đánh giá (22/11/2024, chạy `python scripts/evaluate.py`)
- Tập kiểm tra: **45 câu** (diễn đạt khác tập huấn luyện).
- **Intent accuracy: 40/45 = 88,9%.**
- 5 câu sai — đáng chú ý là cả 5 đều có confidence thấp (0,197–0,498), tức phần lớn trường hợp bot sẽ fallback/hỏi lại thay vì trả lời sai tự tin:
  | Câu | Đúng | Dự đoán | Confidence |
  |---|---|---|---|
  | mua rồi không ưng có trả lại được không shop | doi_tra | thanh_toan | 0,293 |
  | có đồng hồ thông minh nào pin trâu không | tu_van_san_pham | khuyen_mai | 0,197 |
  | giao nhầm hàng cho tôi rồi đấy | khieu_nai | tra_don_hang | 0,271 |
  | tết shop có nghỉ không | gio_lam_viec | chao_hoi | 0,268 |
  | sản phẩm lỗi trong 30 ngày đầu có đổi mới không | bao_hanh | doi_tra | 0,498 |

## Kịch bản hội thoại nhiều lượt (đo trong cùng script)
| Kịch bản | Kết quả |
|---|---|
| Tra đơn đúng SĐT (3 lượt) | PASS |
| Sai SĐT — không lộ dữ liệu | PASS |
| Đơn không tồn tại | PASS |
| Khiếu nại tạo ticket + handoff | PASS |
| Fallback 2 lần → handoff | PASS |
