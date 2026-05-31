"""
Demo 1.3 — Dùng OpenAI SDK với Ollama local (API tương thích).

Mục đích:
    Đây là ĐIỂM BÁN HÀNG LỚN NHẤT của Ollama. Toàn bộ code Python/Node/Go
    viết cho ChatGPT API chỉ cần đổi:
        base_url: "https://api.openai.com/v1"  →  "http://localhost:11434/v1"
    là chạy với local model. Không cần viết lại logic, không cần wrapper.

    Hệ quả: mọi framework hỗ trợ OpenAI (LangChain, LlamaIndex, Pydantic AI,
    Vercel AI SDK, Continue extension...) đều dùng được với Ollama.

Chạy:
    python 1_ollama_basics/03_openai_compat.py
"""
from openai import OpenAI

# ===== Trỏ OpenAI SDK về Ollama =====
# Đây là phần "magic": cùng 1 SDK của OpenAI, chỉ đổi 2 tham số.
client = OpenAI(
    # base_url: endpoint OpenAI-compatible của Ollama. Cổng mặc định 11434.
    base_url="http://localhost:11434/v1",

    # api_key: Ollama KHÔNG kiểm tra key, nhưng SDK của OpenAI bắt buộc có
    # field này. Cho 1 chuỗi bất kỳ là được.
    api_key="ollama",
)

# ===== Gọi như bình thường =====
# Mọi tham số (temperature, top_p, max_tokens, tools, response_format...)
# đều dùng được vì Ollama implement đúng spec OpenAI.
response = client.chat.completions.create(
    model="qwen3:1.7b",   # Đổi sang "gpt-4o-mini" + base_url OpenAI → chạy với OpenAI thật
    messages=[
        {"role": "system", "content": "Bạn là trợ lý hữu ích, trả lời ngắn gọn."},
        {"role": "user", "content": "Tóm tắt đoạn sau trong 1 câu: 'Cuộc họp tuần này "
                                     "chốt 3 việc: hoàn thiện báo cáo quý, lên kế hoạch "
                                     "tuyển dụng, và rà soát ngân sách marketing.'"},
    ],
    temperature=0.3,  # Thấp để câu trả lời nhất quán, ít sáng tạo
)

print(response.choices[0].message.content)
print("\n--- Bài học ---")
print("Nếu đổi:")
print("  base_url='https://api.openai.com/v1'")
print("  api_key=<OpenAI key thật>")
print("  model='gpt-4o-mini'")
print("code này chạy y hệt với OpenAI cloud.")
print("→ Migration giữa local và cloud chỉ cần config, không sửa logic.")
