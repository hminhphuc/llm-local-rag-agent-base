"""
Chụp ảnh giao diện Open WebUI (giao diện chat khuyến nghị của workshop) ra PNG.

Yêu cầu:
    - Open WebUI đang chạy: `docker compose up -d` (mở http://localhost:3000)
    - Ollama đang chạy ở host, đã pull qwen3:1.7b
    - pip install playwright && playwright install chromium  (xem docs/requirements-docs.txt)

Cách dùng:
    python docs/capture_openwebui.py
    -> sinh docs/screenshots/open_webui_rag_real.png

Lưu ý: docker-compose.yml đặt WEBUI_AUTH=False nên vào thẳng giao diện chat,
không cần tạo tài khoản. Script tự đóng popup "What's New", chọn qwen3:1.7b,
gửi 1 câu hỏi tiếng Việt rồi chụp khung hội thoại.
"""
import time

from playwright.sync_api import sync_playwright

URL = "http://localhost:3000"
OUT = "docs/screenshots/open_webui_rag_real.png"
QUESTION = "Giải thích RAG (Retrieval-Augmented Generation) trong 3 câu ngắn gọn."
MODEL = "qwen3:1.7b"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 810})
        page.goto(URL, wait_until="networkidle", timeout=60000)
        time.sleep(5)

        # Đóng popup "What's New" (nếu có)
        for label in ["Okay, Let's Go!", "Okay, Let’s Go!", "Okay"]:
            try:
                page.get_by_role("button", name=label).click(timeout=3000)
                break
            except Exception:
                pass
        else:
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass
        time.sleep(2)

        # Chọn model MODEL (best-effort)
        try:
            page.get_by_text("anninh", exact=False).first.click(timeout=4000)
            time.sleep(1)
            page.get_by_text(MODEL, exact=False).first.click(timeout=4000)
            time.sleep(1)
        except Exception:
            pass

        # Gõ câu hỏi + gửi
        sent = False
        for sel in ["textarea", '[contenteditable="true"]']:
            try:
                box = page.locator(sel).last
                box.click(timeout=4000)
                if sel == "textarea":
                    box.fill(QUESTION)
                else:
                    box.type(QUESTION)
                time.sleep(0.5)
                page.keyboard.press("Enter")
                sent = True
                break
            except Exception:
                pass

        if sent:
            time.sleep(30)  # chờ CPU sinh câu trả lời

        page.screenshot(path=OUT, full_page=False)
        browser.close()
    print(f"[OK] Đã lưu {OUT}")


if __name__ == "__main__":
    main()
