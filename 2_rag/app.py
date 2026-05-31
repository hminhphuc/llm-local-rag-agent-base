"""
Gradio chat UI cho RAG — đã polish cho Gradio 6.x.

Cải tiến so với bản trước:
- Theme Soft (xanh navy, nhẹ nhàng)
- Custom font Montserrat + Inter
- Layout 2 cột với Group/Accordion để gọn gàng
- Custom CSS cho polish (rounded corners, shadow, spacing)
- Streaming response thực sự
- Header có gradient + emoji
- Cấu hình trong launch() theo Gradio 6.x API

CHẠY:
    python 2_rag/app.py
    → http://localhost:7860
"""
import os
import sys
from pathlib import Path

import gradio as gr
import ollama

sys.path.insert(0, str(Path(__file__).parent))

from rag_minimal import (  # noqa: E402
    DB_DIR,
    EMBED_MODEL,
    LLM_MODEL,
    build_index,
    retrieve,
)


# ============================================================
# HÀM TIỆN ÍCH
# ============================================================
def list_available_models() -> list[str]:
    try:
        models = sorted([m.model for m in ollama.list().models])
        chat_models = [m for m in models if "embed" not in m.lower() and "bge" not in m.lower()]
        return chat_models or [LLM_MODEL]
    except Exception:
        return [LLM_MODEL]


def ensure_index() -> str:
    if not DB_DIR.exists():
        build_index()
    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(DB_DIR))
        col = client.get_collection("quy_che_an_ninh")
        return f"✅ Index sẵn sàng — {col.count()} chunks"
    except Exception as e:
        return f"⚠️ Index lỗi: {e}"


def format_sources(hits: list[dict]) -> str:
    lines = ["\n\n---\n**📎 Đoạn tham khảo:**\n"]
    for i, h in enumerate(hits, 1):
        preview = h["text"][:250].replace("\n", " ")
        if len(h["text"]) > 250:
            preview += "..."
        lines.append(f"\n**{i}. `{h['source']}`** _(distance: {h['distance']:.3f})_")
        lines.append(f"> {preview}\n")
    return "\n".join(lines)


# ============================================================
# Chat handler (có streaming)
# ============================================================
def respond(message: str, history: list, model_name: str, top_k: int, show_sources: bool):
    if not DB_DIR.exists():
        yield "⚠️ Chưa có index. Bấm **Build / Rebuild index** ở sidebar."
        return

    hits = retrieve(message, top_k=top_k)

    context_text = "\n\n".join(f"[Nguồn: {c['source']}]\n{c['text']}" for c in hits)

    prompt = f"""Bạn là trợ lý tra cứu tài liệu nội bộ. Dùng tài liệu sau để trả lời.
Chỉ dựa vào tài liệu. Nếu không đủ, nói rõ "Tài liệu không đề cập".
Trích nguồn (tên file) sau mỗi ý.

=== Tài liệu ===
{context_text}

=== Câu hỏi ===
{message}

=== Trả lời ==="""

    # Streaming + tắt thinking mode (output sạch hơn)
    try:
        stream = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2},
            stream=True,
            think=False,
        )
    except TypeError:
        # Phiên bản ollama-python cũ không có tham số think
        stream = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2},
            stream=True,
        )

    response_text = ""
    for chunk in stream:
        response_text += chunk.message.content
        yield response_text

    if show_sources:
        response_text += format_sources(hits)
        yield response_text


# ============================================================
# Theme + CSS
# ============================================================
# Theme Soft nhẹ nhàng (blue/navy).
# Có thể đổi sang Citrus, Glass, Ocean tuỳ thẩm mỹ.
theme = gr.themes.Ocean(
    primary_hue="blue",
    secondary_hue="indigo",
    neutral_hue="slate",
    radius_size="md",
    spacing_size="md",
)

# Custom CSS cho polish chuyên nghiệp
custom_css = """
/* Header gradient */
.app-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    padding: 24px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);
}
.app-header h1 {
    color: white !important;
    margin: 0 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
.app-header p {
    color: rgba(255, 255, 255, 0.9) !important;
    margin: 8px 0 0 0 !important;
    font-size: 14px !important;
}
/* Sidebar groups */
.sidebar-group {
    background: white;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 12px;
}
.sidebar-group h3 {
    margin-top: 0 !important;
    color: #1e3a8a;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
/* Status box */
.status-box {
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    padding: 10px 14px;
    border-radius: 6px;
    font-size: 13px;
    color: #15803d;
}
/* Chat container */
.chat-container {
    background: white;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    padding: 8px;
}
/* Footer note */
.footer-note {
    text-align: center;
    color: #6b7280;
    font-size: 12px;
    padding: 16px 0;
}
"""


