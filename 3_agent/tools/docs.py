"""
Tool: search_internal_docs

Tái sử dụng RAG pipeline từ Module 2. Đây là minh chứng rõ ràng cho
"RAG là 1 tool của Agent" — RAG không bị thay thế, nó trở thành 1 thành phần.
"""
import sys
from pathlib import Path

# Cho phép import rag_minimal từ 2_rag/.
# Hơi "hack" — production nên đóng gói rag thành package riêng (pip install).
# Cho lớp học giữ đơn giản: thêm path vào sys.path.
_REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "2_rag"))

from rag_minimal import retrieve  # noqa: E402


def search_internal_docs(query: str, top_k: int = 3) -> str:
    """Tìm trong kho quy chế nội bộ của đơn vị.

    Dùng khi user hỏi về quy định, chính sách, quy trình, quy chế nội bộ
    của đơn vị (mật khẩu, phân loại tài liệu, sự cố, email, thiết bị,
    dữ liệu cá nhân...).

    Args:
        query: câu hỏi hoặc từ khóa cần tìm, bằng tiếng Việt.
        top_k: số đoạn trả về (mặc định 3, không cần đổi trừ khi cần nhiều ngữ cảnh).

    Returns:
        Các đoạn tài liệu liên quan, mỗi đoạn có tên file nguồn để trích dẫn.
        Nếu chưa build index, trả về thông báo lỗi rõ ràng.
    """
    try:
        hits = retrieve(query, top_k=top_k)
    except Exception as e:
        # Báo lỗi rõ để agent biết cách xử lý: thường nó sẽ thông báo lại
        # cho user thay vì bịa câu trả lời.
        return (
            f"Lỗi truy vấn RAG: {e}. "
            f"Có thể chưa build index (chạy: python 2_rag/rag_minimal.py --build)"
        )

    if not hits:
        return "Không tìm thấy tài liệu liên quan."

    # Format kết quả dạng numbered list với nguồn — giúp LLM dễ trích dẫn lại
    result = []
    for i, h in enumerate(hits, 1):
        result.append(f"[Đoạn {i}] Nguồn: {h['source']}\n{h['text']}")
    return "\n\n".join(result)
