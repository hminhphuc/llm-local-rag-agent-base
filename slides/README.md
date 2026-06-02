# Slides — Workshop Local LLM + RAG

Slide deck cho buổi giảng 2 giờ — re-weight theo trọng tâm: **Local LLM là trục chính**, RAG thứ yếu. Framing chung chung cho nhiều đối tượng (không chỉ an ninh); trục bảo mật duy nhất = "dữ liệu của bạn không rời máy".

> 🖥️ **Mạch hands-on mỗi module = 3 nhịp trực quan:** **Làm gì & ở đâu** (ảnh Jupyter Lab thật + nơi thực hiện + bước chính) → **Làm theo** (slide nền tối, đúng lệnh PowerShell để gõ + ghi chú mac/Linux) → **Kết quả đúng** (ảnh terminal thật + ô xanh "✓ ra như vầy là đúng"). Người làm biết gõ gì ở đâu; người chỉ xem cũng hình dung được các bước + kết quả. Ảnh thật tạo bằng `docs/capture_jupyter.py` (Jupyter) và `docs/render_real_output.py` (terminal).

## Phân bổ slide

| Phần | Vai trò |
|---|---|
| Mở đầu | Title + lý do chạy local + roadmap |
| **Phần 1 — Local LLM** | **Trục chính**: Ollama, ưu điểm, demo, model, thuật ngữ + **làm gì&ở đâu → lệnh → kết quả (M1)** |
| Phần 2 — RAG | Bài toán, pipeline, embedding + **làm gì&ở đâu → lệnh → kết quả (M2) + Open WebUI** |
| Đóng | Thành quả + bảo mật mang về + Q&A |

## File chính

| File | Định dạng | Dùng khi nào |
|---|---|---|
| **`SLIDES.pptx`** | PowerPoint | Trình chiếu chính, có thể edit |
| **`SLIDES.pdf`** | PDF | Backup, in, gửi học viên |
| **`SLIDES.html`** | HTML | Browser fullscreen + presenter mode |
| **`SLIDES.md`** | Markdown source | Edit nội dung, version control |
| **`theme.css`** | Theme styling | Custom design navy + blue |

> Cả 3 bản (PPTX/PDF/HTML) đều render từ `SLIDES.md` hiện tại — nội dung đồng nhất (đa-đối-tượng, qwen3:1.7b).

## Cấu trúc slide

> Mỗi module = 3 nhịp in đậm: **làm gì & ở đâu** (ảnh Jupyter thật) → **làm theo** (lệnh, nền tối) → **kết quả** (ảnh terminal thật + ✓).

| Slide | Phần | Nội dung |
|---|---|---|
| 1 | Title (lead) | Local LLM · RAG |
| 2 | Mở đầu | Vì sao chạy LLM trên máy mình? (3 lý do phổ quát) |
| 3 | Mở đầu | Bạn thấy mình trong đó chứ? (đa đối tượng) |
| 4 | Mở đầu | Roadmap — 2 module |
| **5** | **làm theo** | **Chuẩn bị — bật môi trường (lệnh)** |
| **6** | **divider** | **Phần 1 · Trục chính** |
| 7 | Phần 1 | Ollama = "Docker cho LLM" |
| 8 | Phần 1 | 5 ưu điểm nhớ ngay |
| 9 | Phần 1 | Demo: 5 dòng code (+ lệnh chạy) |
| 10 | Phần 1 | Chọn model theo MÁY của bạn (RAM ↔ size) |
| 11 | Phần 1 | Bản đồ thuật ngữ (cho người mới) |
| **12** | **làm gì & ở đâu** | **Module 1 — ảnh Jupyter Lab thật + bước chính** |
| **13** | **làm theo** | **Module 1 — lệnh Local LLM** |
| **14** | **kết quả** | **Kết quả đúng — Module 1 (ảnh + ✓)** |
| **15** | **divider** | **Phần 2 · Thứ yếu nhưng quan trọng** |
| 16 | Phần 2 | Bài toán: AI không biết tài liệu của BẠN |
| 17 | Phần 2 | RAG pipeline (diagram banner) |
| 18 | Phần 2 | Embedding |
| **19** | **làm gì & ở đâu** | **Module 2 — ảnh Jupyter Lab thật + bước chính** |
| **20** | **làm theo** | **Module 2 — lệnh RAG** |
| **21** | **kết quả** | **Kết quả đúng — RAG (ảnh + ✓)** |
| 22 | Phần 2 | Open WebUI — giao diện như ChatGPT |
| … | Tổng kết | Sau 2 giờ bạn đã làm được + 3 việc tuần này |
| … | Tổng kết | Một điểm bảo mật để mang về + đọc thêm handbook |
| … | Q&A (lead) | Cảm ơn + Q&A |

