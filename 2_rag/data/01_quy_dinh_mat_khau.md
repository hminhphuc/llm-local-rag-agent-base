# Quy định về mật khẩu và xác thực

**Mã văn bản:** QĐ-AN-001/2026
**Hiệu lực:** 01/01/2026
**Phân loại:** Công khai nội bộ

## 1. Phạm vi áp dụng
Áp dụng cho toàn bộ cán bộ, học viên, nhân viên có tài khoản truy cập hệ thống thông tin của đơn vị.

## 2. Yêu cầu độ phức tạp mật khẩu

- Tối thiểu 12 ký tự
- Bắt buộc có: chữ hoa, chữ thường, chữ số, ký tự đặc biệt
- Không trùng với 5 mật khẩu gần nhất
- Không chứa tên đăng nhập, họ tên, ngày sinh
- Không sử dụng từ điển phổ thông (password, 123456, qwerty…)

## 3. Chu kỳ thay đổi

- Tài khoản thường: 90 ngày
- Tài khoản quản trị: 60 ngày
- Tài khoản đặc quyền (root, domain admin): 30 ngày

## 4. Xác thực đa yếu tố (MFA)

Bắt buộc bật MFA cho:
- Tài khoản quản trị hệ thống
- Tài khoản truy cập từ xa (VPN, SSH)
- Tài khoản truy cập tài liệu mật cấp độ 2 trở lên

Phương thức MFA chấp nhận: TOTP (Google Authenticator, Microsoft Authenticator), khóa cứng FIDO2. Không chấp nhận SMS OTP cho tài khoản quản trị.

## 5. Xử lý vi phạm

- Lần 1: nhắc nhở bằng văn bản
- Lần 2: tạm khóa tài khoản 7 ngày
- Lần 3: báo cáo lãnh đạo, xem xét kỷ luật
