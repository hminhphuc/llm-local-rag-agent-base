"""
Agent đơn giản dùng Pydantic AI + Ollama.

CÔNG THỨC:
    Agent = LLM + Tools + ReAct loop

Agent khác RAG ở chỗ:
    - RAG: LLM chỉ làm 1 việc — đọc tài liệu rồi trả lời.
    - Agent: LLM TỰ QUYẾT gọi tool nào, theo thứ tự nào, dừng khi nào.

ReAct loop (Reason + Act):
    1. Thought:     "Tôi cần làm gì để trả lời?"
    2. Action:      gọi tool X với tham số Y
    3. Observation: kết quả từ tool
    4. Lặp lại từ bước 1 đến khi đủ thông tin
    5. Final Answer

Pydantic AI ẨN vòng lặp này — ta chỉ khai báo tool, framework lo phần còn lại.

VÌ SAO PYDANTIC AI:
    - Python thuần, decorator đơn giản (giống FastAPI)
    - Type-safe qua Pydantic
    - Hỗ trợ mọi provider OpenAI-compatible → dùng được với Ollama
    - Code rõ ràng, ít "ma thuật" hơn LangGraph

CÁCH DÙNG:
    python 3_agent/agent_simple.py                          # demo mặc định
    python 3_agent/agent_simple.py --ask "câu hỏi"          # hỏi 1 câu
    python 3_agent/agent_simple.py --interactive            # chat liên tục

YÊU CẦU TRƯỚC:
    Đã build index Module 2 (search_internal_docs cần đó):
    python 2_rag/rag_minimal.py --build
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Cho phép import package tools/ (cùng thư mục với file này)
sys.path.insert(0, str(Path(__file__).parent))

# Nạp .env (do pull_models tự ghi) để dùng đúng model bạn đã chọn lúc pull.
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

from pydantic_ai import Agent

# Pydantic AI 1.x đổi tên: OpenAIModel -> OpenAIChatModel (cho Chat Completions API).
# Cover cả 2 trường hợp để code tương thích cả version cũ và mới.
try:
    from pydantic_ai.models.openai import OpenAIChatModel as OpenAIModel
except ImportError:
    from pydantic_ai.models.openai import OpenAIModel

from pydantic_ai.providers.openai import OpenAIProvider

from tools import (
    check_ip_reputation,
    get_current_time,
    read_log_file,
    search_internal_docs,
)


# ============================================================
# CẤU HÌNH MODEL
# ============================================================
# Đọc từ env, có default. Đổi 1 dòng là chạy model khác.
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:1.7b")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

# Pydantic AI thông qua provider OpenAI-compatible để gọi Ollama.
# Đây chính là điểm tỏa sáng của Ollama: framework vốn viết cho OpenAI
# cloud → chỉ đổi base_url là dùng với local model.
model = OpenAIModel(
    LLM_MODEL,
    provider=OpenAIProvider(
        base_url=OLLAMA_URL,
        api_key="ollama",  # placeholder, Ollama không kiểm tra
    ),
)


# ============================================================
# KHỞI TẠO AGENT
# ============================================================
# System prompt là phần quan trọng nhất — quyết định agent biết
# DÙNG tool nào KHI NÀO. Viết rõ ràng giúp agent ít bị "lười" hay sai.
agent = Agent(
    model,
    system_prompt=(
        "Bạn là trợ lý hữu ích. Khi user hỏi, hãy chủ động dùng các tool có sẵn "
        "để thu thập thông tin trước khi trả lời. Quy tắc:\n"
        "- Khi cần tra cứu tài liệu/quy định nội bộ: dùng search_internal_docs.\n"
        "- Khi user nhắc đến địa chỉ IP: dùng check_ip_reputation.\n"
        "- Khi cần đọc một file: dùng read_log_file (chỉ truyền tên file, không path).\n"
        "- Khi user hỏi thời gian, ngày tháng: dùng get_current_time.\n"
        "- Có thể gọi nhiều tool tuần tự để có đầy đủ context.\n"
        "- Sau khi có đủ thông tin, trả lời bằng tiếng Việt, ngắn gọn, trích nguồn."
    ),
    # retries: nếu tool call lỗi (sai format, exception...), agent sẽ thử lại
    # tối đa N lần. Đặt thấp để tránh vòng lặp vô hạn khi model nhỏ "ngoan cố".
    retries=2,
)


# ============================================================
# ĐĂNG KÝ TOOLS
# ============================================================
# tool_plain: function thuần (không cần RunContext).
# Pydantic AI tự đọc:
#   - Tên function    → tên tool
#   - Type annotation → JSON schema cho tham số
#   - Docstring       → mô tả tool cho LLM
# Vì vậy docstring trong tools/*.py rất quan trọng — LLM dùng đó để
# quyết định tool nào phù hợp với câu hỏi.
agent.tool_plain(search_internal_docs)
agent.tool_plain(check_ip_reputation)
agent.tool_plain(read_log_file)
agent.tool_plain(get_current_time)


# ============================================================
# CHẠY 1 QUERY
# ============================================================
def run_query(question: str, verbose: bool = True) -> str:
    """Chạy 1 query qua agent.

    Args:
        question: câu hỏi của user
        verbose: True thì in các bước ReAct loop (mỗi tool call, mỗi observation)
                 để học viên thấy "agent đang nghĩ gì"

    Returns:
        Câu trả lời cuối cùng (string)
    """
    if verbose:
        print(f"\n{'=' * 70}")
        print(f"[User] {question}")
        print("=" * 70)

    # run_sync: chạy synchronous (chặn cho đến khi agent xong).
    # Pydantic AI cũng có run() async cho production.
    result = agent.run_sync(question)

    if verbose:
        # In các message trong vòng ReAct loop — học viên thấy được
        # quá trình "LLM gọi tool → nhận kết quả → quyết định bước tiếp".
        # Đây chính là điểm quan trọng nhất khi giảng về agent.
        print("\n[Các bước agent đã thực hiện]")
        for i, msg in enumerate(result.all_messages(), 1):
            kind = type(msg).__name__
            preview = str(msg)[:200].replace("\n", " ")
            print(f"  {i}. [{kind}] {preview}...")
        print("\n[Câu trả lời cuối]")
        print(result.output)
        print()

    return result.output


# ============================================================
# CÁC CHẾ ĐỘ CHẠY
# ============================================================
def demo() -> None:
    """3 ví dụ SINGLE-TOOL để học viên thấy agent tự gọi đúng tool.

    LƯU Ý (đã verify 29/05/2026): qwen3:1.7b — model mặc định workshop —
    gọi TỐT 1 tool mỗi câu, nhưng KHÔNG chain multi-tool ổn định.
    Vì vậy demo mặc định dùng câu single-tool (chắc chắn chạy đẹp).
    Muốn xem multi-tool chain → đặt LLM_MODEL=qwen3:4b (hoặc 8b) rồi
    chạy `--ask` với câu ghép, ví dụ trong docstring run_query.
    """
    questions = [
        "Bây giờ là mấy giờ?",                                    # → get_current_time
        "Kiểm tra IP 203.0.113.42 có an toàn không?",            # → check_ip_reputation
        "Tìm trong tài liệu nội bộ: quy trình xử lý sự cố.",     # → search_internal_docs
    ]
    for q in questions:
        run_query(q)


# Câu multi-tool để thử với model lớn hơn (qwen3:4b+). KHÔNG dùng cho demo
# mặc định vì 1.7b không chain ổn định. Gọi: agent_simple.py --ask "<câu này>"
MULTI_TOOL_EXAMPLES = [
    "Kiểm tra IP 203.0.113.42 và cho biết theo tài liệu cần làm gì nếu IP đó độc hại.",
    "Bây giờ là mấy giờ, và quy trình trực ứng cứu trong tài liệu thế nào?",
]


def interactive() -> None:
    """Chế độ chat liên tục — học viên tự thử câu hỏi của mình."""
    print(f"=== Agent interactive (model={LLM_MODEL}) ===")
    print("Có sẵn 4 tool: search_internal_docs, check_ip_reputation, read_log_file, get_current_time")
    print("Gõ 'exit' để thoát.\n")
    while True:
        try:
            q = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q:
            continue
        if q.lower() in {"exit", "quit", "thoat"}:
            break
        run_query(q, verbose=False)  # không in step để chat sạch sẽ
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent demo cho workshop")
    parser.add_argument("--ask", type=str, help="Hỏi 1 câu rồi thoát")
    parser.add_argument("--interactive", action="store_true", help="Chế độ chat liên tục")
    parser.add_argument("--demo", action="store_true", help="Chạy 3 ví dụ single-tool (mặc định)")
    args = parser.parse_args()

    if args.ask:
        run_query(args.ask)
    elif args.interactive:
        interactive()
    else:
        # Không có flag → chạy demo để học viên thấy ngay tác dụng
        demo()


if __name__ == "__main__":
    main()
