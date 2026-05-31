# Module 1 — Local LLM với Ollama

> Mục tiêu: học viên tự chạy được LLM trên máy mình, hiểu vì sao Ollama là lựa chọn tốt khi cần chạy AI 100% offline (dữ liệu không rời máy).

## Nội dung module

**Khuyến nghị dùng [notebook.ipynb](notebook.ipynb)** để chạy từng bước theo lớp giảng. Các file `.py` là phiên bản standalone, chạy độc lập từ terminal.

| Demo | Notebook | File standalone | Học gì |
|---|---|---|---|
| 1.1 Chat đơn giản | Bước 1 trong [notebook.ipynb](notebook.ipynb) | [01_chat.py](01_chat.py) | Gọi LLM 5 dòng code |
| 1.2 Streaming | Bước 2 | [02_streaming.py](02_streaming.py) | Hiển thị token theo thời gian thực |
| 1.3 API tương thích OpenAI | Bước 3 | [03_openai_compat.py](03_openai_compat.py) | Code OpenAI cũ chạy ngay với Ollama |
| 1.4 So sánh model | Bước 4 | [04_compare_models.py](04_compare_models.py) | Đổi model 1 dòng, so chất lượng + tốc độ |
| 1.5 Custom model | Bước 5 | [Modelfile.anninh](Modelfile.anninh) | Đóng gói system prompt thành "model riêng" |

## Vì sao chọn Ollama (nhấn trong giảng bài)

### 1. Cài đặt tối giản
```powershell
winget install Ollama.Ollama   # xong
```
So với llama.cpp/vLLM cần compile/cấu hình CUDA thủ công.

### 2. Tự tối ưu phần cứng
Ollama tự detect GPU (NVIDIA, AMD, Apple Silicon), tự chọn số layer offload, tự fallback CPU. Học viên **không cần biết** về VRAM, quantization, batch size.

### 3. Đổi model 1 lệnh
```powershell
ollama run qwen3:4b      # đổi sang
ollama run llama3.2:3b   # rồi đổi sang
ollama run gemma3:4b     # rồi đổi nữa
```
Không cần download/setup lại từ đầu, không cần convert format.

### 4. API tương thích OpenAI
Toàn bộ code Python/Node/Go viết cho ChatGPT API → chỉ đổi `base_url` là chạy với local model. Migration zero-effort.

### 5. Offline 100%
Sau khi pull model, **tắt mạng vẫn chạy**. Đây là điểm sống còn với tài liệu mật.

### 6. Modelfile — "Dockerfile cho LLM"
Đóng gói prompt + parameters thành "model" riêng, share team được. Ví dụ: tạo `troly:latest` là Qwen3 với system prompt cố định cho trợ lý của bạn.

## Cách chạy demo

> ✅ **Trước khi chạy, kiểm tra 2 điều:**
> 1. **Ollama đang chạy?** (Windows: tìm icon Ollama ở khay hệ thống; chưa có → mở app Ollama). Nếu không, code báo `Connection refused`.
> 2. **Đã bật venv?** Đầu dòng lệnh phải có `(.venv)`. Chưa → `.\.venv\Scripts\Activate.ps1` (Windows) / `source .venv/bin/activate` (mac/Linux).
>
> Mỗi script in chữ ra màn hình, mất ~10–30 giây trên CPU (nhanh hơn nếu có GPU).

> 📓 **Notebook (`.ipynb`) là gì?** Là file mở **trong trình duyệt**, chạy từng ô code một. Cách mở: bật venv → gõ `jupyter lab` → đợi trình duyệt tự bật → bấm vào `notebook.ipynb`. Notebook và file `.py` cho **kết quả giống nhau**.

### Cách A: Notebook (khuyến nghị cho lớp học)

**Windows:**
```powershell
.\.venv\Scripts\Activate.ps1
jupyter lab 1_ollama_basics\notebook.ipynb
```
**macOS / Linux:**
```bash
source .venv/bin/activate
jupyter lab 1_ollama_basics/notebook.ipynb
```

### Cách B: Standalone scripts

**Windows:**
```powershell
.\.venv\Scripts\Activate.ps1
python 1_ollama_basics\01_chat.py
python 1_ollama_basics\02_streaming.py
python 1_ollama_basics\03_openai_compat.py
python 1_ollama_basics\04_compare_models.py

# Tạo custom model
ollama create anninh -f 1_ollama_basics\Modelfile.anninh
ollama run anninh
```

**macOS / Linux:**
```bash
source .venv/bin/activate
python 1_ollama_basics/01_chat.py
python 1_ollama_basics/02_streaming.py
python 1_ollama_basics/03_openai_compat.py
python 1_ollama_basics/04_compare_models.py

# Tạo custom model
ollama create anninh -f 1_ollama_basics/Modelfile.anninh
ollama run anninh
```

> 💡 **`Modelfile.anninh` chỉ là một ví dụ** — nó đóng gói sẵn một system prompt (ở đây là trợ lý cho một bối cảnh cụ thể). Đây chính là chỗ bạn **sửa khối `SYSTEM`** để tạo trợ lý cho **vai trò của mình** (trợ lý HR, gia sư học tập, trợ lý pháp lý…). File dùng base `qwen3:1.7b` cho khớp mặc định workshop; máy mạnh có thể đổi dòng `FROM` sang `qwen3:4b`.

## Bài tập gợi ý (15 phút thực hành)

1. Pull thêm 1 model khác (`gemma3:4b` chẳng hạn) và sửa `04_compare_models.py` thêm vào danh sách so sánh
2. Sửa `Modelfile.anninh` để bot trả lời theo phong cách "ngắn gọn, có gạch đầu dòng"
3. Tự viết file `05_my_chat.py` lưu lịch sử hội thoại vào file JSON

## Tài liệu chính thức (đọc thêm)

| Chủ đề | Nguồn |
|---|---|
| Ollama (runtime) | [ollama.com](https://ollama.com) · [github.com/ollama/ollama](https://github.com/ollama/ollama) |
| Ollama model library | [ollama.com/library](https://ollama.com/library) |
| Ollama Python SDK | [github.com/ollama/ollama-python](https://github.com/ollama/ollama-python) |
| OpenAI Python SDK | [github.com/openai/openai-python](https://github.com/openai/openai-python) |
| Modelfile reference | [github.com/ollama/ollama/blob/main/docs/modelfile.md](https://github.com/ollama/ollama/blob/main/docs/modelfile.md) |
| Qwen3 model card | [qwenlm.github.io](https://qwenlm.github.io/) · [huggingface.co/Qwen](https://huggingface.co/Qwen) |
| Llama model card | [llama.com](https://www.llama.com/) |
| GGUF format spec | [github.com/ggml-org/ggml/blob/master/docs/gguf.md](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) |

Xem chi tiết về quantization, performance tuning, so sánh runtime ở [TAI_LIEU_CHI_TIET.md — Phần 1](../TAI_LIEU_CHI_TIET.md).

## Tiếp theo
[Module 2 — RAG cho tài liệu nội bộ →](../2_rag/)
