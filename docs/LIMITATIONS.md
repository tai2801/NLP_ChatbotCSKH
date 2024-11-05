# Limitations

1. **Dữ liệu huấn luyện nhỏ** (152 câu tự viết): accuracy 88,9% trên tập kiểm tra 45 câu cùng miền; câu diễn đạt lạ, viết tắt nhiều hoặc không dấu có thể bị phân loại sai — đã có cơ chế fallback + handoff để giảm rủi ro trả lời sai.
2. **Tìm kiếm ngữ nghĩa bằng TF-IDF** là xấp xỉ theo từ vựng, không hiểu đồng nghĩa sâu như sentence embedding. Chưa dùng sentence-transformers vì nặng và cần tải model; đây là hướng nâng cấp đã ghi trong FUTURE_IMPROVEMENTS.
3. **Xác thực đơn bằng SĐT** là mức minh họa cho đồ án; triển khai thật nên dùng OTP.
4. **Admin token dạng tĩnh** (demo) — triển khai thật cần đăng nhập + phân quyền.
5. **SQLite + 1 tiến trình**: phù hợp demo/đồ án, chưa tối ưu cho tải lớn/đa tiến trình.
6. Chính sách trong KB và dữ liệu đơn hàng đều là **giả định/minh họa**, không dùng tư vấn cho khách hàng thật.
7. Bot chưa xử lý tốt câu hỏi chứa 2 intent cùng lúc (vd vừa hỏi phí ship vừa tra đơn) — hiện ưu tiên flow đang dở dang, sau đó mới tới intent mới.
