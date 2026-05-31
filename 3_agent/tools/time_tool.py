"""
Tool: get_current_time

Tool đơn giản nhất — không tham số, không IO, chỉ trả về thời gian hệ thống.

Thiết kế:
    Tool này được thiết kế đơn giản nhất để minh hoạ cơ chế "tool call"
    mà không bị phân tâm bởi logic phức tạp. Cấu trúc này giúp hiểu rõ
    các tool phức tạp hơn có IO và sandbox sẽ dễ hơn.

    Đồng thời, đây là tool minh họa "tại sao LLM cần tool":
        LLM không biết thời gian hiện tại (knowledge cutoff).
        → cần tool external để có thông tin runtime.
"""
from datetime import datetime


def get_current_time() -> str:
    """Lấy thời gian hiện tại theo giờ máy (mặc định giờ Việt Nam).

    Dùng khi user hỏi về thời gian, ngày tháng, thứ trong tuần,
    hoặc cần ngữ cảnh thời điểm để đối chiếu với chính sách
    (ví dụ "giờ này có trong giờ trực không?").

    Returns:
        Chuỗi định dạng 'YYYY-MM-DD HH:MM:SS, <thứ trong tuần>'.
        Ví dụ: '2026-05-29 14:30:45, Thứ Sáu'
    """
    now = datetime.now()

    # weekday() trả về 0=Thứ Hai ... 6=Chủ Nhật
    weekdays = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]

    return f"{now.strftime('%Y-%m-%d %H:%M:%S')}, {weekdays[now.weekday()]}"
