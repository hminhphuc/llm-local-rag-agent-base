"""
Demo 1.1 — Chat đơn giản với Ollama.

Mục đích:
    Cho học viên thấy "chỉ 5 dòng code là gọi được LLM local". So với việc
    tự load transformers, quản VRAM, handle batching... đây là sức mạnh
    của Ollama: ẩn hết phần khó, expose API đơn giản.

Chạy:
    python 1_ollama_basics/01_chat.py
"""
import ollama

# ===== Chọn model =====
# Đổi thành tên model bạn đã pull (kiểm tra bằng `ollama list`).
# Các lựa chọn phổ biến:
#   - "qwen3:1.7b"    → mặc định workshop (nhẹ, output sạch, ~73 tok/s CPU)
#   - "qwen3:4b"      → chất lượng cao hơn, cần RAM 16GB+
#   - "llama3.2:3b"   → nhanh, tiếng Anh tốt
#   - "troly"         → model custom đã tạo từ Modelfile
MODEL = "qwen3:1.7b"

# ===== Gọi LLM =====
# ollama.chat() nhận list "messages" giống định dạng của OpenAI.
# Mỗi message có 2 trường:
#   - role:    "system" (hướng dẫn cho LLM), "user" (câu hỏi), "assistant" (câu trả lời cũ)
#   - content: nội dung text
#
# Lợi ích của format này: dễ chuyển sang nhiều turn (giữ lịch sử hội thoại)
# bằng cách append message mới vào list.
response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": "Bạn là trợ lý hữu ích, trả lời ngắn gọn, rõ ràng."},
        {"role": "user", "content": "Giải thích RAG (Retrieval-Augmented Generation) trong 3 câu."},
    ],
    # think=False: tắt thinking mode của Qwen3 (mặc định bật, in ra <think>...</think>
    # block dài). Cho ứng dụng đơn giản, tắt đi để output sạch.
    # Nếu model không hỗ trợ tham số này (model khác Qwen3), Ollama bỏ qua không lỗi.
    think=False,
)

# response.message.content là chuỗi text LLM trả về.
# response còn các field hữu ích khác:
#   - response.eval_count    : số token sinh ra
#   - response.eval_duration : thời gian (nanoseconds) → tính tốc độ tok/s
#   - response.total_duration: tổng thời gian gồm cả load model
print(response.message.content)
