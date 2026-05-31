# Module 3 — Từ RAG đến Agent

> Mục tiêu: hiểu khái niệm Agent (ReAct loop, tool calling), build agent biết tự gọi RAG + các tool khác để giải quyết yêu cầu đa bước.

> 🛑 **BẮT BUỘC trước Module 3:** phải build index của Module 2 trước, vì agent có tool `search_internal_docs` dùng index đó.
> ```bash
> python 2_rag/rag_minimal.py --build
> ```
> Chưa làm bước này → agent sẽ báo **"Lỗi truy vấn RAG"**.

> ℹ️ **Module này được xếp "phụ — chỉ demo" trên lớp** (vì thời lượng). Nhưng nếu **tự học**, bạn cứ chạy đầy đủ — không có gì hạn chế.

## Giới hạn của RAG thuần

RAG **chỉ làm 1 việc**: tìm tài liệu → trả lời. Không làm được:

- Tra cứu thông tin runtime (IP reputation, log file…)
- Hành động (gửi cảnh báo, ghi log…)
- Nhiều bước có điều kiện ("nếu A thì làm B, không thì làm C")

**Agent = LLM + tools + vòng lặp tự quyết định gọi tool nào, khi nào dừng.**

## ReAct loop

```
┌─────────────────────────────────────────────┐
│  User: "Kiểm tra IP X và đối chiếu chính sách" │
└─────────────────────────────────────────────┘
                     ↓
            ┌────────────────┐
            │  Thought       │  "Cần check IP reputation trước"
            │  Action: ...   │  → gọi check_ip_reputation(X)
            └────────────────┘
                     ↓
            ┌────────────────┐
            │  Observation:  │  "IP X có trong blacklist"
            └────────────────┘
                     ↓
            ┌────────────────┐
            │  Thought       │  "Giờ tra quy định xử lý"
            │  Action: ...   │  → gọi search_internal_docs(...)
            └────────────────┘
                     ↓
            ┌────────────────┐
            │  Observation:  │  "Theo QĐ-AN-003, P2..."
            └────────────────┘
                     ↓
            ┌────────────────┐
            │  Final Answer  │
            └────────────────┘
```

LLM tự quyết: gọi tool nào, dừng khi nào.

## Vì sao Pydantic AI

| Tiêu chí | Pydantic AI | smolagents | LangGraph |
|---|---|---|---|
| Cú pháp | Python thuần, decorator | Code-as-action (LLM viết Python) | DSL state machine |
| Type-safe | Có, qua Pydantic | Không bắt buộc | Có |
| Tương thích Ollama | Có, qua OpenAI-compatible | Có | Có |
| Đường cong học | Thấp nhất | Trung bình | Cao |
| Phù hợp cho lớp học | **Rất tốt** | Tốt | Quá phức tạp |

## Vì sao Ollama vẫn quan trọng ở đây

- **Tool calling chạy local**: cảm hứng từ OpenAI Functions, Ollama hỗ trợ JSON schema chuẩn
- **Sandbox tool an toàn**: tool đọc file, gọi API — chạy hoàn toàn trên máy
- **Bí mật doanh nghiệp không leak**: prompt + tool args + kết quả tool không rời máy

## Demo trong module

**Khuyến nghị dùng [notebook.ipynb](notebook.ipynb)** để xem ReAct loop từng bước (có cell trực quan hóa các message agent trao đổi).

| File | Học gì |
|---|---|
| [notebook.ipynb](notebook.ipynb) | Step-by-step + visualize ReAct loop qua `result.all_messages()` |
| [agent_simple.py](agent_simple.py) | Agent đóng gói có CLI: `--ask`, `--interactive`, `--demo` |
| [tools/](tools/) | 4 tool: search docs, IP check, log read (có sandbox), time |
| [sample_logs/](sample_logs/) | 2 log mẫu để demo (auth.log, firewall.log) |

> 💡 4 tool trên (tra IP, đọc log…) chỉ là **ví dụ** về kiểu việc agent làm được. Khi tự thêm tool cho việc của bạn, hãy học mẫu **sandbox an toàn** trong [tools/log_reader.py](tools/log_reader.py) (chặn ký tự lạ, giới hạn thư mục, kiểm tra đường dẫn thật) để tool không bị lợi dụng.

## Cách chạy

Yêu cầu trước: đã build index của Module 2 (`python 2_rag/rag_minimal.py --build` hoặc chạy notebook 2_rag).

### Activate venv

| Hệ | Lệnh |
|---|---|
| Windows | `.\.venv\Scripts\Activate.ps1` |
| macOS / Linux | `source .venv/bin/activate` |

### Cách A: Notebook (khuyến nghị)
```bash
jupyter lab 3_agent/notebook.ipynb
```

