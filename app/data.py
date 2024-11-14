# -*- coding: utf-8 -*-
"""
Dữ liệu huấn luyện và kịch bản mẫu cho HelpDesk NLP.

- INTENTS: câu mẫu huấn luyện intent classification (tiếng Việt).
- KB_SEED: knowledge base FAQ/chính sách của shop giả định "TechZone (minh họa)".
- ORDERS_SEED: đơn hàng mẫu DEMO (dữ liệu minh họa phục vụ đồ án).
- PRODUCTS: danh mục sản phẩm demo dùng cho entity extraction + tư vấn.
"""

INTENTS = {
    "chao_hoi": [
        "xin chào", "chào shop", "hello shop", "chào bạn", "hi shop ơi",
        "alo shop có đó không", "chào buổi sáng", "shop ơi cho mình hỏi",
        "bạn có online không", "chào ad", "hey shop", "có ai hỗ trợ không",
    ],
    "tra_don_hang": [
        "kiểm tra đơn hàng của tôi", "đơn hàng của tôi đến đâu rồi",
        "tra cứu đơn hàng", "xem tình trạng đơn hàng", "đơn của tôi giao chưa",
        "tôi muốn kiểm tra đơn", "đơn hàng mã TZ100001 đang ở đâu",
        "theo dõi đơn hàng giúp tôi", "đơn tôi đặt hôm qua sao rồi",
        "check đơn hàng cho mình", "đơn của mình khi nào tới",
        "tình trạng đơn hàng thế nào rồi shop",
    ],
    "van_chuyen": [
        "phí ship bao nhiêu", "giao hàng mất bao lâu", "shop có giao nhanh không",
        "thời gian vận chuyển bao lâu", "phí vận chuyển tính thế nào",
        "có giao hàng trong ngày không", "ship về tỉnh mất mấy ngày",
        "đơn vị vận chuyển nào giao hàng", "giao hàng toàn quốc không shop",
        "miễn phí vận chuyển khi nào", "ship nội thành bao nhiêu tiền",
        "có hỗ trợ giao hàng hỏa tốc không",
    ],
    "doi_tra": [
        "chính sách đổi trả thế nào", "tôi muốn đổi sản phẩm", "hàng lỗi có được trả không",
        "đổi trả trong bao nhiêu ngày", "sản phẩm không đúng mô tả có trả được không",
        "thủ tục đổi trả ra sao", "tôi muốn trả hàng hoàn tiền", "đổi size khác được không",
        "hàng bị vỡ khi giao có đổi không", "quy định trả hàng của shop",
        "đổi hàng cần mang theo gì", "phí đổi trả ai chịu",
    ],
    "bao_hanh": [
        "chính sách bảo hành thế nào", "sản phẩm bảo hành bao lâu", "bảo hành ở đâu",
        "laptop này bảo hành mấy năm", "hàng lỗi bảo hành như thế nào",
        "trung tâm bảo hành ở đâu vậy shop", "bảo hành có mất phí không",
        "điều kiện bảo hành là gì", "sản phẩm hết bảo hành có sửa được không",
        "thời gian bảo hành của tai nghe", "bảo hành chính hãng không shop",
        "mang máy đi bảo hành cần giấy tờ gì",
    ],
    "thanh_toan": [
        "shop hỗ trợ thanh toán thế nào", "có trả góp không", "thanh toán bằng thẻ được không",
        "có cod không shop", "trả góp 0% lãi suất không", "chuyển khoản ngân hàng nào",
        "thanh toán khi nhận hàng được không", "có ví điện tử không",
        "các hình thức thanh toán gồm những gì", "đặt cọc trước bao nhiêu", "trả góp cần thủ tục gì",
        "thanh toán online có an toàn không",
    ],
    "tu_van_san_pham": [
        "tư vấn cho tôi một chiếc laptop", "nên mua điện thoại nào tầm 10 triệu",
        "shop có tai nghe chống ồn không", "gợi ý sản phẩm bán chạy",
        "laptop nào phù hợp sinh viên", "có máy tính bảng cho trẻ em không",
        "tư vấn giúp mình con chuột không dây", "sản phẩm nào đang hot",
        "điện thoại chụp ảnh đẹp tầm trung", "mình cần bàn phím cơ chơi game",
        "shop bán smartwatch không", "nên chọn iphone hay samsung",
    ],
    "khieu_nai": [
        "tôi muốn khiếu nại", "giao hàng quá chậm tôi rất bực", "nhân viên thái độ tệ",
        "sản phẩm không giống quảng cáo tôi muốn phàn nàn", "tôi không hài lòng chút nào",
        "shop làm ăn thế này à", "gửi khiếu nại ở đâu", "tôi muốn góp ý về dịch vụ",
        "hàng giao sai mà shop không xử lý", "quá thất vọng về shop",
        "tôi muốn phản ánh chất lượng phục vụ", "đây là trải nghiệm tệ nhất",
    ],
    "khuyen_mai": [
        "shop có khuyến mãi gì không", "có mã giảm giá không shop", "đang có sale gì",
        "chương trình ưu đãi tháng này", "có voucher cho khách mới không",
        "giảm giá sinh nhật thành viên thế nào", "flash sale khi nào diễn ra",
        "mua nhiều có giảm thêm không", "có mã freeship không", "ưu đãi cho học sinh sinh viên",
        "tích điểm đổi quà ra sao", "sắp tới có đợt giảm giá lớn không",
    ],
    "tai_khoan": [
        "quên mật khẩu thì làm sao", "đổi thông tin tài khoản thế nào",
        "tôi không đăng nhập được", "đăng ký tài khoản có lợi gì",
        "xóa tài khoản của tôi", "cập nhật số điện thoại trong tài khoản",
        "tài khoản bị khóa phải làm sao", "đổi địa chỉ giao hàng mặc định",
        "xem điểm tích lũy ở đâu", "tôi muốn thay email đăng nhập",
    ],
    "gio_lam_viec": [
        "shop mở cửa mấy giờ", "giờ làm việc của shop", "cuối tuần shop có mở không",
        "cửa hàng đóng cửa lúc mấy giờ", "ngày lễ shop có hoạt động không",
        "hotline hỗ trợ hoạt động mấy giờ", "shop làm việc đến mấy giờ tối",
        "chủ nhật có bán hàng không", "thời gian làm việc của bộ phận hỗ trợ",
    ],
    "lien_he_nhan_vien": [
        "cho tôi gặp nhân viên", "tôi muốn nói chuyện với người thật",
        "chuyển tôi gặp tư vấn viên", "gặp nhân viên hỗ trợ giúp tôi",
        "bot trả lời không đúng tôi cần gặp người", "cho xin số hotline gặp nhân viên",
        "kết nối tôi với bộ phận chăm sóc khách hàng", "tôi cần người hỗ trợ trực tiếp",
        "gặp admin giúp mình", "nhân viên đâu tôi cần hỗ trợ gấp",
    ],
    "cam_on": [
        "cảm ơn shop nhiều", "ok cảm ơn bạn", "tuyệt vời cảm ơn nhé",
        "cám ơn shop đã hỗ trợ", "rất hài lòng cảm ơn", "thanks shop",
        "cảm ơn tư vấn nhiệt tình", "mình hiểu rồi cảm ơn",
    ],
    "tam_biet": [
        "tạm biệt shop", "hẹn gặp lại", "bye shop nhé", "thôi mình đi đây",
        "chào tạm biệt", "gặp lại sau nhé", "bye bye",
    ],
}

