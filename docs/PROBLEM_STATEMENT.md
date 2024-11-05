# Problem Statement + Requirements

## Bài toán
Shop thương mại điện tử nhận nhiều câu hỏi lặp lại (vận chuyển, đổi trả, bảo hành...) và yêu cầu tra cứu đơn hàng. Nhân viên không thể trực tuyến 24/7. Cần chatbot tiếng Việt: hiểu ý định, trả lời chính sách từ knowledge base, tra cứu đơn hàng an toàn và biết chuyển nhân viên khi vượt khả năng.

## Functional Requirements
- FR1: Phân loại intent cho câu hỏi tiếng Việt, kèm confidence score.
- FR2: Trích xuất entity: mã đơn (TZxxxxxx), số điện thoại, tên sản phẩm.
- FR3: Tra cứu đơn nhiều lượt: bot chủ động hỏi thông tin còn thiếu (mã đơn → SĐT).
- FR4: Xác thực mã đơn + SĐT khớp DB trước khi trả trạng thái; sai thì từ chối, không lộ dữ liệu.
- FR5: Trả lời chính sách bằng tìm kiếm TF-IDF cosine trên knowledge base.
- FR6: Fallback khi confidence < 0.45, kèm gợi ý chủ đề; ghi lại câu chưa giải quyết.
- FR7: Khiếu nại → tạo ticket có mã; handoff khi khách yêu cầu hoặc fallback 2 lần liên tiếp.
- FR8: Lưu toàn bộ lịch sử hội thoại theo phiên.
- FR9: Admin xem thống kê (hội thoại, intent phổ biến, tỷ lệ fallback), quản lý KB (CRUD), xem câu chưa giải quyết và ticket.
- FR10: Widget chat nhúng trong trang shop demo; trang admin dashboard riêng.

## Non-functional Requirements
- NFR1: Trả lời 1 lượt < 1 giây trên máy thường (sau khi nạp model).
- NFR2: Không lộ dữ liệu đơn hàng khi chưa xác thực (yêu cầu bảo mật cốt lõi).
- NFR3: Không phụ thuộc API/LLM bên ngoài; chạy offline hoàn toàn.
- NFR4: Dữ liệu đơn hàng mẫu phải ghi rõ là demo/minh họa.
- NFR5: API admin được bảo vệ bằng token (demo), ghi rõ cần thay bằng xác thực thật khi triển khai.