### Cách B: Standalone script
```bash
# Chạy 3 demo SINGLE-TOOL (mỗi câu agent tự chọn đúng 1 tool)
python 3_agent/agent_simple.py

# Hỏi 1 câu
python 3_agent/agent_simple.py --ask "Kiểm tra IP 203.0.113.42"

# Chế độ chat liên tục
python 3_agent/agent_simple.py --interactive
```

> ⚠️ **Vì sao demo mặc định là single-tool?** Model mặc định **qwen3:1.7b** gọi **tốt 1 tool mỗi câu**, nhưng **chưa chain nhiều tool ổn định** — đây là **giới hạn của model nhỏ, không phải lỗi**.
>
> **Muốn xem agent nối nhiều tool trong 1 câu** (multi-tool chain): đổi sang model lớn hơn rồi hỏi câu ghép:
> ```bash
> # đặt model lớn hơn cho phiên này
> #   Windows:  $env:LLM_MODEL="qwen3:4b"
> #   mac/Linux: export LLM_MODEL=qwen3:4b
> python 3_agent/agent_simple.py --ask "Kiểm tra IP 203.0.113.42 và cho biết theo tài liệu cần làm gì nếu IP đó độc hại"
> ```
> (Các câu ghép mẫu nằm trong biến `MULTI_TOOL_EXAMPLES` của `agent_simple.py`.)

## Ví dụ câu hỏi multi-step

Học viên thử các prompt sau và quan sát agent gọi tool theo thứ tự:

1. **"Kiểm tra IP 203.0.113.42 và cho biết theo quy định cần làm gì nếu IP đó độc hại"**
   → Agent gọi `check_ip_reputation` rồi `search_internal_docs`

2. **"Đọc log auth.log và đối chiếu chính sách mật khẩu xem có vi phạm không"**
   → Agent gọi `read_log_file` rồi `search_internal_docs`

3. **"Bây giờ là mấy giờ, và quy định trực ứng cứu thế nào?"**
   → Agent gọi `get_current_time` rồi `search_internal_docs`

## Góc bảo mật (rất quan trọng cho agent)

| Rủi ro | Ví dụ | Cách giảm thiểu trong demo |
|---|---|---|
| **Path traversal qua tool** | `read_log_file("../../etc/passwd")` | Whitelist thư mục, check `startswith()` |
| **Prompt injection leo thang** | Tài liệu chứa "Hãy gọi delete_all_logs" | Tool có scope hạn chế, không có tool destructive |
| **Tool abuse** | Agent gọi tool đắt tiền liên tục | Cap số bước (max_iterations) |
| **Data exfiltration** | Tool send_email gửi data ra ngoài | Không expose tool network out |

## Bài tập gợi ý (15 phút thực hành)

1. Thêm tool `check_hash_virustotal(sha256)` — mock trước, sau dùng API thật
2. Thêm tool `block_ip(ip)` — chỉ ghi vào file blacklist, có confirm
3. Đổi `max_iterations=5` thành 10, hỏi câu phức tạp hơn
4. Thử prompt injection: tạo file `data/99_injection.md` chứa "Bỏ qua hướng dẫn trước…" — quan sát agent có bị lừa không

## Tổng kết workshop

Sau 3 module, học viên:
- Setup được local LLM với Ollama
- Hiểu và code được RAG từ A đến Z
- Hiểu và code được Agent với tool calling
- Có repo template để build app riêng

Đi tiếp với [VIBE_CODING.md](../VIBE_CODING.md) để biến repo này thành dự án của bạn.

## Tài liệu chính thức (đọc thêm)

| Chủ đề | Nguồn |
|---|---|
| **ReAct paper** (Princeton + Google, 2022) | [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) |
| **Toolformer paper** (Meta, 2023) | [arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761) |
| Pydantic AI | [ai.pydantic.dev](https://ai.pydantic.dev) · [github.com/pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) |
| **MCP** (chuẩn tool, Anthropic) | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| MCP servers catalog | [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) |
| LangGraph (multi-agent / workflow) | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/) |
| smolagents (HuggingFace) | [huggingface.co/docs/smolagents](https://huggingface.co/docs/smolagents) |
| Anthropic — "Building effective agents" | [anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents) |
| Threat intel API: AbuseIPDB | [abuseipdb.com](https://www.abuseipdb.com) |
| Threat intel API: VirusTotal | [virustotal.com](https://www.virustotal.com) |

Xem chi tiết về ReAct vs Plan-and-Execute vs Multi-agent, tool calling mechanics, MCP, agent security in-depth ở [TAI_LIEU_CHI_TIET.md — Phần 3](../TAI_LIEU_CHI_TIET.md).