INTENT_LABELS = {
    "chao_hoi": "Chào hỏi",
    "tra_don_hang": "Tra cứu đơn hàng",
    "van_chuyen": "Vận chuyển",
    "doi_tra": "Đổi trả",
    "bao_hanh": "Bảo hành",
    "thanh_toan": "Thanh toán",
    "tu_van_san_pham": "Tư vấn sản phẩm",
    "khieu_nai": "Khiếu nại",
    "khuyen_mai": "Khuyến mãi",
    "tai_khoan": "Tài khoản",
    "gio_lam_viec": "Giờ làm việc",
    "lien_he_nhan_vien": "Gặp nhân viên",
    "cam_on": "Cảm ơn",
    "tam_biet": "Tạm biệt",
}

# Knowledge base: mỗi mục thuộc 1 intent/chủ đề, có câu hỏi mẫu + câu trả lời chính sách.
# Đây là chính sách GIẢ ĐỊNH của shop minh họa TechZone, tự viết cho đồ án.
KB_SEED = [
    {"intent": "van_chuyen", "question": "Phí vận chuyển tính thế nào?",
     "answer": "TechZone tính phí ship theo khu vực: nội thành TP.HCM 25.000đ, các tỉnh 35.000đ. Đơn từ 500.000đ được MIỄN PHÍ giao hàng tiêu chuẩn. Giao hỏa tốc nội thành (2-4 giờ) phụ thu 40.000đ."},
    {"intent": "van_chuyen", "question": "Giao hàng mất bao lâu?",
     "answer": "Thời gian giao dự kiến: nội thành 1-2 ngày, tỉnh lân cận 2-3 ngày, toàn quốc 3-5 ngày làm việc. Đơn đặt trước 15h được xuất kho trong ngày."},
    {"intent": "van_chuyen", "question": "Đơn vị vận chuyển nào giao hàng?",
     "answer": "TechZone hợp tác với GHN và Viettel Post. Mã vận đơn được gửi qua SMS/email khi đơn ở trạng thái Đang giao (SHIPPING)."},
    {"intent": "doi_tra", "question": "Chính sách đổi trả của shop là gì?",
     "answer": "TechZone hỗ trợ đổi/trả trong 15 ngày kể từ ngày nhận hàng nếu sản phẩm lỗi kỹ thuật, sai mô tả hoặc hư hỏng khi vận chuyển. Sản phẩm cần còn nguyên tem, đầy đủ phụ kiện và hóa đơn."},
    {"intent": "doi_tra", "question": "Phí đổi trả ai chịu?",
     "answer": "Đổi trả do lỗi của shop (lỗi kỹ thuật, giao sai, vỡ do vận chuyển) được miễn phí hoàn toàn. Đổi vì lý do cá nhân (đổi màu/model) khách chịu phí ship 2 chiều."},
    {"intent": "doi_tra", "question": "Hoàn tiền mất bao lâu?",
     "answer": "Sau khi shop nhận và kiểm tra hàng trả đạt điều kiện, tiền hoàn về phương thức thanh toán gốc trong 3-5 ngày làm việc (COD hoàn qua chuyển khoản)."},
    {"intent": "bao_hanh", "question": "Chính sách bảo hành thế nào?",
     "answer": "Sản phẩm điện tử tại TechZone bảo hành chính hãng 12-24 tháng tùy dòng (laptop 24 tháng, điện thoại 12 tháng, phụ kiện 6 tháng). 1 đổi 1 trong 30 ngày đầu nếu lỗi phần cứng từ nhà sản xuất."},
    {"intent": "bao_hanh", "question": "Mang máy đi bảo hành cần gì?",
     "answer": "Khi bảo hành, bạn mang theo hóa đơn mua hàng (hoặc đọc số điện thoại đặt hàng) và phiếu bảo hành. Trung tâm bảo hành TechZone: 140 Lê Trọng Tấn, Tân Phú, TP.HCM, làm việc 8h30-20h30 hằng ngày."},
    {"intent": "thanh_toan", "question": "Shop hỗ trợ những hình thức thanh toán nào?",
     "answer": "TechZone hỗ trợ: COD (thanh toán khi nhận hàng), chuyển khoản ngân hàng, thẻ ATM/Visa qua cổng thanh toán, ví MoMo/ZaloPay và trả góp 0% qua thẻ tín dụng cho đơn từ 3.000.000đ."},
    {"intent": "thanh_toan", "question": "Trả góp cần thủ tục gì?",
     "answer": "Trả góp 0% áp dụng cho thẻ tín dụng của 20+ ngân hàng, kỳ hạn 3-12 tháng, đơn tối thiểu 3.000.000đ. Trả góp qua CCCD (Home Credit/ FE Credit) áp dụng tại cửa hàng cho đơn từ 2.000.000đ."},
    {"intent": "khuyen_mai", "question": "Shop đang có khuyến mãi gì?",
     "answer": "Chương trình hiện tại (minh họa): giảm đến 20% phụ kiện, tặng voucher 200.000đ cho đơn laptop từ 15.000.000đ, freeship mọi đơn từ 500.000đ. Khách mới đăng ký nhận voucher 50.000đ cho đơn đầu tiên."},
    {"intent": "khuyen_mai", "question": "Tích điểm thành viên thế nào?",
     "answer": "Mỗi 10.000đ chi tiêu tích 1 điểm. 100 điểm đổi voucher 50.000đ. Hạng Vàng (chi tiêu năm từ 20.000.000đ) được giảm thêm 3% và ưu tiên hỗ trợ."},
    {"intent": "tai_khoan", "question": "Quên mật khẩu thì làm sao?",
     "answer": "Bạn bấm 'Quên mật khẩu' ở trang đăng nhập, nhập email/SĐT đã đăng ký để nhận mã đặt lại mật khẩu. Nếu vẫn không được, gọi hotline 1900 6868 (số minh họa) để được hỗ trợ."},
    {"intent": "tai_khoan", "question": "Đổi số điện thoại trong tài khoản thế nào?",
     "answer": "Vào Tài khoản > Thông tin cá nhân > Số điện thoại, nhập SĐT mới và xác thực OTP. Lưu ý: SĐT gắn với tra cứu đơn hàng nên hãy cập nhật trước khi đặt đơn mới."},
    {"intent": "gio_lam_viec", "question": "Giờ làm việc của shop?",
     "answer": "Cửa hàng TechZone mở cửa 8h30-21h30 tất cả các ngày, kể cả cuối tuần. Bộ phận CSKH online hỗ trợ 8h-22h hằng ngày. Ngày lễ lớn shop vẫn bán online, giao hàng có thể chậm hơn 1-2 ngày."},
    {"intent": "tu_van_san_pham", "question": "Laptop nào phù hợp cho sinh viên?",
     "answer": "Tầm 13-16 triệu, bạn có thể tham khảo Laptop Học Tập Pro 14 (Core i5, RAM 16GB) học tập/văn phòng rất ổn. Nếu học đồ họa, nên chọn Laptop Đồ Họa Max 16 có card rời. Bạn cho bot biết ngân sách và nhu cầu để gợi ý sát hơn nhé."},
    {"intent": "tu_van_san_pham", "question": "Điện thoại nào bán chạy?",
     "answer": "Điện thoại bán chạy tại TechZone hiện là Smartphone X5 Pro và Smartphone A9. Tai nghe chống ồn bán chạy là Tai Nghe Không Dây SonicBuds Pro. Bạn muốn bot gợi ý theo tầm giá nào?"},
]

