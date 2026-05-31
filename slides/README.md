# Slides — Workshop Local LLM + RAG + Agent

Slide deck **23 trang** cho buổi giảng 2 giờ — re-weight theo trọng tâm: **Local LLM là trục chính**, RAG thứ yếu, Agent chỉ demo. Framing chung chung cho nhiều đối tượng (không chỉ an ninh); trục bảo mật duy nhất = "dữ liệu của bạn không rời máy".

## Phân bổ slide theo trọng số

| Phần | Số slide | Vai trò |
|---|---|---|
| Mở đầu (1-4) | 4 | Title + 3 lý do chạy local + "bạn thấy mình trong đó" + roadmap |
| **Phần 1 — Local LLM (5-13)** | **9 (trục chính)** | Ollama, 5 ưu điểm, demo, API, **chọn model theo máy**, **bản đồ thuật ngữ**, thực hành |
| Phần 2 — RAG (14-20) | 7 | Bài toán, pipeline, embedding, demo, thực hành (thả tài liệu của bạn) |
| Phần 3 — Agent (21-23 gốc → gộp) | 3 | Chỉ demo single-tool + định hướng tự học |
| Đóng | 3 | 3 thành quả + 3 việc tuần này + bảo mật mang về + Q&A |

## File chính

| File | Định dạng | Dùng khi nào |
|---|---|---|
| **`SLIDES.pptx`** | PowerPoint | Trình chiếu chính, có thể edit |
| **`SLIDES.pdf`** | PDF | Backup, in, gửi học viên |
| **`SLIDES.html`** | HTML | Browser fullscreen + presenter mode |
| **`SLIDES.md`** | Markdown source | Edit nội dung, version control |
| **`theme.css`** | Theme styling | Custom design navy + blue |

> Cả 3 bản (PPTX/PDF/HTML) đều render từ `SLIDES.md` hiện tại — nội dung đồng nhất (đa-đối-tượng, qwen3:1.7b).

## Cấu trúc 23 slides

| Slide | Phần | Nội dung |
|---|---|---|
| 1 | Title (lead) | Local LLM · RAG · Agent |
| 2 | Mở đầu | Vì sao chạy LLM trên máy mình? (3 lý do phổ quát) |
| 3 | Mở đầu | Bạn thấy mình trong đó chứ? (đa đối tượng) |
| 4 | Mở đầu | Roadmap — 3 module, trọng số rõ ràng |
| **5** | **divider** | **Phần 1 · Trục chính** |
| 6 | Phần 1 | Ollama = "Docker cho LLM" |
| 7 | Phần 1 | 5 ưu điểm nhớ ngay |
| 8 | Phần 1 | Demo: 5 dòng code = LLM chạy local |
| 9 | Phần 1 | Chọn model theo MÁY của bạn (RAM ↔ size) |
| 10 | Phần 1 | Bản đồ thuật ngữ (cho người mới) |
| 11 | Phần 1 | 🛠️ Thực hành Phần 1 · 22 phút |
| **12** | **divider** | **Phần 2 · Thứ yếu nhưng quan trọng** |
| 13 | Phần 2 | Bài toán: AI không biết tài liệu của BẠN |
| 14 | Phần 2 | RAG pipeline — 5 bước (diagram) |
| 15 | Phần 2 | Embedding — bước "ma thuật" |
| 16 | Phần 2 | Demo RAG (terminal + Open WebUI) |
| 17 | Phần 2 | 🛠️ Thực hành Phần 2 · 19 phút (thả tài liệu của bạn) |
| **18** | **divider** | **Phần 3 · Giới thiệu (chỉ demo)** |
| 19 | Phần 3 | Agent = LLM + Tools + ReAct loop (diagram) |
| 20 | Phần 3 | Demo Agent |
| 21 | Tổng kết | Sau 2 giờ bạn đã làm được + 3 việc tuần này |
| 22 | Tổng kết | Một điểm bảo mật để mang về + đọc thêm handbook |
| 23 | Q&A (lead) | Cảm ơn + Q&A |

## Triết lý thiết kế

- **1 slide = 1 takeaway** — học viên đọc xong nhớ được 1 ý chính
- **Re-weight**: Phần 1 (Local LLM) 7 slide = trục chính; Phần 2 (RAG) 6 slide; Phần 3 (Agent) 3 slide = chỉ demo
- **Diagram + screenshot làm trục**, chữ tối thiểu
- **Framing đa đối tượng** + trục bảo mật duy nhất "dữ liệu không rời máy"

## Theme design

- **Font**: Segoe UI / Inter
- **Palette**: Navy `#0f172a` + Blue `#1e40af` + Accent `#06b6d4`
- **Code blocks**: Dark theme syntax highlighting
- **3 layout chính**:
  - `lead` — title gradient
  - `divider` — section divider  
  - `demo` — dark theme cho code

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
| 14 (RAG pipeline) | `docs/diagrams/02_rag_pipeline.png` |
| 15 (embedding) | `docs/diagrams/04_embedding_space.png` |
| 16 (RAG demo) | `terminal_rag_query.png` + `open_webui_rag_real.png` |
| 19 (ReAct loop) | `docs/diagrams/03_react_loop.png` |
| 20 (Agent trace) | `docs/screenshots/terminal_agent_trace.png` |

Tài liệu chi tiết bổ trợ: `../docs/TAI_LIEU_CHI_TIET.docx`
Kịch bản nói chi tiết: `../KICH_BAN_GIANG.md`
