# Quy định phân loại tài liệu

**Mã văn bản:** QĐ-AN-002/2026
**Hiệu lực:** 01/01/2026

## 1. Bốn cấp độ phân loại

| Cấp độ | Tên gọi | Mô tả | Màu nhãn |
|---|---|---|---|
| 0 | Công khai | Có thể public, không gây thiệt hại | Xanh lá |
| 1 | Nội bộ | Chỉ trong đơn vị, lộ ra gây phiền hà | Vàng |
| 2 | Mật | Lộ ra gây thiệt hại nghiêm trọng | Cam |
| 3 | Tuyệt mật | Lộ ra gây thiệt hại đặc biệt nghiêm trọng | Đỏ |

## 2. Quy tắc lưu trữ

### Cấp độ 0 - Công khai
- Lưu trên hệ thống thông thường
- Có thể đăng cổng thông tin điện tử

### Cấp độ 1 - Nội bộ
- Lưu trên file server nội bộ
- Yêu cầu đăng nhập tài khoản đơn vị
- Không gửi qua email cá nhân (gmail, outlook.com…)

### Cấp độ 2 - Mật
- Lưu trên hệ thống chuyên dụng có mã hóa AES-256
- Truy cập yêu cầu MFA
- Chỉ in ra giấy khi có phê duyệt, đóng dấu "MẬT" mọi trang
- Cấm chụp ảnh màn hình, sao chép USB không được cấp phép

### Cấp độ 3 - Tuyệt mật
- Lưu trên hệ thống vật lý cách ly (air-gap)
- Chỉ thao tác trong phòng chuyên dụng có giám sát
- Cấm tuyệt đối thiết bị cá nhân vào khu vực xử lý
- Mọi truy cập ghi nhật ký, lưu trữ 10 năm

## 3. Quy tắc gửi và chia sẻ

- Tài liệu Mật trở lên: chỉ gửi qua hệ thống mã hóa nội bộ
- Khi chia sẻ với đơn vị ngoài: phải có công văn chính thức, ký số
- Cấm chuyển tiếp tự động (auto-forward) email chứa tài liệu Mật

## 4. Hủy tài liệu

- Tài liệu giấy cấp 2-3: hủy bằng máy nghiền chéo (cross-cut), không đốt
- Tài liệu số: xóa bằng công cụ wipe chuẩn DoD 5220.22-M, không chỉ delete bình thường
- Lập biên bản hủy có chữ ký 2 cán bộ chứng kiến
