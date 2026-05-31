"""
Chụp screenshot Gradio app đang chạy bằng Playwright.

Yêu cầu:
- Gradio app đã start ở http://localhost:7860
- Playwright + Chromium đã cài

Chạy:
    python docs/capture_gradio.py
Output:
    docs/screenshots/gradio_ui_real.png          (giao diện ban đầu)
    docs/screenshots/gradio_ui_chat_real.png     (sau khi chat thật)
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parent / "screenshots"
URL = "http://localhost:7860"


def main():
    OUT_DIR.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1500, "height": 950},
            device_scale_factor=2,
            locale="vi-VN",
        )
        page = context.new_page()

        print(f"Loading {URL}...")
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(10000)  # đợi Gradio render xong

        # Screenshot ban đầu
        page.screenshot(path=str(OUT_DIR / "gradio_ui_real.png"), full_page=False)
        print(f"[OK] gradio_ui_real.png (initial)")

        # ===== Gửi 1 câu hỏi =====
        try:
            # Gradio ChatInterface có textarea với placeholder "Type a message..."
            # Tìm trong main chat area (sau sidebar)
            textareas = page.locator("textarea").all()
            print(f"Found {len(textareas)} textareas")

            # Last textarea thường là input chat (sidebar có thể không có textarea)
            chat_input = textareas[-1] if textareas else None
            if not chat_input:
                raise RuntimeError("Không tìm thấy textarea chat")

            # Cuộn xuống để chat area visible
            chat_input.scroll_into_view_if_needed()
            page.wait_for_timeout(500)

            # Click + type
            chat_input.click()
            page.wait_for_timeout(300)
            chat_input.fill("Quy trình xử lý sự cố ATTT?")
            page.wait_for_timeout(500)

            # Submit Enter
            chat_input.press("Enter")
            print("Sent message, waiting for LLM response (60s)...")

            # Đợi LLM trả lời (qwen3:1.7b CPU ~15-25s, buffer to 60s)
            page.wait_for_timeout(60000)

            page.screenshot(path=str(OUT_DIR / "gradio_ui_chat_real.png"), full_page=False)
            print(f"[OK] gradio_ui_chat_real.png (after chat)")

        except Exception as e:
            print(f"[WARN] Send chat failed: {type(e).__name__}: {e}")
            # Screenshot anyway to debug
            page.screenshot(path=str(OUT_DIR / "gradio_debug.png"))

        browser.close()


if __name__ == "__main__":
    main()
