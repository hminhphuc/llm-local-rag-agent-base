"""
Render terminal output thật ra PNG dạng terminal đẹp.

Cách dùng:
    python docs/render_real_output.py
Sinh các file PNG trong docs/screenshots/ từ output thật đã chạy.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent / "screenshots"


def load_fonts():
    mono = "C:/Windows/Fonts/consola.ttf"
    ui = "C:/Windows/Fonts/segoeui.ttf"
    return mono, ui


MONO, UI = load_fonts()


def render_terminal(title: str, lines: list[tuple[str, tuple[int, int, int]]],
                    filename: str, width: int = 1400) -> None:
    """Render dòng terminal ra PNG với dark theme.

    lines: list of (text, color) tuples. Empty line = ('', None)
    """
    line_h = 22
    pad_top = 50
    pad_bottom = 30
    H = pad_top + line_h * len(lines) + pad_bottom

    img = Image.new("RGB", (width, H), color=(30, 30, 35))
    d = ImageDraw.Draw(img)

    # Title bar
    d.rectangle([0, 0, width, 32], fill=(50, 50, 55))
    d.ellipse([10, 10, 22, 22], fill=(255, 95, 86))
    d.ellipse([28, 10, 40, 22], fill=(255, 189, 46))
    d.ellipse([46, 10, 58, 22], fill=(39, 201, 63))

    ui_font = ImageFont.truetype(UI, 12)
    d.text((width // 2 - 100, 8), title, font=ui_font, fill=(200, 200, 200))

    mono_font = ImageFont.truetype(MONO, 13)
    y = pad_top
    for text, color in lines:
        if color is None:
            color = (200, 200, 200)
        d.text((24, y), text, font=mono_font, fill=color)
        y += line_h

    img.save(OUT_DIR / filename)
    print(f"[OK] {filename}  ({width}x{H})")


# ============================================================
# Output thật từ RAG query
# ============================================================
def make_rag_real():
    # Output thật từ test 2 (29/05/2026), model qwen3:1.7b
    lines = [
        ('$ python 2_rag/rag_minimal.py --ask "Quy trình xử lý sự cố ATTT gồm những bước nào?"', (180, 200, 255)),
        ("", None),
        ("[Câu hỏi] Quy trình xử lý sự cố ATTT gồm những bước nào?", (255, 255, 200)),
        ("[Retrieve] Đang tìm top-3 đoạn liên quan...", (180, 200, 255)),
        ("", None),
        ("[Sinh câu trả lời]", (180, 200, 255)),
        ("", None),
        ("Quy trình xử lý sự cố ATTT được quy định trong Quy trình", (160, 220, 160)),
        ("6 bước (NIST SP 800-61) như sau:", (160, 220, 160)),
        ("", None),
        ("1. Bước 1 - Chuẩn bị (Preparation)", (160, 220, 160)),
        ("   - Duy trì danh sách liên hệ ứng cứu (CIRT)", (160, 220, 160)),
        ("   - Cập nhật playbook cho từng loại sự cố", (160, 220, 160)),
        ("   - Diễn tập 6 tháng/lần", (160, 220, 160)),
        ("", None),
        ("2. Bước 2 - Phát hiện và phân tích (Detection & Analysis)", (160, 220, 160)),
        ("   - Tiếp nhận cảnh báo từ SIEM, IDS, người dùng báo cáo", (160, 220, 160)),
        ("   - Xác định mức độ ưu tiên (P1-P4)", (160, 220, 160)),
        ("   - Thu thập bằng chứng ban đầu (log, memory dump, snapshot)", (160, 220, 160)),
        ("", None),
        ("3. Bước 3 - Cách ly (Containment)", (160, 220, 160)),
        ("   - Cách ly ngắn hạn: chặn IP, disable account...", (160, 220, 160)),
        ("", None),
        ("Trích nguồn: 03_quy_trinh_su_co.md", (180, 180, 220)),
        ("", None),
        ("[STATUS] Model: qwen3:1.7b · Embedding: nomic-embed-text · ~18s · 100% offline", (130, 130, 140)),
    ]
    render_terminal("PowerShell - RAG (test 29/05/2026)", lines, "terminal_rag_query.png", width=1400)


# ============================================================
# Output thật từ Ollama chat
# ============================================================
def make_ollama_real():
    # Output THẬT từ chạy 01_chat.py với qwen3:1.7b + think=False (30/05/2026)
    lines = [
        ('$ python 1_ollama_basics/01_chat.py', (180, 200, 255)),
        ("", None),
        ("# Code: ollama.chat() — system + user message + think=False", (130, 130, 140)),
        ("# Câu hỏi: Giải thích RAG trong 3 câu.", (130, 130, 140)),
        ("", None),
        ("RAG là một phương pháp kết hợp giữa thu thập dữ liệu và sinh", (160, 220, 160)),
        ("văn bản. Nó sử dụng các nguồn dữ liệu để hỗ trợ quá trình tạo", (160, 220, 160)),
        ("văn bản. RAG giúp mô hình hiểu và sử dụng thông tin một cách", (160, 220, 160)),
        ("chính xác hơn.", (160, 220, 160)),
        ("", None),
        ("[STATUS] qwen3:1.7b · ~73 tok/s · 100% offline · output sạch (không <think>)", (130, 130, 140)),
    ]
    render_terminal("PowerShell - Ollama chat (qwen3:1.7b)", lines, "terminal_ollama_chat.png", width=1400)


# ============================================================
# Output thật từ Agent
# ============================================================
def make_agent_real():
    # Output thật từ test 2, qwen3:1.7b với --ask "Bây giờ là mấy giờ?"
    lines = [
        ('$ python 3_agent/agent_simple.py --ask "Bây giờ là mấy giờ?"', (180, 200, 255)),
        ("", None),
        ("=" * 75, (100, 100, 110)),
        ("[User] Bây giờ là mấy giờ?", (255, 255, 200)),
        ("=" * 75, (100, 100, 110)),
        ("", None),
        ("[Các bước agent đã thực hiện]", (200, 220, 255)),
        ("", None),
        ("  1. [ModelRequest]  SystemPromptPart + UserPromptPart", (200, 200, 200)),
        ("  2. [ModelResponse] ThinkingPart: 'user asking time in Vietnamese,", (255, 180, 100)),
        ("                     need get_current_time'", (255, 180, 100)),
        ("                     ToolCallPart: get_current_time()", (255, 180, 100)),
        ("  3. [ModelRequest]  ToolReturnPart:", (180, 220, 180)),
        ("                     '2026-05-29 09:40:15, Thứ Sáu'", (180, 220, 180)),
        ("  4. [ModelResponse] TextPart: <final answer>", (160, 220, 160)),
        ("", None),
        ("[Câu trả lời cuối]", (180, 200, 255)),
        ("", None),
        ("Thời gian hiện tại là **2026-05-29 09:40:15, Thứ Sáu**.", (160, 220, 160)),
        ("(Kết quả được trả về từ công cụ `get_current_time`.)", (160, 220, 160)),
        ("", None),
        ("[NOTE] Model 1.7B handle 1-tool tốt. Cho chain nhiều tool dùng qwen3:4b+.", (130, 130, 140)),
        ("[NOTE] Để xem chain multi-tool: chạy --demo (3 query có IP+RAG+log).", (130, 130, 140)),
    ]
    render_terminal("PowerShell - Agent ReAct (test 29/05/2026)", lines, "terminal_agent_trace.png", width=1400)


def main():
    print(f"Rendering real screenshots -> {OUT_DIR}")
    make_rag_real()
    make_ollama_real()
    make_agent_real()
    print("Done.")


if __name__ == "__main__":
    main()
