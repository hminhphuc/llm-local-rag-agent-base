"""
Tools cho agent.

Mỗi tool là 1 function Python thuần với:
    - Type annotation (LLM hiểu kiểu tham số)
    - Docstring tiếng Việt (LLM dùng để quyết định khi nào gọi)

Để thêm tool mới:
    1. Tạo file my_tool.py trong thư mục này
    2. Export function ra ngoài qua __all__ ở file đó
    3. Import vào __init__.py này
    4. Đăng ký trong agent_simple.py bằng agent.tool_plain(my_tool)

Đây là cấu trúc mở: có thể thêm tool VirusTotal, Shodan, Whois...
mà không cần sửa code agent.
"""
from .docs import search_internal_docs
from .ip_reputation import check_ip_reputation
from .log_reader import read_log_file
from .time_tool import get_current_time

__all__ = [
    "search_internal_docs",
    "check_ip_reputation",
    "read_log_file",
    "get_current_time",
]
