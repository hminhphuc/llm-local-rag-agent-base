"""
Demo 1.4 — So sánh nhiều model trên cùng 1 prompt.

Mục đích:
    Minh họa "đổi model = đổi 1 string" trong Ollama. Không cần
    download lại framework, không cần restart, không cần convert format.
    Tradeoff size vs chất lượng vs tốc độ là quyết định runtime.

    Đây là điểm quan trọng khi vận hành: khi có yêu cầu thay đổi
    (model mới hơn, yêu cầu cập nhật), chỉ cần ollama pull X
    và đổi tên là xong.

Chạy:
    python 1_ollama_basics/04_compare_models.py
"""
import time
import ollama

# ===== Cấu hình demo =====
# Cùng 1 prompt cho tất cả model để so sánh công bằng
PROMPT = "Giải thích ngắn gọn cho người mới: máy học (machine learning) là gì?"

# Danh sách model muốn so. Thêm/bớt tùy ý để so sánh — đây chính là cú đổi "1 dòng".
# Uncomment dòng dưới sau khi
# ollama pull gemma3:4b.
MODELS = [
    "qwen3:1.7b",   # nhẹ nhất, nhanh nhất
    "qwen3:4b",     # chất lượng cao hơn (cần RAM 16GB+)
    "llama3.2:3b",  # Meta, tiếng Anh xuất sắc, tiếng Việt khá
    # "gemma3:4b",  # Google, uncomment sau khi pull
]


def list_local_models() -> set[str]:
    """Lấy danh sách model đã pull về máy.

    Dùng để skip model chưa pull, tránh script bị crash.
    """
    return {m.model for m in ollama.list().models}


def benchmark(model: str) -> None:
    """Chạy benchmark cho 1 model và in stats.

    Đo 2 chỉ số quan trọng:
    - Latency (giây): tổng thời gian từ lúc gửi đến lúc xong
    - Throughput (tok/s): số token sinh ra / thời gian → đo tốc độ inference
    """
    print(f"\n{'=' * 60}")
    print(f"Model: {model}")
    print("=" * 60)

    # Đo thời gian từ trước khi gọi API
    start = time.time()
    # think=False: tắt thinking mode của Qwen3 để benchmark "đẹp" (đếm token sinh
    # ra thực sự là output, không phải block <think>). Model khác bỏ qua tham số này.
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": PROMPT}],
            options={"num_predict": 200},
            think=False,
        )
    except TypeError:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": PROMPT}],
            options={"num_predict": 200},
        )
    elapsed = time.time() - start

    # Tính tốc độ token/giây — chỉ số quan trọng nhất khi đánh giá inference speed.
    # eval_count = số token model đã sinh ra (không tính prompt).
    content = response.message.content
    eval_count = response.eval_count or 0
    tok_per_sec = eval_count / elapsed if elapsed > 0 else 0

    print(content)
    print(f"\n[Thống kê] {eval_count} tokens trong {elapsed:.1f}s = {tok_per_sec:.1f} tok/s")


def main() -> None:
    # Kiểm tra trước những model nào đã pull, để skip cái chưa có
    local = list_local_models()
    print(f"Prompt: {PROMPT}\n")
    print(f"Model đã pull trong máy: {sorted(local)}")

    for model in MODELS:
        # Ollama đôi khi thêm ":latest" vào tên, check cả 2 dạng
        if model not in local and f"{model}:latest" not in local:
            print(f"\n[SKIP] {model} chưa pull. Chạy lệnh: ollama pull {model}")
            continue
        benchmark(model)

    print("\n--- Quan sát ---")
    print("- Model nhỏ (1.7b-3b): nhanh, đủ cho RAG đơn giản, hơi yếu khi suy luận nhiều bước")
    print("- Model trung (4b-8b): cân bằng, phù hợp đa số use case")
    print("- Model lớn (>14b): chất lượng tốt nhất, cần GPU để chạy mượt")


if __name__ == "__main__":
    main()
