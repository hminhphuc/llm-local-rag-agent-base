# Hướng dẫn: Tự xây dựng ứng dụng RAG bằng mã nguồn (Python)

> Tài liệu này dành cho việc tìm hiểu chuyên sâu và tự xây dựng RAG bằng mã nguồn, thay cho phương án sử dụng giao diện Open WebUI (không lập trình). Kết quả là một file `rag_app.py` (~130 dòng), vận hành hoàn toàn trên máy cục bộ, không yêu cầu kết nối Internet.
> Toàn bộ mã nguồn dưới đây đã được kiểm chứng bằng thực nghiệm và cho ra câu trả lời kèm trích nguồn.

## Mục lục
1. [Mục tiêu xây dựng](#1-mục-tiêu-xây-dựng)
2. [Chuẩn bị](#2-chuẩn-bị)
3. [Cấu hình](#3-cấu-hình)
4. [Xây dựng từng bước (6 bước RAG)](#4-xây-dựng-từng-bước--6-bước-rag)
5. [Chạy thử](#5-chạy-thử)
6. [Tùy biến theo nhu cầu](#6-tùy-biến-theo-nhu-cầu)
7. [Bổ sung giao diện web (tùy chọn)](#7-bổ-sung-giao-diện-web-tùy-chọn)
8. [Lỗi thường gặp](#8-lỗi-thường-gặp)

---

## 1. Mục tiêu xây dựng

Sản phẩm là một ứng dụng RAG thực hiện chức năng: nạp tài liệu, tiếp nhận câu hỏi, và trả lời bám sát nội dung tài liệu kèm trích nguồn. Pipeline gồm 6 bước, chia thành 2 pha:

| Pha | Bước | Chạy khi nào |
|---|---|---|
| **Offline** (build 1 lần) | 1. Load → 2. Chunk → 3. Embed → 4. Store | `--build` |
| **Online** (mỗi câu hỏi) | 5. Retrieve → 6. Generate | `--ask "..."` |

Công nghệ sử dụng: Python kết hợp **Ollama** (vận hành LLM và mô hình nhúng cục bộ) và **ChromaDB** (cơ sở dữ liệu vector). Tài liệu không sử dụng LangChain nhằm trình bày rõ từng bước; LangChain về bản chất là một lớp bọc trên chính các bước này.

![](docs/diagrams/02_rag_pipeline.png)

---

## 2. Chuẩn bị

**a) Ollama và 2 mô hình** (chi tiết cài đặt Ollama được trình bày trong `HUONG_DAN_HOC_VIEN.md`):
```bash
ollama pull qwen3:1.7b        # LLM trả lời
ollama pull nomic-embed-text  # model embedding (chữ → vector)
```

**b) Hai thư viện Python** (nên kích hoạt `venv` trước):
```bash
pip install ollama chromadb
```

**c) Tài liệu nguồn:** một thư mục chứa file `.md` / `.txt`. Tài liệu này dùng sẵn `2_rag/data/` (6 file quy chế mẫu); về sau có thể thay bằng tài liệu khác.

---

## 3. Cấu hình

Tạo file `rag_app.py`, mở đầu bằng phần import và các hằng số cấu hình:

```python
import argparse, glob, os, sys
import chromadb, ollama

# In tiếng Việt không vỡ trên console Windows (mặc định cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA_DIR    = "2_rag/data"      # thư mục tài liệu nguồn (.md / .txt)
DB_DIR      = "chroma_db"       # nơi ChromaDB lưu vector (tự tạo)
COLLECTION  = "rag_docs"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL   = "qwen3:1.7b"
CHUNK_SIZE    = 500             # số ký tự mỗi đoạn
CHUNK_OVERLAP = 50              # ký tự gối nhau giữa 2 đoạn liền kề
TOP_K         = 3               # số đoạn lấy ra cho mỗi câu hỏi
```

Lưu ý: ba giá trị `500 / 50 / 3` tương ứng với Chunk Size, Overlap và Top-K trong lý thuyết. Việc thay đổi các giá trị này phục vụ thử nghiệm chất lượng.

---

## 4. Xây dựng từng bước — 6 bước RAG

### Bước 1 — Load: đọc tài liệu

Đọc mọi file `.md`/`.txt` trong thư mục, lưu kèm tên file để phục vụ trích nguồn về sau.

```python
def load_documents(data_dir=DATA_DIR):
    docs = []
    paths = sorted(glob.glob(os.path.join(data_dir, "*.md")) +
                   glob.glob(os.path.join(data_dir, "*.txt")))
    for path in paths:
        with open(path, encoding="utf-8") as f:
            docs.append({"source": os.path.basename(path), "text": f.read()})
    return docs
```

### Bước 2 — Chunk: cắt thành đoạn nhỏ

LLM không xử lý được toàn bộ file một lúc; do đó tài liệu được cắt thành đoạn khoảng 500 ký tự. **Overlap 50** giúp các câu nằm vắt ngang ranh giới không bị cắt cụt nghĩa.

```python
def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks, start = [], 0
    while start < len(text):
        chunk = text[start:start + size].strip()
        if chunk:
            chunks.append(chunk)
        start += size - overlap        # dịch tới, chừa phần overlap
    return chunks
```

### Bước 3 — Embed: chữ → vector (chạy local)

Mỗi đoạn được biến đổi thành một **vector** (với `nomic-embed-text` là 768 chiều) thông qua Ollama; dữ liệu không được gửi ra ngoài. Toàn bộ danh sách được truyền vào để nhúng theo lô nhằm tăng tốc độ.

```python
def embed(texts):
    """texts: list[str] -> list[list[float]] (mỗi text một vector)."""
    resp = ollama.embed(model=EMBED_MODEL, input=texts)
    return resp["embeddings"]
```

### Bước 4 — Store: lưu vào ChromaDB (build index)

Với mỗi đoạn, ChromaDB lưu đồng thời **id + vector + văn bản gốc + metadata** (tên file). Collection cũ được xóa trước để quá trình lập chỉ mục lại được thực hiện trên trạng thái sạch.

```python
def build_index():
    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        client.delete_collection(COLLECTION)   # build lại từ đầu cho sạch
    except Exception:
        pass
    col = client.create_collection(COLLECTION)

    ids, documents, metadatas = [], [], []
    docs = load_documents()
    for d in docs:
        for i, ch in enumerate(chunk_text(d["text"])):
            ids.append(f"{d['source']}::{i}")
            documents.append(ch)
            metadatas.append({"source": d["source"], "chunk": i})

    embeddings = embed(documents)              # embed cả lô 1 lần
    col.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    print(f"[Build] {len(docs)} tài liệu -> {len(documents)} đoạn đã lưu vào '{COLLECTION}'.")
```

### Bước 5 — Retrieve: tìm top-k đoạn gần nghĩa nhất

Câu hỏi được nhúng thành vector, sau đó ChromaDB truy hồi `k` đoạn gần nhất (giá trị `distance` càng nhỏ thì mức tương đồng ngữ nghĩa càng cao).

```python
def retrieve(question, k=TOP_K):
    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        col = client.get_collection(COLLECTION)
    except Exception:
        raise SystemExit("Chưa có index. Chạy: python rag_app.py --build")
    q_emb = embed([question])[0]
    res = col.query(query_embeddings=[q_emb], n_results=k)
    return [
        {"text": doc, "source": meta["source"], "distance": dist}
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]
```

### Bước 6 — Generate: LLM trả lời dựa trên ngữ cảnh

Các đoạn truy hồi được ghép thành **ngữ cảnh**, đưa vào một **prompt** ràng buộc mô hình chỉ trả lời theo tài liệu, rồi gọi LLM. Kết quả được in kèm **trích nguồn**.

```python
def generate_answer(question):
    hits = retrieve(question)
    context = "\n\n".join(f"[Nguồn: {h['source']}]\n{h['text']}" for h in hits)
    prompt = (
        "Chỉ trả lời dựa trên TÀI LIỆU dưới đây. Nếu tài liệu không đủ thông tin, "
        "trả lời đúng câu 'Tài liệu không đề cập'. Trả lời bằng tiếng Việt.\n\n"
        f"=== TÀI LIỆU ===\n{context}\n\n=== CÂU HỎI ===\n{question}"
    )
    resp = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        think=False,                  # qwen3: tắt 'suy nghĩ' cho output sạch
    )
    print(resp["message"]["content"].strip())
    nguon = ", ".join(sorted({h["source"] for h in hits}))
    print(f"\n--- Trích nguồn: {nguon}")
```

Quan trọng: cốt lõi của RAG nằm ở prompt này. Yêu cầu "chỉ trả lời dựa trên tài liệu, nếu thiếu thì trả lời 'không đề cập'" là yếu tố giảm thiểu hiện tượng bịa đặt và làm cho câu trả lời có thể kiểm chứng được.

### Ghép lại — CLI

```python
def main():
    ap = argparse.ArgumentParser(description="Ứng dụng RAG local (Ollama + ChromaDB)")
    ap.add_argument("--build", action="store_true", help="Build index từ tài liệu")
    ap.add_argument("--ask", type=str, metavar="CÂU_HỎI", help="Đặt 1 câu hỏi")
    args = ap.parse_args()
    if args.build:
        build_index()
    elif args.ask:
        generate_answer(args.ask)
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
```

Lưu ý: mã nguồn đầy đủ có sẵn tại file **`rag_app.py`** trong repo.

---

## 5. Chạy thử

```bash
# 1) Build index (chạy 1 lần; chạy lại khi đổi/thêm tài liệu)
python rag_app.py --build

# 2) Hỏi
python rag_app.py --ask "Quy trình xử lý sự cố ATTT gồm những bước nào?"
```

Kết quả thực nghiệm (rút gọn):
```text
[Build] 6 tài liệu -> 25 đoạn đã lưu vào 'rag_docs'.

Quy trình xử lý sự cố ATTT gồm những bước sau:
1. Chuẩn bị (Preparation) — duy trì danh sách ứng cứu (CIRT), cập nhật playbook, diễn tập...
2. Phát hiện và phân tích — nhận cảnh báo SIEM/IDS, xác định ưu tiên (P1-P4), thu thập bằng chứng...
3. Cách ly (Containment) — chặn IP, disable account...

--- Trích nguồn: 03_quy_trinh_su_co.md
```

Phần **Trích nguồn** trỏ đúng file xác nhận RAG đang vận hành đúng: câu trả lời bám theo tài liệu nguồn, không bịa đặt.

---

## 6. Tùy biến theo nhu cầu

| Muốn gì | Làm sao |
|---|---|
| Dùng **tài liệu riêng** | Đặt file `.md`/`.txt` vào thư mục `DATA_DIR`, sau đó chạy lại `--build`. (PDF: chuyển sang `.txt` trước.) |
| Đổi/thêm tài liệu | **Build lại** (`--build`); mã nguồn tự xóa index cũ rồi dựng lại. |
| Đoạn to/nhỏ | Chỉnh `CHUNK_SIZE` / `CHUNK_OVERLAP`, rồi `--build` lại. |
| Lấy nhiều đoạn hơn | Tăng `TOP_K` (3 → 5): ngữ cảnh đầy đặn hơn nhưng độ trễ cao hơn. |
| Trả lời chất lượng hơn | Đổi `LLM_MODEL` sang `qwen3:4b` (cần RAM 16GB). |
| Embedding mạnh hơn | Đổi `EMBED_MODEL` sang `bge-m3` (1024 chiều); cần `--build` lại vì số chiều khác. |
| Đổi giọng/ngôn ngữ trả lời | Sửa `prompt` trong `generate_answer`. |

Quan trọng: đổi mô hình embedding bắt buộc lập chỉ mục lại. Vector cũ và mới khác nhau về số chiều và không gian; trộn lẫn sẽ cho kết quả sai. Xóa thư mục `chroma_db/` rồi chạy `--build`.

---

## 7. Bổ sung giao diện web (tùy chọn)

Trường hợp cần một ô chat thay cho thao tác trên terminal, có thể dùng **Gradio** (~12 dòng). Điều chỉnh `generate_answer` để **trả về chuỗi** thay vì `print`, sau đó:

```bash
pip install gradio
```
```python
# rag_ui.py
import gradio as gr
from rag_app import retrieve, LLM_MODEL
import ollama

def answer(question, history):
    hits = retrieve(question)
    context = "\n\n".join(f"[Nguồn: {h['source']}]\n{h['text']}" for h in hits)
    prompt = ("Chỉ trả lời dựa trên tài liệu sau, thiếu thì nói 'Tài liệu không đề cập', "
              f"tiếng Việt.\n\n{context}\n\nCâu hỏi: {question}")
    out = ollama.chat(model=LLM_MODEL, messages=[{"role": "user", "content": prompt}],
                      think=False)["message"]["content"].strip()
    nguon = ", ".join(sorted({h["source"] for h in hits}))
    return f"{out}\n\n— Trích nguồn: {nguon}"

gr.ChatInterface(answer, title="Trợ lý RAG local").launch()
```
Chạy `python rag_ui.py`, sau đó mở địa chỉ Gradio được in ra (thường là `http://127.0.0.1:7860`). Cần chạy `--build` trước để có index.

Lưu ý: đây là phương án tự xây dựng giao diện. Trường hợp chỉ cần một giao diện dựng sẵn mà không lập trình, sử dụng **Open WebUI** (xem `HUONG_DAN_HOC_VIEN.md`).

---

## 8. Lỗi thường gặp

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `ModuleNotFoundError: chromadb` / `ollama` | Chưa cài thư viện / chưa bật venv | `pip install ollama chromadb`; bật venv (đầu dòng có `(.venv)`) |
| `UnicodeEncodeError` khi in tiếng Việt | Console Windows dùng cp1252 | Đã có `sys.stdout.reconfigure(encoding="utf-8")` đầu file; hoặc đặt biến môi trường `PYTHONUTF8=1` |
| `Chưa có index. Chạy: --build` | Chưa build hoặc xóa nhầm `chroma_db/` | Chạy `python rag_app.py --build` trước |
| `Connection refused` / không gọi được model | Ollama chưa chạy | Mở app Ollama; kiểm tra `ollama list` |
| `model "..." not found` | Chưa pull model | `ollama pull qwen3:1.7b` và `ollama pull nomic-embed-text` |
| Đổi embedding xong kết quả sai | Index cũ dùng embedding cũ | Xóa thư mục `chroma_db/` → `--build` lại |
| Trả lời lệch / "Tài liệu không đề cập" dù có | Model nhỏ `1.7b` + câu hỏi cộc lốc | Hỏi bằng câu tự nhiên (tránh mã ngắn "P1"); tăng `TOP_K`; đổi `qwen3:4b` |

---

> Tài liệu liên quan: **`HUONG_DAN_HOC_VIEN.md`** (dùng RAG bằng giao diện Open WebUI, không code) · sơ đồ `docs/diagrams/02_rag_pipeline.png`.
