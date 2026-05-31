# Quy trình xử lý sự cố an toàn thông tin

**Mã văn bản:** QĐ-AN-003/2026
**Hiệu lực:** 01/01/2026

## 1. Phân loại sự cố

| Mức | Tên | Ví dụ | SLA phản hồi |
|---|---|---|---|
| P1 | Nghiêm trọng | Mất kiểm soát hệ thống, lộ tài liệu Mật, ransomware | 15 phút |
| P2 | Cao | Tài khoản quản trị bị xâm nhập, DDoS gây gián đoạn dịch vụ | 1 giờ |
| P3 | Trung bình | Phát hiện malware trên 1 máy, lừa đảo qua email | 4 giờ |
| P4 | Thấp | Cảnh báo IDS, đăng nhập sai liên tiếp | 24 giờ |

## 2. Quy trình 6 bước (NIST SP 800-61)

### Bước 1 - Chuẩn bị (Preparation)
- Duy trì danh sách liên hệ ứng cứu (CIRT)
- Cập nhật playbook cho từng loại sự cố
- Diễn tập 6 tháng/lần

### Bước 2 - Phát hiện và phân tích (Detection & Analysis)
- Tiếp nhận cảnh báo từ SIEM, IDS, người dùng báo cáo
- Xác định mức độ ưu tiên (P1-P4)
- Thu thập bằng chứng ban đầu (log, memory dump, snapshot)

### Bước 3 - Cách ly (Containment)
- Cách ly ngắn hạn: chặn IP, disable account, ngắt mạng máy bị nhiễm
- Cách ly dài hạn: cài lại OS, đổi credentials, vá lỗ hổng
- Bảo vệ bằng chứng: không tắt máy, làm bản sao đĩa cứng

### Bước 4 - Diệt trừ (Eradication)
- Gỡ bỏ malware, backdoor, web shell
- Vá lỗ hổng gốc đã bị khai thác
- Quét lại toàn bộ hệ thống liên quan

### Bước 5 - Phục hồi (Recovery)
- Khôi phục dịch vụ từ backup sạch
- Theo dõi tăng cường trong 30 ngày
- Xác nhận hệ thống hoạt động bình thường

### Bước 6 - Bài học kinh nghiệm (Lessons Learned)
- Họp review trong 2 tuần sau sự cố
- Cập nhật playbook và quy trình
- Báo cáo lãnh đạo, lưu hồ sơ 5 năm

## 3. Liên hệ ứng cứu (CIRT)

- Trực tổng đài: 24/7
- Email: cirt@donvi.gov.vn
- Hotline nội bộ: 1900-XXX
- Khi sự cố P1: gọi điện thoại trực tiếp, KHÔNG chỉ gửi email

## 4. Báo cáo bên ngoài

Sự cố P1-P2 liên quan tài liệu Mật phải báo cáo:
- Cục An toàn thông tin (trong 24 giờ)
- Lãnh đạo trực tiếp (ngay khi xác nhận)
- Đơn vị liên quan nếu ảnh hưởng tới đối tác
