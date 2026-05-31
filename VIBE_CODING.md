# Biến workshop này thành dự án của bạn

> Hướng dẫn dùng AI assistant (Cursor, Claude Code, GitHub Copilot…) để mở rộng repo này theo nhu cầu thật, không cần viết code từ đầu.

## Tinh thần "vibe coding"

Repo này được thiết kế để:
- Mỗi module **tự đứng độc lập** — sửa 1 module không ảnh hưởng module khác
- Tên file, tên hàm, comment đều **rõ nghĩa** — AI hiểu được context ngay
- Có **dataset mẫu sạch** — bạn fork về, thay bằng data thật là dùng được
- Có **README đầy đủ** ở mỗi thư mục — AI assistant đọc README để hiểu cấu trúc

## 5 prompt mẫu để mở rộng repo

### 1. Thay dataset bằng tài liệu của bạn

Mở Cursor/Claude Code tại thư mục repo, paste:

```
Tôi muốn dùng tài liệu PDF trong C:/MyDocs/AnNinhDonVi/ thay cho dataset mẫu.
Hãy:
1. Cài thư viện pypdf nếu chưa có
2. Sửa 2_rag/rag_minimal.py: hàm load_documents() đọc cả .md và .pdf,
   với .pdf thì dùng pypdf để extract text từ tất cả trang
3. Đổi DATA_DIR sang đường dẫn mới
4. Chạy lại --build và kiểm tra
```

### 2. Thêm tool mới cho agent

```
Trong 3_agent/tools/, thêm tool check_hash_virustotal(sha256):
- Gọi API https://www.virustotal.com/api/v3/files/{hash}
- Đọc API key từ env var VIRUSTOTAL_API_KEY
- Trả về dict gồm: hash, malicious_count, total_engines, detection_names (list top 3)
- Nếu API trả 404, return malicious=False
- Đăng ký vào agent_simple.py
```

### 3. Đổi model

```
Đổi LLM mặc định trong toàn repo từ qwen3:4b sang llama3.2:3b.
Tìm và thay tất cả reference (Python files, README, Modelfile, docker-compose).
Cập nhật pull_models.ps1 để pull đúng model mới.
```

### 4. Thêm metadata filter cho RAG

```
Trong 2_rag/rag_minimal.py:
- Thêm field 'level' (0/1/2/3) vào metadata khi index, parse từ dòng "Phân loại:" trong markdown
- Thêm tham số --max-level cho --ask để chỉ retrieve trong tài liệu có level <= max
- Mặc định max_level=1 (chỉ tài liệu Công khai + Nội bộ)
- Cập nhật README giải thích tính năng
```

### 5. Build app riêng dựa trên template

```
Tôi muốn build một app phân tích log bảo mật:
- Reuse module 1, 2, 3 của workshop
- Web UI để upload file log (.log, .txt) — dùng Open WebUI, hoặc tự viết bằng Gradio/FastAPI
- Agent phân tích: tìm anomaly, đối chiếu chính sách nội bộ, gợi ý hành động
- Export kết quả ra Markdown report

Hãy tạo thư mục mới apps/log_analyzer/, viết app.py và README.
```

## Best practice khi vibe-coding

### Cung cấp context rõ ràng
- Tag thư mục cụ thể (`2_rag/`) thay vì nói chung "RAG"
- Đề cập file gốc nếu sửa (`Sửa hàm chunk_text trong 2_rag/rag_minimal.py`)
- Mô tả input/output mong muốn cho hàm mới

### Yêu cầu nhỏ rồi mở rộng
Đừng paste 1 prompt 500 chữ. Chia thành:
1. "Thêm hàm A" → kiểm tra
2. "Bây giờ thêm hàm B dùng A" → kiểm tra
3. "Tích hợp vào CLI" → kiểm tra

### Luôn test sau mỗi thay đổi
```powershell
# Test nhanh sau khi sửa
python 2_rag/rag_minimal.py --build
python 2_rag/rag_minimal.py --ask "câu test"
```

### Backup trước khi sửa lớn
```powershell
git init    # nếu chưa
git add -A; git commit -m "before-change"
# rồi mới bảo AI sửa
```

## Câu hỏi thường gặp

### Vibe-coding có an toàn cho code production không?
**Không, nếu không review.** Nguyên tắc:
- Luôn đọc diff trước khi accept
- Test pipeline đầu-cuối sau mỗi sửa
- Đặc biệt cảnh giác với code có `subprocess`, `eval`, `open()` với path từ user

### AI assistant có upload code của tôi không?
- **Claude Code (Anthropic API)**: code được gửi đến Anthropic. Đọc terms.
- **Cursor**: có chế độ Privacy Mode tắt training.
- **Continue + Ollama**: 100% local nếu dùng model local.

→ Với data nhạy cảm, dùng Continue extension + Ollama là an toàn nhất.

### Làm sao biết AI hiểu đúng repo?
Hỏi nó trước khi cho sửa:
```
Hãy đọc README.md, 2_rag/rag_minimal.py và 3_agent/agent_simple.py,
sau đó tóm tắt kiến trúc trong 5 gạch đầu dòng. KHÔNG sửa gì cả.
```
Nếu tóm tắt sai → cung cấp thêm context, đừng để nó sửa code.
