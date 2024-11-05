# Future Improvements

- Thay TF-IDF cosine bằng sentence-transformers (mô hình embedding tiếng Việt) cho tìm kiếm ngữ nghĩa thật, có cache vector KB.
- Mở rộng dữ liệu huấn luyện từ chính các câu fallback đã ghi (vòng lặp cải tiến dữ liệu có kiểm duyệt của admin).
- Xác thực tra đơn bằng OTP gửi SMS thay cho đối chiếu SĐT.
- Đăng nhập admin + phân quyền thay cho token tĩnh; nhân viên trả lời trực tiếp trong phiên handoff (live chat 2 chiều qua WebSocket).
- Hỗ trợ câu hỏi đa intent và sửa lỗi chính tả/viết tắt tiếng Việt (teencode) tốt hơn.
- Đóng gói Docker, chuyển SQLite → PostgreSQL khi triển khai thật.
