# Chạy AI riêng tư trên máy của bạn — Local LLM → RAG → Agent

> **Workshop này dạy bạn chạy một mô hình AI ngay trên máy mình — hoàn toàn offline, dữ liệu không rời khỏi máy.** Sau đó (tùy chọn) cho AI đọc tài liệu của riêng bạn để trả lời có dẫn nguồn (RAG), và cho AI biết dùng công cụ để làm việc nhiều bước (Agent).

**Chưa biết mấy từ này?** Đọc 20 giây là đủ để bắt đầu:

| Từ | Nghĩa đơn giản |
|---|---|
| **LLM** | "Bộ não" AI biết đọc–viết tiếng người (như ChatGPT), nhưng đây chạy **trên máy bạn** |
| **Offline / Local** | Chạy không cần Internet — tắt Wi-Fi vẫn dùng được. Dữ liệu **không gửi lên mạng** |
| **RAG** | Cho AI đọc **tài liệu của bạn** rồi hỏi đáp dựa trên đó (ít bịa, có trích nguồn) |
| **Agent** | AI biết tự dùng **công cụ** (tra giờ, đọc file, tìm tài liệu…) để làm việc nhiều bước |

Trục xuyên suốt cả buổi: **dữ liệu của bạn không rời máy.**

---

## 1. Dành cho ai? Học xong có gì?

Workshop cho **nhiều đối tượng**: dân văn phòng, sinh viên, lập trình viên, người làm nghiên cứu — bất kỳ ai muốn dùng AI mà **không gửi dữ liệu lên mạng**.

> ✅ **Ngay sau khi hoàn thành Module 1, bạn đã có một trợ lý AI riêng chạy offline trên máy — đó đã là một hệ thống hoàn chỉnh, dùng được ngay.**
> Module 2 (RAG) và Module 3 (Agent) là **phần mở rộng tùy chọn** — không bắt buộc.

| Module | Bạn làm được gì | Vai trò |
|---|---|---|
| **1 — Local LLM** | Chat với AI ngay trên máy, offline | ⭐ **Bắt buộc** (xong đây là đủ) |
| 2 — RAG | Hỏi đáp trên tài liệu của riêng bạn | Tùy chọn |
| 3 — Agent | AI biết dùng công cụ, làm việc nhiều bước | Tùy chọn (giới thiệu) |

---

## 2. Cần chuẩn bị gì?