PRODUCTS = [
    "Laptop Học Tập Pro 14", "Laptop Đồ Họa Max 16", "Smartphone X5 Pro",
    "Smartphone A9", "Tai Nghe Không Dây SonicBuds Pro", "Chuột Không Dây M220",
    "Bàn Phím Cơ K87", "Máy Tính Bảng TabEdu 10", "Đồng Hồ Thông Minh FitWatch 2",
    "Loa Bluetooth BoomBox Mini",
]

ORDER_STATUS_VI = {
    "PENDING": "Chờ xác nhận",
    "PACKING": "Đang đóng gói",
    "SHIPPING": "Đang giao hàng",
    "DELIVERED": "Đã giao thành công",
    "CANCELLED": "Đã hủy",
    "RETURNING": "Đang xử lý đổi/trả",
}

# Đơn hàng mẫu DEMO — dữ liệu minh họa phục vụ đồ án.
ORDERS_SEED = [
    {"code": "TZ100001", "phone": "0901234567", "customer": "Nguyễn Văn An", "product": "Laptop Học Tập Pro 14", "qty": 1, "total": 14990000, "status": "SHIPPING", "tracking": "GHN88210001", "eta": "2024-11-22", "created": "2024-11-19"},
    {"code": "TZ100002", "phone": "0912345678", "customer": "Trần Thị Bình", "product": "Smartphone X5 Pro", "qty": 1, "total": 8990000, "status": "DELIVERED", "tracking": "GHN88210002", "eta": "2024-11-19", "created": "2024-11-17"},
    {"code": "TZ100003", "phone": "0901234567", "customer": "Nguyễn Văn An", "product": "Tai Nghe Không Dây SonicBuds Pro", "qty": 2, "total": 1598000, "status": "PENDING", "tracking": "", "eta": "", "created": "2024-11-20"},
    {"code": "TZ100004", "phone": "0933456789", "customer": "Lê Hoàng Cường", "product": "Bàn Phím Cơ K87", "qty": 1, "total": 1290000, "status": "PACKING", "tracking": "", "eta": "2024-11-23", "created": "2024-11-20"},
    {"code": "TZ100005", "phone": "0977889900", "customer": "Phạm Thu Dung", "product": "Smartphone A9", "qty": 1, "total": 5490000, "status": "CANCELLED", "tracking": "", "eta": "", "created": "2024-11-15"},
    {"code": "TZ100006", "phone": "0912345678", "customer": "Trần Thị Bình", "product": "Chuột Không Dây M220", "qty": 1, "total": 390000, "status": "DELIVERED", "tracking": "VTP55210006", "eta": "2024-11-16", "created": "2024-11-14"},
    {"code": "TZ100007", "phone": "0966554433", "customer": "Võ Minh Đức", "product": "Laptop Đồ Họa Max 16", "qty": 1, "total": 28990000, "status": "SHIPPING", "tracking": "GHN88210007", "eta": "2024-11-21", "created": "2024-11-18"},
    {"code": "TZ100008", "phone": "0909887766", "customer": "Đặng Ngọc Hà", "product": "Máy Tính Bảng TabEdu 10", "qty": 1, "total": 4990000, "status": "RETURNING", "tracking": "VTP55210008", "eta": "", "created": "2024-11-10"},
    {"code": "TZ100009", "phone": "0933456789", "customer": "Lê Hoàng Cường", "product": "Đồng Hồ Thông Minh FitWatch 2", "qty": 1, "total": 2990000, "status": "DELIVERED", "tracking": "GHN88210009", "eta": "2024-11-18", "created": "2024-11-16"},
    {"code": "TZ100010", "phone": "0988112233", "customer": "Bùi Thanh Phong", "product": "Loa Bluetooth BoomBox Mini", "qty": 3, "total": 2070000, "status": "PACKING", "tracking": "", "eta": "2024-11-23", "created": "2024-11-20"},
    {"code": "TZ100011", "phone": "0977889900", "customer": "Phạm Thu Dung", "product": "Smartphone X5 Pro", "qty": 1, "total": 8990000, "status": "SHIPPING", "tracking": "GHN88210011", "eta": "2024-11-22", "created": "2024-11-19"},
    {"code": "TZ100012", "phone": "0966554433", "customer": "Võ Minh Đức", "product": "Tai Nghe Không Dây SonicBuds Pro", "qty": 1, "total": 799000, "status": "PENDING", "tracking": "", "eta": "", "created": "2024-11-20"},
    {"code": "TZ100013", "phone": "0909887766", "customer": "Đặng Ngọc Hà", "product": "Smartphone A9", "qty": 2, "total": 10980000, "status": "DELIVERED", "tracking": "VTP55210013", "eta": "2024-11-20", "created": "2024-11-18"},
    {"code": "TZ100014", "phone": "0988112233", "customer": "Bùi Thanh Phong", "product": "Chuột Không Dây M220", "qty": 2, "total": 780000, "status": "CANCELLED", "tracking": "", "eta": "", "created": "2024-11-13"},
]
