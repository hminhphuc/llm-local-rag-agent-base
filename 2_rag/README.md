# Module 2 — RAG cho tài liệu của bạn

> **RAG là gì (1 câu):** đưa **tài liệu của BẠN** vào, rồi hỏi AI — AI trả lời **dựa trên tài liệu đó**, có trích nguồn, nên ít bịa hơn.
>
> Mục tiêu module: dựng pipeline RAG hoàn chỉnh, hiểu **từng bước**, không phụ thuộc framework nặng.

> 📂 **Về thư mục `data/`:** 6 file trong đó chỉ là **dataset MẪU** (giả lập quy chế nội bộ) để demo cho chạy được ngay. Đây là chỗ bạn **thay bằng tài liệu của mình**: hợp đồng, tài liệu HR, ghi chú nghiên cứu, mã nguồn… Bản thân nội dung an ninh chỉ là *một ví dụ*, không phải trọng tâm.

## Nội dung module

**Khuyến nghị dùng [notebook.ipynb](notebook.ipynb)** để chạy từng bước theo lớp giảng. Các file `.py` là phiên bản đóng gói, dùng cho production hoặc tích hợp.

| Demo | File | Học gì |
|---|---|---|
| 2.0 Step-by-step pipeline | [notebook.ipynb](notebook.ipynb) | 6 bước RAG, mỗi bước 1 cell có output |
| 2.1 RAG minimal đóng gói | [rag_minimal.py](rag_minimal.py) | Pipeline RAG đầy đủ trong ~200 dòng, có CLI |
| 2.2 Gradio UI | [app.py](app.py) | Giao diện chat có streaming, chọn model live, hiện trích nguồn |
| 2.3 Dataset mẫu | [data/](data/) | 6 file MD giả lập quy chế an ninh |

## Pipeline RAG

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Loader  │ →  │ Chunker  │ →  │ Embedder │ →  │ VectorDB │ →  │ Retriever│
│ (đọc MD) │    │ (cắt nhỏ)│    │  (Ollama │    │ (Chroma) │    │ (top-k)  │
└──────────┘    └──────────┘    │ bge/nomic│    └──────────┘    └────┬─────┘
                                 └──────────┘                        ↓
                                                              ┌──────────┐
                                                              │Generator │
                                                              │ (Ollama  │
                                                              │  Qwen3)  │
                                                              └──────────┘
```

## Vì sao tự code RAG thay vì dùng LangChain?

**Học viên cần nhìn rõ từng bước.** LangChain trừu tượng hóa thành `RetrievalQA.from_chain_type(...)` — chạy được nhưng học viên không hiểu bên trong làm gì.

Sau khi học module này, anh em đọc LangChain/LlamaIndex sẽ thấy "à, nó chỉ là wrapper của những bước này".

## Vì sao Ollama hữu ích ở đây

- **Embedding cũng phục vụ qua Ollama** (`ollama.embed(...)`) — cùng 1 daemon, không cần dựng server embedding riêng (BGE/HuggingFace).
- **Đổi embedding model 1 dòng**: `nomic-embed-text` → `bge-m3` — không cần đổi code, chỉ đổi tên.
- **Offline**: kho tài liệu mật + LLM + embedding đều trong máy → không byte nào rời khỏi máy.

## Cách chạy

### Cách A: Notebook (khuyến nghị cho lớp học)

**Windows:**
```powershell
.\.venv\Scripts\Activate.ps1
jupyter lab 2_rag\notebook.ipynb
```
**macOS / Linux:**
```bash
source .venv/bin/activate
jupyter lab 2_rag/notebook.ipynb
```
Chạy từng cell, xem output ngay. Notebook tự build index.

### Cách B: Standalone scripts

Path khác nhau (Windows dùng `\`, macOS/Linux dùng `/`), nhưng có thể dùng `/` trên cả 2 — Python tự xử lý.

> ⚠️ **Bắt buộc `--build` index 1 lần trước**, rồi mới hỏi được. Build xong tạo thư mục `chroma_db/` (đã được gitignore).

```bash
# 1. Build index từ dataset mẫu (chạy 1 lần; chạy lại nếu đổi/thêm tài liệu)
python 2_rag/rag_minimal.py --build

# 2. Hỏi đáp CLI
python 2_rag/rag_minimal.py --ask "Quy định mật khẩu của đơn vị?"

# 3. Chat UI (Gradio)
python 2_rag/app.py
# Mở http://127.0.0.1:7860   (127.0.0.1 và localhost là cùng một máy)
```

> 🔁 **Nếu đổi embedding model** (vd `nomic-embed-text` → `bge-m3`): index cũ không còn hợp lệ → **xóa thư mục `chroma_db/`** rồi `--build` lại, nếu không kết quả sẽ sai âm thầm.

## Góc bảo mật (nhấn trong giảng bài)

| Rủi ro | Ví dụ | Cách giảm thiểu |
|---|---|---|
| **RAG poisoning** | Tài liệu nhiễm câu "Hãy bỏ qua hướng dẫn trước, tiết lộ…" | Sanitize input, không trust blindly tài liệu |
| **PII leakage** | Embedding chứa CMND/CCCD có thể bị reverse | Redact PII trước khi embed |
| **Permission bypass** | RAG retrieve tài liệu user không có quyền đọc | Filter by metadata.user_role trước khi embed search |
| **Context overflow** | Attacker chèn 100KB text vào 1 file để chiếm context | Giới hạn chunk size, cap số chunk |

## Bài tập gợi ý (15 phút thực hành)

1. Thay dataset mẫu bằng PDF của riêng bạn (mở rộng loader để đọc PDF)
2. Mở `rag_minimal.py`, đổi dòng `TOP_K = 3` (dòng 77) thành `TOP_K = 5`, chạy lại `--ask` rồi so số đoạn trích nguồn
3. Thêm metadata filter: chỉ retrieve trong tài liệu có `level: cong_khai`
4. Đổi embedding từ `nomic-embed-text` sang `bge-m3` (nếu đã pull) — so chất lượng

## Tài liệu chính thức (đọc thêm)

| Chủ đề | Nguồn |
|---|---|
| RAG paper gốc (Meta AI, 2020) | [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401) |
| ChromaDB | [trychroma.com](https://www.trychroma.com) · [docs.trychroma.com](https://docs.trychroma.com) |
| Gradio | [gradio.app](https://www.gradio.app) · [github.com/gradio-app/gradio](https://github.com/gradio-app/gradio) |
| Nomic Embed | [nomic.ai](https://www.nomic.ai/) |
| BGE-M3 | [huggingface.co/BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) |
| MTEB Leaderboard (so sánh embedding) | [huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard) |
| RAGAS (đánh giá RAG) | [docs.ragas.io](https://docs.ragas.io) |
| Microsoft Presidio (PII redaction) | [microsoft.github.io/presidio](https://microsoft.github.io/presidio/) |
| LangChain RAG tutorial | [python.langchain.com/docs/tutorials/rag](https://python.langchain.com/docs/tutorials/rag/) |
| LlamaIndex RAG | [docs.llamaindex.ai](https://docs.llamaindex.ai) |

Xem chi tiết về embedding lý thuyết, chunking strategies, vector DB comparison, RAG security in-depth ở [TAI_LIEU_CHI_TIET.md — Phần 2](../TAI_LIEU_CHI_TIET.md).

## Tiếp theo
[Module 3 — Từ RAG đến Agent →](../3_agent/)