| Thành phần | Tối thiểu | Khuyến nghị |
|---|---|---|
| Hệ điều hành | Windows 10 / macOS 12 / Ubuntu 20.04 | Bản mới nhất |
| RAM | 8GB | 16GB |
| Ổ trống | 5GB | 10GB |
| Python | 3.10+ | 3.11+ |
| Mạng | Chỉ cần để **tải model 1 lần** (~1.7GB) | Sau đó chạy offline |
| Docker Desktop | Không cần (nếu chỉ học bằng notebook/CLI) | **Cần nếu dùng giao diện Open WebUI** — [tải về](https://www.docker.com/products/docker-desktop/) |

> Học bằng **notebook/CLI**: chỉ cần Ollama + Python. Dùng **giao diện chat Open WebUI** (đẹp như ChatGPT, khuyến nghị): cài thêm **Docker Desktop** — `setup.ps1`/`setup.sh` không tự cài Docker.

<details>
<summary><b>👉 Cách kiểm tra máy bạn (Windows)</b></summary>

- **RAM bao nhiêu?** Bấm `Windows` → gõ "About your PC" → xem dòng *Installed RAM*.
- **Có Python chưa?** Mở PowerShell, gõ `python --version`. Nếu báo lỗi → cài [Python 3.11](https://www.python.org/downloads/) (nhớ tick *Add to PATH*).
- **Có card đồ họa (GPU) rời không?** `Windows` → gõ "Device Manager" → mục *Display adapters*. Có NVIDIA/AMD = chạy nhanh hơn (không bắt buộc).

**Chọn model theo RAM:** dưới 14GB RAM, hoặc không có GPU riêng → chọn **[1] qwen3:1.7b** (mặc định). Từ 16GB hoặc có GPU → có thể chọn [2]/[3] mạnh hơn.
</details>

---

## 3. Cài đặt (làm 1 lần)

### Bước 0 — Lấy code về máy

**Đã quen Git?**
```bash
git clone https://github.com/hminhphuc/llm-local-rag-agent-base.git
cd llm-local-rag-agent-base
```
**Chưa quen Git?** Vào [trang repo trên GitHub](https://github.com/hminhphuc/llm-local-rag-agent-base) → nút xanh **Code** → **Download ZIP** → giải nén → mở thư mục vừa giải nén.

---

### 🪟 Windows (PowerShell)

> ⚠️ **Mở PowerShell thế nào?** Bấm chuột phải vào nút **Start** → chọn **Windows PowerShell**. Rồi `cd` vào thư mục repo, ví dụ:
> ```powershell
> cd C:\Users\TÊN-BẠN\Downloads\llm-local-rag-agent-base
> ```

> 🛑 **Nếu gặp lỗi "running scripts is disabled" — chạy dòng này trước** (chỉ 1 lần):
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

```powershell
# 1. Cài Ollama + tạo môi trường Python (.venv) + cài thư viện
.\0_setup\setup.ps1
#    ⚠️ Nếu script báo cần khởi động lại PowerShell sau khi cài Ollama:
#    đóng cửa sổ này, mở PowerShell mới, cd lại thư mục, rồi chạy lại .\0_setup\setup.ps1

# 2. Tải model (1 lần; Enter để chọn mặc định qwen3:1.7b ~1.7GB)
.\0_setup\pull_models.ps1

# 3. Bật môi trường Python (.venv)
.\.venv\Scripts\Activate.ps1

# 4. Test nhanh — thấy AI trả lời là xong
ollama run qwen3:1.7b "Xin chào, bạn là ai?"
```

### 🍎 macOS / 🐧 Linux (Bash)

```bash
# 1. Cấp quyền + cài Ollama + tạo .venv + cài thư viện
chmod +x 0_setup/setup.sh 0_setup/pull_models.sh
./0_setup/setup.sh

# 2. Tải model (Enter = mặc định qwen3:1.7b)
./0_setup/pull_models.sh

# 3. Bật môi trường Python
source .venv/bin/activate

# 4. Test nhanh
ollama run qwen3:1.7b "Xin chào, bạn là ai?"
```

> 💡 **`.venv` là gì?** Là môi trường ảo chứa riêng các thư viện Python của workshop, không ảnh hưởng hệ thống. Phải **bật (activate)** nó trước khi chạy `python`.

---

## 4. ⚠️ Luôn bật venv trước khi chạy `python`

Đây là một lỗi rất phổ biến. **Trước mỗi lệnh `python`**, hãy chắc venv đang bật (đầu dòng lệnh có chữ `(.venv)`):

| Hệ | Lệnh bật venv |
|---|---|
| Windows | `.\.venv\Scripts\Activate.ps1` |
| macOS / Linux | `source .venv/bin/activate` |

Quên bật venv → gặp lỗi `ModuleNotFoundError`. Cứ bật lại rồi chạy tiếp.

---

## 5. Cách học & giao diện

**Học bằng notebook (khuyến nghị):** mở file `.ipynb` từng module bằng Jupyter Lab, chạy từng ô code để hiểu từng bước.
```bash
jupyter lab        # đợi trình duyệt tự mở, bấm vào notebook.ipynb của từng module
```

**Giao diện chat — Open WebUI** (giống ChatGPT, chạy 100% local): lịch sử hội thoại, đổi model, **kéo–thả tài liệu để hỏi đáp** — không cần code. Cần cài [Docker Desktop](https://www.docker.com/products/docker-desktop/) trước, và Ollama phải đang chạy:
```powershell
docker compose up -d        # khởi động Open WebUI
# Mở trình duyệt: http://localhost:3000
```

> 🚧 **Docker bị chặn (máy công ty) hoặc không muốn cài?** Bạn vẫn **học đầy đủ** chỉ với notebook/CLI — giao diện chỉ là phần tiện thêm, không bắt buộc. Nếu vẫn muốn UI đẹp mà không cần Docker: `pip install open-webui` rồi `open-webui serve` (mở http://localhost:8000) — nhưng **lần đầu cài rất nặng (~2.5GB, ~20 phút)**, cân nhắc kỹ.

> 💡 **Nâng cao (tùy chọn):** tự mở rộng repo bằng AI (Cursor/Claude Code) → đọc [VIBE_CODING.md](VIBE_CODING.md).

---

## 6. Bản đồ 3 module — chạy thử & thấy ngay kết quả

> ⚠️ **Nhớ bật venv trước mỗi lệnh `python`** (xem mục 4). Mỗi lệnh in kết quả ra màn hình, mất ~10–30 giây trên CPU (nhanh hơn nếu có GPU); riêng `--build` của Module 2 lâu hơn vì phải tạo embedding từ tài liệu. Notebook và script cho **kết quả giống nhau** — notebook chạy trong trình duyệt, script chạy trong terminal.

### ⭐ Module 1 — Local LLM (bắt buộc) · [chi tiết](1_ollama_basics/)
Chat với AI chạy ngay trên máy.
```bash
python 1_ollama_basics/01_chat.py
```

### Module 2 — RAG (tùy chọn) · [chi tiết](2_rag/)
Hỏi đáp trên tài liệu của bạn. **Yêu cầu: xây dựng index lần đầu:**
```bash
python 2_rag/rag_minimal.py --build                          # tạo index (1 lần — bắt buộc cho cả Module 3)
python 2_rag/rag_minimal.py --ask "Quy định mật khẩu thế nào?"
# Giao diện chat đẹp (giống ChatGPT)? → dùng Open WebUI: docker compose up -d → http://localhost:3000
```

### Module 3 — Agent (tùy chọn, giới thiệu) · [chi tiết](3_agent/)
AI biết tự gọi công cụ.
> 🛑 **Cần làm Module 2 trước** (`python 2_rag/rag_minimal.py --build`), nếu không tool tìm tài liệu sẽ báo lỗi.
```bash
python 3_agent/agent_simple.py                               # 3 demo (mỗi câu gọi 1 tool)
python 3_agent/agent_simple.py --ask "Bây giờ là mấy giờ?"
```
> ℹ️ Với model mặc định **qwen3:1.7b**, agent gọi tốt **1 tool/câu**. Muốn nó nối nhiều tool trong 1 câu → dùng model lớn hơn (`qwen3:4b`+). Đây là giới hạn của model nhỏ, **không phải lỗi**.

---

## 7. Tự học hay học trên lớp?

- **Tự học:** làm tuần tự **0 → 1 → 2 → 3** (đừng bỏ Module 2 vì Module 3 cần index của nó). Dùng **notebook**. Tổng ~1–2 giờ tùy tốc độ.
- **Học trên lớp:** giảng viên dẫn theo slide; bảng phân bổ thời gian ở mục **"Dành cho giảng viên"** cuối trang.

---

## 8. Gặp lỗi? Tra nhanh tại đây

| Triệu chứng | Nguyên nhân & cách xử lý |
|---|---|
| `running scripts is disabled` (Windows) | Chạy `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` rồi thử lại |
| `ModuleNotFoundError` khi chạy `python …` | **Chưa bật venv** → chạy lệnh activate ở **mục 4** phía trên |
| `Connection refused` / Ollama không phản hồi | Ollama chưa chạy → mở app Ollama (Windows: tìm icon ở khay hệ thống) |
| Module 3 báo **"Lỗi truy vấn RAG"** | Chưa build index → chạy `python 2_rag/rag_minimal.py --build` |
| `winget` không nhận diện (Windows) | Cài [App Installer](https://www.microsoft.com/store/productId/9NBLGGH4NNS1) |
| Cổng `11434` / `3000` đang bận | Đã có tiến trình khác chạy — thường không sao, dùng luôn |

Bảng lỗi đầy đủ theo từng hệ điều hành: [0_setup/README.md](0_setup/README.md). Lỗi sâu hơn: [TAI_LIEU_CHI_TIET.md — Phần 7](TAI_LIEU_CHI_TIET.md).

---

## 9. Cấu trúc repo

```
.
├── 0_setup/              # Script cài đặt (.ps1 cho Windows, .sh cho macOS/Linux)
├── 1_ollama_basics/      # ⭐ Module 1: chat, streaming, API, so sánh model
├── 2_rag/                # Module 2: RAG (pipeline + CLI)
│   └── data/             #   ↳ dataset MẪU (6 file quy chế — thay bằng tài liệu của bạn)
├── 3_agent/              # Module 3: agent + 4 tool (có sandbox)
│   └── sample_logs/      #   ↳ log MẪU để demo
├── docs/                 # Tài liệu Word + sơ đồ (xem mục dưới)
├── slides/               # Slide bài giảng (cho giảng viên)
├── docker-compose.yml    # Open WebUI — giao diện chat khuyến nghị
├── requirements.txt      # Thư viện Python cho học viên
└── VIBE_CODING.md        # Hướng dẫn tự mở rộng repo bằng AI
```

> 📌 Thư mục `data/` và `sample_logs/` chỉ là **dữ liệu mẫu** để demo. Đây là chỗ bạn thay bằng tài liệu của riêng mình (hợp đồng, tài liệu HR, ghi chú nghiên cứu, mã nguồn…).

---

## 10. Tài liệu kèm theo

### 📘 Cho học viên (tự học & tra cứu)
| File | Dùng để |
|---|---|
| [TAI_LIEU_CHI_TIET.md](TAI_LIEU_CHI_TIET.md) · [bản Word](docs/TAI_LIEU_CHI_TIET.docx) | Handbook chi tiết: định nghĩa, sơ đồ, bảng tra lỗi — đọc trong giờ thực hành & sau buổi |
| [VIBE_CODING.md](VIBE_CODING.md) | Tự mở rộng repo bằng AI assistant |

### 🎓 Dành cho giảng viên (học viên bỏ qua)
| File | Dùng để |
|---|---|
| **[INSTRUCTOR_CHECKLIST.md](INSTRUCTOR_CHECKLIST.md)** | ✅ Checklist 1 trang: chuẩn bị trước buổi + câu hỏi an toàn + fallback — **đọc trước tiên** |
| [KICH_BAN_GIANG.md](KICH_BAN_GIANG.md) | Kịch bản nói chi tiết 2 giờ, có timing |
| [slides/SLIDES.pptx](slides/SLIDES.pptx) | Slide 23 trang (kèm PDF/HTML) |
| [BAO_CAO_TEST.md](BAO_CAO_TEST.md) | Báo cáo test end-to-end + các lỗi đã fix |

---

## 🎓 Dành cho giảng viên (học viên bỏ qua mục này)

Workshop ~2h, 3 module độc lập có thể dạy rời. Trọng số khi giảng trên lớp:

| Module | Vai trò | Thời lượng trên lớp |
|---|---|---|
| 1 — Local LLM | ⭐ **Trục chính (46%)** | 22' giảng + 22' thực hành |
| 2 — RAG | Thứ yếu (35%) | 15' giảng + 19' thực hành |
| 3 — Agent | Phụ — chỉ demo (19%) | 14' demo (không thực hành tại lớp) |
| Tổng kết & Q&A | — | 12' |

> Lưu ý: bảng trên áp dụng cho **lịch dạy trên lớp**. Người **tự học** vẫn làm đầy đủ cả 3 module.

Triết lý: **giảng tập trung trực giác + demo cốt lõi**; chi tiết (embedding lý thuyết, chunking, bảo mật chuyên sâu, MCP, production…) đẩy sang [TAI_LIEU_CHI_TIET.md](TAI_LIEU_CHI_TIET.md). Hướng dẫn dùng bộ tài liệu: xem [KICH_BAN_GIANG.md](KICH_BAN_GIANG.md).

---

## Vì sao chọn stack này?

| Thành phần | Công cụ | Vì sao |
|---|---|---|
| Chạy LLM | **Ollama** | Cài 1 lệnh, tự tối ưu GPU/CPU, đổi model 1 dòng, API giống OpenAI |
| Model | **Qwen3:1.7b** (mặc định) | Output sạch, nhanh, hỗ trợ tool calling, nhẹ (~1.4GB; ~1.7GB cả embedding) |
| Embedding | **nomic-embed-text** | 274MB, đa ngôn ngữ, chạy qua Ollama |
| Vector DB | **ChromaDB** | Gọn trong 1 file, không cần server riêng |
| Agent | **Pydantic AI** | Python thuần, type-safe, dễ đọc |
| Giao diện | **Open WebUI** | Giống ChatGPT, đầy đủ tính năng, chạy bằng Docker — không cần code |

---

## Tham khảo chính thức

| Công nghệ | Trang chính thức | Tổ chức |
|---|---|---|
| **Ollama** | [ollama.com](https://ollama.com) | Ollama Inc. |
| **Qwen3** | [qwenlm.github.io](https://qwenlm.github.io/) | Alibaba Cloud |
| **ChromaDB** | [trychroma.com](https://www.trychroma.com) | Chroma |
| **Pydantic AI** | [ai.pydantic.dev](https://ai.pydantic.dev) | Pydantic |
| **Open WebUI** | [openwebui.com](https://openwebui.com) | OSS community |

Paper nền tảng: **RAG** — [Lewis et al. 2020](https://arxiv.org/abs/2005.11401) · **ReAct** — [Yao et al. 2022](https://arxiv.org/abs/2210.03629). Danh sách đầy đủ: [TAI_LIEU_CHI_TIET.md — Phần 8](TAI_LIEU_CHI_TIET.md).

---

## License
[MIT](LICENSE) — dùng cho mục đích giáo dục.