## Triết lý thiết kế

- **1 slide = 1 takeaway** — học viên đọc xong nhớ được 1 ý chính
- **Re-weight**: Phần 1 (Local LLM) = trục chính; Phần 2 (RAG) = thứ yếu nhưng quan trọng
- **Diagram + screenshot làm trục**, chữ tối thiểu
- **Framing đa đối tượng** + trục bảo mật duy nhất "dữ liệu không rời máy"

## Theme design (refresh 2026)

- **Font**: Inter (fallback Segoe UI) — đổi độ đậm thay vì đổi font
- **Palette tối giản**: Ink `#0b1324` + 1 accent xanh `#2563eb` + nền/xám trung tính
- **Nhịp dọc nhất quán**: mọi slide nội dung top-align, tiêu đề cùng cao độ + accent bar mảnh bên dưới
- **Box phẳng**: nền nhạt + viền trái accent, bỏ gradient/đổ bóng nặng
- **Không emoji trang trí** (giữ ✅ ở slide tổng kết)
- **Ảnh**: dùng đơn vị px (Marp bỏ qua `w:%` cho ảnh inline), tự căn giữa
- **3 layout chính**: `lead` (title gradient) · `divider` (section) · `demo` (dark cho code)

## Rebuild khi sửa nội dung

```bash
# Yêu cầu: Node.js + Marp CLI
npm install -g @marp-team/marp-cli

cd slides

# Export 3 format (ghi đè cùng tên SLIDES.*)
marp SLIDES.md --theme theme.css -o SLIDES.pptx --allow-local-files
marp SLIDES.md --theme theme.css --pdf SLIDES.pdf --allow-local-files
marp SLIDES.md --theme theme.css --html SLIDES.html --allow-local-files
```

> **Lưu ý khi rebuild**: nếu PowerPoint đang mở `SLIDES.pptx` → đóng trước khi export (file bị lock). Tránh ký tự `$` trong slide (Marp hiểu nhầm là LaTeX) → viết "USD" thay vì "$".

## Tips trình chiếu

### PowerPoint
- Mở `SLIDES.pptx` → F5 trình chiếu
- Có thể chỉnh ad-hoc trong PowerPoint trước buổi

### PDF
- Mở `SLIDES.pdf` → Ctrl+L (fullscreen Acrobat) hoặc F11 (browser)
- Phím `←` `→` chuyển

### HTML (best cho presenter)
- Mở `SLIDES.html` trong browser
- `p` — presenter view (có notes)
- `f` — fullscreen
- `o` — overview tất cả slide

## Cross-reference với tài liệu khác

| Slide | Diagram / Screenshot |
|---|---|
| RAG pipeline | `docs/diagrams/02_rag_pipeline.png` |
| embedding | `docs/diagrams/04_embedding_space.png` |
| RAG demo | `terminal_rag_query.png` + `open_webui_rag_real.png` |

Tài liệu chi tiết bổ trợ: `../docs/TAI_LIEU_CHI_TIET.docx`
Kịch bản nói chi tiết: `../KICH_BAN_GIANG.md`
