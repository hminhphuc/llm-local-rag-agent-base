# Quy định bảo vệ dữ liệu cá nhân

**Mã văn bản:** QĐ-AN-006/2026
**Hiệu lực:** 01/01/2026
**Căn cứ:** Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân

## 1. Định nghĩa

**Dữ liệu cá nhân (DLCN)**: thông tin nhận diện hoặc giúp nhận diện một cá nhân cụ thể.

**DLCN cơ bản**: họ tên, ngày sinh, giới tính, nơi sinh, quốc tịch, hình ảnh, số điện thoại, CMND/CCCD, biển số xe, mã số thuế, email, tài khoản số, dữ liệu phản ánh hoạt động trên không gian mạng.

**DLCN nhạy cảm**: quan điểm chính trị, tôn giáo, sức khỏe, di truyền, sinh trắc học, xu hướng tính dục, vị trí địa lý, tình trạng pháp lý, tài chính cá nhân, dữ liệu trẻ em.

## 2. Nguyên tắc xử lý

1. **Hợp pháp**: có cơ sở pháp lý rõ ràng
2. **Minh bạch**: thông báo cho chủ thể dữ liệu
3. **Mục đích cụ thể**: chỉ thu thập cho mục đích đã thông báo
4. **Tối thiểu**: chỉ thu thập dữ liệu thực sự cần thiết
5. **Chính xác**: cập nhật, sửa chữa kịp thời
6. **Lưu trữ có thời hạn**: xóa khi hết mục đích
7. **Bảo mật**: áp dụng biện pháp kỹ thuật phù hợp

## 3. Quyền của chủ thể dữ liệu

Chủ thể có quyền:
- Biết về việc xử lý DLCN của mình
- Đồng ý/rút lại sự đồng ý
- Truy cập, sửa đổi, xóa DLCN
- Hạn chế xử lý
- Phản đối xử lý
- Yêu cầu cung cấp DLCN
- Khiếu nại, tố cáo, khởi kiện
- Yêu cầu bồi thường thiệt hại

## 4. Biện pháp bảo vệ kỹ thuật

### Khi lưu trữ
- Mã hóa DLCN nhạy cảm khi lưu (encryption at rest)
- Phân quyền truy cập theo nguyên tắc least privilege
- Ghi nhật ký mọi truy cập, lưu trữ 2 năm

### Khi truyền
- Sử dụng kênh mã hóa (TLS 1.2 trở lên)
- Cấm gửi DLCN nhạy cảm qua email không mã hóa
- Cấm in DLCN nhạy cảm ra giấy nếu không cần thiết

### Khi xử lý bằng AI/RAG
- Cấm đưa DLCN nhạy cảm vào prompt của LLM thương mại (OpenAI, Google…)
- Nếu dùng LLM phải dùng deployment local (Ollama, vLLM) hoặc instance riêng tư
- Redact DLCN trước khi embed vào vector DB nếu vector có thể bị reverse

## 5. Vi phạm và xử lý

- Báo cáo Bộ Công an trong 72 giờ nếu xảy ra rò rỉ DLCN
- Thông báo chủ thể bị ảnh hưởng nếu rò rỉ có thể gây thiệt hại
- Phạt hành chính tới 100 triệu đồng (NĐ 13/2023, Điều 7)
- Trường hợp nghiêm trọng: truy cứu trách nhiệm hình sự theo Bộ luật Hình sự
