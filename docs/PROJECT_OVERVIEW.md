# Project Overview — HelpDesk NLP

Chatbot chăm sóc khách hàng cho cửa hàng thương mại điện tử giả định **TechZone (minh họa)** — môn Xử lý ngôn ngữ tự nhiên (HUIT).

Điểm nổi bật so với các chatbot FAQ đơn giản:
1. **Hội thoại nhiều lượt có context** — máy trạng thái theo phiên (session) ghi nhớ flow tra cứu đơn hàng qua nhiều lượt chat.
2. **Tra cứu đơn hàng từ DB sau khi xác thực** — mã đơn + số điện thoại phải khớp dữ liệu; bot không tự bịa trạng thái.
3. **Chuyển nhân viên (handoff) có quy tắc** — khách yêu cầu, khiếu nại, hoặc bot fallback 2 lần liên tiếp.
4. **Quản trị & đo chất lượng** — dashboard thống kê intent, tỷ lệ fallback, danh sách câu chưa giải quyết, quản lý knowledge base.

Công nghệ: Python, FastAPI, scikit-learn (TF-IDF + Logistic Regression), SQLite, frontend HTML/CSS/JS thuần.
