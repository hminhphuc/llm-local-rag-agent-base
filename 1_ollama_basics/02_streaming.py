"""
Demo 1.2 — Streaming output (token bay ra theo thời gian thực).

Mục đích:
    LLM sinh token tuần tự. Mặc định ollama.chat() chờ sinh xong hết
    rồi mới trả về → user thấy "đứng hình" vài giây. Streaming cho phép
    hiển thị từng token NGAY khi LLM sinh ra → UX giống ChatGPT.

Cực kỳ quan trọng khi chạy CPU/model lớn, vì có thể mất 10-30s mới sinh xong.

Chạy:
    python 1_ollama_basics/02_streaming.py
"""
import ollama

MODEL = "qwen3:1.7b"

# Khác với 01_chat.py: thêm stream=True.
# Khi đó ollama.chat() trả về một generator, không phải 1 response object.
# Mỗi lần next() lấy ra 1 chunk chứa vài token.
stream = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Liệt kê 5 mẹo viết email chuyên nghiệp, mỗi mẹo 1 câu."},
    ],
    stream=True,
    think=False,  # Tắt thinking mode của Qwen3 để output sạch (xem 01_chat.py)
)

# Lặp qua từng chunk và in ra ngay.
# end="" để không xuống dòng giữa các chunk.
# flush=True ép Python in ngay (mặc định buffer cho đến khi đầy/xuống dòng).
for chunk in stream:
    print(chunk.message.content, end="", flush=True)

# In dòng mới cuối cùng cho gọn terminal
print()
