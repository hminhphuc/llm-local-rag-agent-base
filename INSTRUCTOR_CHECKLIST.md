# ✅ Checklist giảng viên — 1 trang

> Gom mọi việc cần làm để buổi 2h chạy mượt. Chi tiết kịch bản nói: [KICH_BAN_GIANG.md](KICH_BAN_GIANG.md). Các lỗi đã biết: [BAO_CAO_TEST.md](BAO_CAO_TEST.md).
> **Quy tắc vàng:** mọi độ trễ trên CPU là thật (RAG 15–25s). Pre-build + warm model trước thì 2h vừa khít; không thì sẽ thấy gấp.

---

## ⏰ Trước buổi 3 ngày — email học viên
- [ ] Yêu cầu chạy **`setup.ps1`/`setup.sh` + `pull_models`** ở nhà (tải ~1.7GB, **không** tải lại tại lớp).
- [ ] **Nếu dùng Open WebUI** (giao diện chat chính trên lớp): nhắc cài trước [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- [ ] Nhắc máy công ty (Windows): test trước lệnh `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. Bị chặn → báo IT hoặc ngồi cạnh bạn.
- [ ] Ai lỡ chưa setup: mang USB hoặc chấp nhận chờ.

## 🔧 Trước buổi 30 phút — trên máy giảng
- [ ] **Bật Ollama** (Windows: icon khay hệ thống; mac/Linux: `ollama serve`) — mọi bước dưới cần Ollama đang chạy.
- [ ] **Pull sẵn image Open WebUI** (~1GB, lần đầu 2–5'): `docker compose pull` — không thì `docker compose up -d` đầu buổi sẽ khóa ~5'.
- [ ] **Pre-build index RAG**: `python rag_app.py --build` (~30s) — `chroma_db/` KHÔNG có sẵn trong repo, không build trước thì Module 2 đứng hình giữa demo.
- [ ] **Warm model** (quan trọng nhất cho hook mở màn): chạy thử 1 lần để nạp model vào cache:
  - `python 1_ollama_basics/01_chat.py`
  - `python rag_app.py --ask "Quy trình xử lý sự cố ATTT?"`
- [ ] (Tùy chọn) Build model custom: sửa `Modelfile.anninh` → `FROM qwen3:1.7b`, `ollama create anninh -f 1_ollama_basics/Modelfile.anninh`.
- [ ] Mở sẵn & xếp split-screen: **terminal** + **jupyter lab** (`1_ollama_basics/notebook.ipynb`) + **Open WebUI** (`docker compose up -d` → http://localhost:3000). Tránh mất thời gian chuyển cảnh giữa các module.
- [ ] **USB/LAN dự phòng**: chép sẵn model (qwen3:1.7b + nomic-embed-text) **và** thư mục `chroma_db/` đã build — cứu học viên thiếu setup.
- [ ] Mở sẵn 4 ảnh fallback trong `docs/screenshots/` (open_webui + 3 terminal — phòng demo chậm).

## ✅ 5 phút đầu giờ — health check cả lớp
- [ ] Cho cả lớp chạy **`ollama list`** → giơ tay ai thiếu model. Xử lý nhóm nhỏ bằng USB trong lúc giảng Phần 0 (roadmap).
- [ ] **Demo `bật venv` trên máy chiếu** (non-dev hay đứng hình ở đây): `\.venv\Scripts\Activate.ps1` (Win) / `source .venv/bin/activate` (mac/Linux).

---

## ⏱️ Bảng thời lượng (98' nội dung trong khung 2h — bảo vệ Q&A)

| Phần | Thời lượng | Ghi chú giữ nhịp |
|---|---|---|
| 0. Mở đầu + demo tắt Wi-Fi | 8' | Warm model trước! Stall 30s ở đây là mất lớp |
| 1. Local LLM (giảng) | 22' | Trục chính |
| **1. Thực hành** | **18' công bố + 4' "cứu hộ"** | Cap từng task ↓ |
| 2. RAG (giảng) | 15' | Pre-run notebook để clear output cũ |
| **2. Thực hành** | **15' công bố + 4' "cứu hộ"** | Dùng câu hỏi an toàn ↓ |
| 3. Tổng kết + Q&A | 12' | Có FAQ thủ sẵn nếu lớp im |

**Cap từng task thực hành Module 1** (để 1 người kẹt không kéo cả lớp): Task 1–2 (CLI) ~5' · Task 3 (Python) ~8' · Task 4 (Modelfile) ~6' · Task 5 (temperature) ~3'. Hết giờ là chuyển, phần còn lại để về nhà.

---

## 💬 Câu hỏi RAG chạy chắc — đưa cho học viên
> Embedding **trượt** với mã ngắn ("P1", "MFA"...) → học viên tưởng RAG hỏng. Bảo họ **thử các câu này trước**, rồi mới biến tấu:
- ✅ "Quy trình xử lý sự cố ATTT gồm những bước nào?"
- ✅ "USB cá nhân có được dùng không?"
- ✅ "Có được forward email công vụ sang gmail?"
- ✅ "Quy định mật khẩu của đơn vị?"

(Các câu này cũng có sẵn làm gợi ý trong notebook và Open WebUI.)

## 🖥️ Demo: chạy gì LIVE, fallback gì
| Demo | Live | Fallback nếu chậm/lỗi |
|---|---|---|
| Tắt Wi-Fi vẫn chạy | ✅ (đã warm) | Video/ảnh đã quay sẵn |
| Chat 5 dòng (Module 1) | ✅ | `docs/screenshots/terminal_ollama_chat.png` |
| RAG query + Open WebUI | ✅ 1 câu | `terminal_rag_query.png` + `open_webui_rag_real.png` |

## ⚠️ Bẫy đã biết (từ BAO_CAO_TEST.md)
- **qwen3:4b vẫn "nghĩ ra mặt giấy"** dù `think=False` → **đừng chọn 4b để demo** dù máy mạnh; 1.7b cho output sạch hơn.
- File upload chỉ đọc **`.md`/`.txt`** (không đọc PDF). Có sẵn file mẫu: [`2_rag/sample_upload/`](2_rag/sample_upload/) cho ai không mang tài liệu.

## 🆘 Sự cố → xử lý nhanh
| Sự cố | Xử lý |
|---|---|
| Ollama không phản hồi | `ollama serve` ở terminal khác |
| Pull/demo chậm | Chuyển sang model đã pull sẵn, đừng đứng chờ |
| `ModuleNotFoundError` | Học viên quên bật venv → activate lại |
| Cổng 3000 bận | Đã có tiến trình chạy — dùng luôn, hoặc đóng cái cũ |
| Module 2 "Lỗi truy vấn RAG" | Chưa build index → `python rag_app.py --build` |