# ============================================================
# UI Blocks
# ============================================================
with gr.Blocks(title="RAG An ninh - Trợ lý tài liệu nội bộ") as demo:
    # === Header với gradient ===
    gr.HTML(
        f"""
        <div class="app-header">
            <h1>🔒 Trợ lý tài liệu nội bộ</h1>
            <p>Hệ thống RAG chạy <b>100% local</b> · LLM: <code>{LLM_MODEL}</code> · Embedding: <code>{EMBED_MODEL}</code></p>
        </div>
        """
    )

    with gr.Row(equal_height=False):
        # ============== SIDEBAR ==============
        with gr.Column(scale=1, min_width=300):
            with gr.Group(elem_classes="sidebar-group"):
                gr.Markdown("### ⚙️ Cấu hình LLM")
                model_dropdown = gr.Dropdown(
                    choices=list_available_models(),
                    value=LLM_MODEL,
                    label="Model",
                    info="Đổi model live, không cần restart",
                )
                top_k_slider = gr.Slider(
                    minimum=1, maximum=10, value=3, step=1,
                    label="Top-k đoạn tham khảo",
                    info="Cao → context phong phú nhưng tốn token",
                )
                show_sources_check = gr.Checkbox(
                    value=True,
                    label="📎 Hiện đoạn tham khảo dưới câu trả lời",
                )

            with gr.Group(elem_classes="sidebar-group"):
                gr.Markdown("### 🗂️ Vector index")
                index_status = gr.Textbox(
                    value=ensure_index(),
                    label="Trạng thái",
                    interactive=False,
                    elem_classes="status-box",
                )
                rebuild_btn = gr.Button("🔄 Build / Rebuild index", variant="secondary", size="sm")

                def do_rebuild():
                    build_index()
                    return ensure_index()

                rebuild_btn.click(fn=do_rebuild, outputs=index_status)

            with gr.Group(elem_classes="sidebar-group"):
                gr.Markdown("### 📚 Tài liệu trong kho")
                data_dir = Path(__file__).parent / "data"
                files_md = "\n".join(f"- `{f.name}`" for f in sorted(data_dir.glob("*.md")))
                gr.Markdown(files_md or "_Chưa có file_")

        # ============== MAIN CHAT ==============
        with gr.Column(scale=3):
            with gr.Group(elem_classes="chat-container"):
                examples_list = [
                    ["Quy trình xử lý sự cố ATTT gồm những bước nào?", LLM_MODEL, 3, True],
                    ["USB cá nhân có được dùng không?", LLM_MODEL, 3, True],
                    ["Quy định mật khẩu của đơn vị?", LLM_MODEL, 3, True],
                    ["Có được forward email công vụ sang gmail?", LLM_MODEL, 3, True],
                ]

                # Gradio 6.x: ChatInterface dùng messages format mặc định, simplified API
                chat = gr.ChatInterface(
                    fn=respond,
                    additional_inputs=[model_dropdown, top_k_slider, show_sources_check],
                    examples=examples_list,
                    chatbot=gr.Chatbot(
                        height=520,
                        show_label=False,
                        resizable=True,
                        avatar_images=(None, None),
                    ),
                    textbox=gr.Textbox(
                        placeholder="💬 Hỏi về quy định nội bộ...",
                        show_label=False,
                        container=False,
                        scale=7,
                        submit_btn="Gửi",  # Gradio 6.x: submit_btn vào Textbox, không vào ChatInterface
                    ),
                    fill_height=False,
                )

    gr.HTML(
        """
        <div class="footer-note">
            🛡️ Mọi truy vấn xử lý 100% trên máy local · Không byte nào rời khỏi đơn vị
        </div>
        """
    )


# ============================================================
# Launch — Gradio 6.x: theme truyền vào launch()
# ============================================================
if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        theme=theme,        # Gradio 6.x: theme vào launch()
        css=custom_css,     # Gradio 6.x: css vào launch()
    )
