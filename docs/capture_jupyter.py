"""Chụp ảnh THẬT Jupyter Lab (notebook mở trong trình duyệt) cho slide 'Làm gì & ở đâu'.

Khởi động Jupyter Lab headless rồi dùng Playwright mở từng notebook và chụp.
    python docs/capture_jupyter.py
Sinh: docs/screenshots/jupyter_m1.png, jupyter_m2.png
"""
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "screenshots"
TOKEN = "workshopcap"
PORT = 8889

NOTEBOOKS = [
    ("1_ollama_basics/notebook.ipynb", "jupyter_m1.png"),
    ("2_rag/notebook.ipynb", "jupyter_m2.png"),
]


def port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def main() -> None:
    jlab = Path(sys.executable).parent / "jupyter-lab.exe"
    proc = subprocess.Popen(
        [
            str(jlab),
            f"--port={PORT}",
            "--no-browser",
            f"--IdentityProvider.token={TOKEN}",
            "--ServerApp.disable_check_xsrf=True",
            "--ServerApp.open_browser=False",
        ],
        cwd=str(ROOT),
    )
    try:
        for _ in range(120):
            if port_open(PORT):
                break
            time.sleep(0.5)
        else:
            print("[ERR] Jupyter không lên cổng", PORT)
            return
        time.sleep(5)  # cho server sẵn sàng hẳn

        base = f"http://localhost:{PORT}"
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(
                viewport={"width": 1440, "height": 860}, device_scale_factor=2
            )
            for nb, out in NOTEBOOKS:
                page.goto(f"{base}/lab/tree/{nb}?token={TOKEN}", wait_until="domcontentloaded")
                try:
                    page.wait_for_selector(".jp-Notebook .jp-Cell", timeout=60000)
                except Exception:
                    print(f"[WARN] {nb}: cell selector timeout, chup anyway")
                page.wait_for_timeout(4500)       # render settle
                page.keyboard.press("Escape")     # bỏ dialog kernel nếu có
                page.wait_for_timeout(1200)
                page.screenshot(path=str(OUT / out))
                print(f"[OK] {out}")
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
