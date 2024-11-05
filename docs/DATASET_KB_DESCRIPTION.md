# Dataset / Knowledge Base Description

## Dữ liệu huấn luyện intent
- 14 intent: chao_hoi, tra_don_hang, van_chuyen, doi_tra, bao_hanh, thanh_toan, tu_van_san_pham, khieu_nai, khuyen_mai, tai_khoan, gio_lam_viec, lien_he_nhan_vien, cam_on, tam_biet.
- Mỗi intent 8–12 câu mẫu tiếng Việt trong `app/data.py` (tổng 152 câu).

## Knowledge base
- 17 mục FAQ/chính sách của shop giả định "TechZone (minh họa)": vận chuyển, đổi trả, bảo hành, thanh toán/trả góp, khuyến mãi/tích điểm, tài khoản, giờ làm việc, tư vấn sản phẩm.
- Đây là chính sách **giả định phục vụ đồ án**, không phải chính sách của doanh nghiệp thật.
- Admin thêm/sửa/xóa KB qua API; bot nạp lại ngay khi có thay đổi.

## Đơn hàng mẫu (DEMO)
- 14 đơn `TZ100001`–`TZ100014` với khách hàng, SĐT, sản phẩm, trạng thái, vận đơn, ETA giả định — toàn bộ là dữ liệu minh họa trong `app/data.py`, ghi rõ ở README và giao diện shop.

## Tập kiểm tra đánh giá
- 45 câu trong `scripts/evaluate.py`, diễn đạt khác câu huấn luyện, dùng đo intent accuracy.
- 5 kịch bản hội thoại nhiều lượt kiểm tra context/xác thực/handoff.
