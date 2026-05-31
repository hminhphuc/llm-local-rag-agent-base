# Thư mục docs/ — Tài liệu Word & assets

> 🛠️ **Học viên không cần đụng tới thư mục này.** Đây là chỗ chứa file Word của handbook + sơ đồ + script để **build lại tài liệu**. Để học, chỉ cần đọc [TAI_LIEU_CHI_TIET.md](../TAI_LIEU_CHI_TIET.md) (hoặc bản [.docx](TAI_LIEU_CHI_TIET.docx)). Mục dưới đây dành cho người bảo trì repo.

Thư mục này chứa file Word của handbook + các asset (diagrams, screenshots) + scripts để rebuild.

## File chính

| File | Mô tả |
|---|---|
| **`TAI_LIEU_CHI_TIET.docx`** | Bản Word của handbook, có cover page + 12 diagram/screenshot + TOC tự sinh + footer page number |
| `reference.docx` | Template style pandoc dùng để convert (Calibri 11pt body, Heading 1 navy 18pt...) |

## Asset

| Thư mục | Nội dung |
|---|---|
| `diagrams/` | 8 Mermaid source `.mmd` + 8 PNG render (architecture, RAG pipeline, ReAct loop, MCP...) |
| `screenshots/` | Terminal output (Ollama/RAG/Agent) vẽ từ output thật bằng `render_real_output.py`; Gradio UI là ảnh chụp thật (`gradio_ui_real.png`, `gradio_ui_chat_real.png` qua `capture_gradio.py`) |

## Cách rebuild khi sửa nội dung

Khi anh sửa `TAI_LIEU_CHI_TIET.md` ở root repo:

```bash
# Activate venv (đã tạo từ workshop setup)
source .venv/bin/activate          # macOS/Linux
.\.venv\Scripts\Activate.ps1       # Windows

# Cài deps cần cho build (chỉ chạy 1 lần)
pip install -r docs/requirements-docs.txt

# Rebuild
python docs/build_docx.py
```

Output: `docs/TAI_LIEU_CHI_TIET.docx` được overwrite.

## Cách sửa diagram

Sửa file `.mmd` trong `diagrams/`, sau đó:

```bash
cd docs/diagrams
mmdc -i 01_overall_architecture.mmd -o 01_overall_architecture.png -b white -w 1400 -H 900 --scale 2
```

Yêu cầu: `npm install -g @mermaid-js/mermaid-cli` (đã có sẵn nếu anh từng cài).

Cú pháp Mermaid: [mermaid.js.org](https://mermaid.js.org/intro/)
Live editor: [mermaid.live](https://mermaid.live)

## Cách cập nhật terminal screenshot

Các ảnh terminal (Ollama/RAG/Agent) được vẽ lại từ **output thật** bằng `render_real_output.py` (chạy code → chép output vào script → render PNG terminal đẹp):

```bash
python docs/render_real_output.py
```

Gradio UI (`gradio_ui_real.png`, `gradio_ui_chat_real.png`) là **ảnh chụp thật** qua Playwright:

```bash
# Khởi động app trước: python 2_rag/app.py
python docs/capture_gradio.py
```

## Đổi style Word

Sửa `customize_reference.py` (đổi font, color, size), chạy lại:

```bash
python docs/customize_reference.py
python docs/build_docx.py
```
