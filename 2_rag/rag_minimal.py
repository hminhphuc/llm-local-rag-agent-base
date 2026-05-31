"""
RAG minimal — pipeline đầy đủ 5 bước, KHÔNG phụ thuộc LangChain.

PIPELINE TỔNG QUAN:
    ┌────────┐   ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌──────────┐
    │ Loader │ → │ Chunker │ → │ Embedder│ → │ VectorDB │ → │ Retriever│
    │ (.md)  │   │ (cắt)   │   │ (Ollama)│   │ (Chroma) │   │ (top-k)  │
    └────────┘   └─────────┘   └─────────┘   └──────────┘   └────┬─────┘
                                                                  ↓
                                                            ┌──────────┐
                                                            │Generator │
                                                            │ (LLM)    │
                                                            └──────────┘

VÌ SAO KHÔNG DÙNG LANGCHAIN?
    Lớp học cần hiểu rõ từng bước. LangChain wrap thành 1 dòng
    `RetrievalQA.from_chain_type(...)` — chạy được nhưng học viên không
    hiểu bên trong. Sau khi hiểu pipeline này, đọc LangChain sẽ thấy
    "chỉ là wrapper của các bước này".

CÁCH DÙNG:
    python 2_rag/rag_minimal.py --build              # build index lần đầu
    python 2_rag/rag_minimal.py --ask "câu hỏi"      # hỏi 1 câu
    python 2_rag/rag_minimal.py --interactive        # chat liên tục

TUỲ BIẾN PHỔ BIẾN:
    - Đổi model:    set biến môi trường LLM_MODEL / EMBED_MODEL
    - Đổi data:     đổi DATA_DIR
    - Đổi chunking: sửa CHUNK_SIZE / CHUNK_OVERLAP
    - Đổi top-k:    sửa TOP_K
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import chromadb
import ollama

# Nạp file .env ở thư mục gốc repo (do pull_models.sh/ps1 tự ghi khi pull model).
# Nhờ vậy, nếu bạn chọn model khác lúc pull, code tự dùng đúng model đó.
# Nếu chưa cài python-dotenv hoặc chưa có .env → bỏ qua, dùng default bên dưới.
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

# ============================================================
# CẤU HÌNH (tách riêng để dễ tuỳ biến)
# ============================================================
# Đọc từ env trước (gồm cả .env vừa nạp), có default nếu chưa set.
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:1.7b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

# Thư mục chứa dataset. Đổi sang path tài liệu thật khi triển khai.
DATA_DIR = Path(__file__).parent / "data"

# Nơi lưu vector DB. Tự tạo nếu chưa có. Có thể xóa thư mục này để build lại từ đầu.
DB_DIR = Path(__file__).parent / "chroma_db"

# Tên collection trong ChromaDB. Có thể có nhiều collection trong cùng DB.
COLLECTION_NAME = "quy_che_an_ninh"

# Chunking: cắt text thành đoạn ~500 ký tự, overlap 50 ký tự.
# Sweet spot cho tiếng Việt:
#   - 300-700 ký tự: vừa đủ giữ 1 ý, không loãng
#   - Overlap 10-20% size: giữ ngữ cảnh ở rìa cắt
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Số đoạn liên quan trả về cho mỗi câu hỏi.
# Top-k cao → context phong phú nhưng tốn token, dễ làm LLM bị nhiễu.
# Top-k thấp → context tập trung nhưng có thể bỏ sót ý.
TOP_K = 3


# ============================================================
# BƯỚC 1 — LOAD: đọc tài liệu
# ============================================================
def load_documents(data_dir: Path) -> list[dict]:
    """Đọc mọi file .md trong thư mục, trả về list dict.

    Mỗi dict gồm:
        - source: tên file (để trích nguồn khi trả lời)
        - text:   nội dung text

    MỞ RỘNG cho production:
        - Đọc PDF:    dùng pypdf, pdfplumber
        - Đọc DOCX:   dùng python-docx
        - Đọc HTML:   dùng BeautifulSoup
        - Đa định dạng: dùng unstructured.io
    """
    docs = []
    for md_file in sorted(data_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        docs.append({"source": md_file.name, "text": text})
    return docs


# ============================================================
# BƯỚC 2 — CHUNK: cắt nhỏ
# ============================================================
def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Cắt text thành các đoạn có overlap.

    Chiến lược: cắt theo số ký tự, có overlap để giữ ngữ cảnh ở rìa cắt.
    Ví dụ với size=500, overlap=50:
        Chunk 1: ký tự [0..500]
        Chunk 2: ký tự [450..950]    ← overlap 50 với chunk 1
        Chunk 3: ký tự [900..1400]   ← overlap 50 với chunk 2

    NÂNG CAO (bài tập cho học viên):
        - Semantic chunking: cắt theo câu (split bằng dấu chấm) hoặc
          theo heading Markdown (# ## ###). Giữ trọn ý tốt hơn.
        - Recursive chunking: thử cắt theo \\n\\n trước, nếu vẫn quá dài
          mới cắt theo \\n, rồi đến câu, rồi đến ký tự.
        - LangChain có RecursiveCharacterTextSplitter làm sẵn việc này.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        # Dịch start nhưng có overlap → không nhảy hết size
        start += size - overlap
    return chunks


# ============================================================
# BƯỚC 3 — EMBED: text → vector
# ============================================================
def embed_texts(texts: list[str], model: str = EMBED_MODEL) -> list[list[float]]:
    """Gọi Ollama embedding cho 1 list text.

    Embedding model dùng ở đây:
        - nomic-embed-text: 768 chiều, 274MB, multilingual khá
        - bge-m3:           1024 chiều, 1.2GB, multilingual rất tốt

    Tham số `input` của ollama.embed nhận list → batch embedding 1 lần,
    nhanh hơn nhiều so với gọi từng cái một.

    Trả về: list các vector (mỗi vector là list float).
    """
    response = ollama.embed(model=model, input=texts)
    return response.embeddings


# ============================================================
# BƯỚC 4 — STORE: lưu vào ChromaDB
# ============================================================
def build_index() -> None:
    """Đọc data/, chunk, embed, ghi vào ChromaDB.

    Chỉ cần chạy 1 lần (hoặc khi data thay đổi). Sau khi build xong,
    file index nằm ở DB_DIR và có thể query nhiều lần.

    LƯU Ý: hàm này XÓA collection cũ rồi tạo mới. Nếu muốn append (không xóa),
    bỏ phần delete_collection và dùng collection.add() để thêm.
    """
    print(f"[Build] Đang đọc tài liệu từ {DATA_DIR}...")
    docs = load_documents(DATA_DIR)
    print(f"[Build] Tìm thấy {len(docs)} tài liệu.")

    # Gom toàn bộ chunk lại để embed batch 1 lần (nhanh hơn embed từng cái)
    all_chunks: list[str] = []
    all_metadatas: list[dict] = []
    all_ids: list[str] = []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            # Metadata đi kèm chunk — cực kỳ hữu ích để:
            #   1. Trích nguồn khi trả lời ("theo file X")
            #   2. Filter khi query (ví dụ: chỉ tìm trong file Y)
            #   3. Debug khi RAG trả sai
            all_metadatas.append({"source": doc["source"], "chunk_index": i})
            # ID phải unique trong collection. Format này dễ trace lại nguồn.
            all_ids.append(f"{doc['source']}_chunk_{i}")

    print(f"[Build] Tổng số chunk: {len(all_chunks)}")
    print(f"[Build] Đang embed bằng model '{EMBED_MODEL}'...")
    embeddings = embed_texts(all_chunks)
    print(f"[Build] Hoàn tất embed. Vector dimension: {len(embeddings[0])}")

    # PersistentClient lưu xuống đĩa (khác từ chromadb.Client() — chỉ in-memory)
    DB_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(DB_DIR))

    # Xóa collection cũ để build lại sạch. Nếu chưa có collection thì pass.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    # Add 4 cùng lúc — ChromaDB lưu vector + text + metadata + id song song.
    # Lúc query, nó tự xếp lại đúng nhau.
    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadatas,
        ids=all_ids,
    )
    print(f"[Build] Đã lưu vào {DB_DIR}/")
    print(f"[Build] Xong. Thử: python {Path(__file__).name} --ask \"Quy định mật khẩu?\"")


# ============================================================
# BƯỚC 5 — RETRIEVE: tìm chunk gần nhất với câu hỏi
# ============================================================
def retrieve(question: str, top_k: int = TOP_K) -> list[dict]:
    """Embed câu hỏi, tìm top-k chunk gần nhất trong vector DB.

    "Gần nhất" theo cosine distance — càng nhỏ càng giống.
    ChromaDB dùng HNSW algorithm bên trong → tìm nhanh kể cả với hàng triệu vector.
    """
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    # Embed câu hỏi bằng CÙNG model đã dùng để embed chunks.
    # Nếu dùng model khác → vector ở 2 không gian khác → kết quả vô nghĩa.
    q_emb = embed_texts([question])[0]

    # query() trả về dict các list, mỗi list 1 phần tử (vì ta chỉ query 1 câu).
    # Dùng [0] để lấy phần tử đầu của list ngoài.
    results = collection.query(query_embeddings=[q_emb], n_results=top_k)

    # Đóng gói lại thành list dict cho dễ dùng
    hits = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append({"text": doc, "source": meta["source"], "distance": dist})
    return hits


# ============================================================
# BƯỚC 6 — GENERATE: LLM sinh câu trả lời từ chunk
# ============================================================
def generate_answer(question: str, contexts: list[dict]) -> str:
    """Đưa các đoạn retrieve được vào prompt, gọi LLM sinh câu trả lời.

    Đây là chữ G trong RAG (Retrieval-Augmented GENERATION).

    PROMPT ENGINEERING quan trọng:
        - "Chỉ trả lời dựa vào tài liệu" → giảm hallucination
        - "Nếu không đủ thông tin, nói rõ" → tránh bịa
        - "Trích nguồn" → audit được, học viên kiểm chứng được
    """
    # Ghép các chunk + metadata thành 1 khối context cho LLM
    context_text = "\n\n".join(
        f"[Nguồn: {c['source']}]\n{c['text']}" for c in contexts
    )

    # Prompt được thiết kế để dễ đọc với LLM:
    # - Tách phần rõ ràng bằng dòng "===
    # - Đặt câu hỏi sau context (LLM tập trung vào câu hỏi gần cuối)
    prompt = f"""Bạn là trợ lý tra cứu tài liệu nội bộ. Dùng tài liệu sau để trả lời câu hỏi.

Nguyên tắc:
- Chỉ trả lời dựa vào tài liệu được cung cấp.
- Nếu tài liệu không đủ thông tin, nói rõ "Tài liệu không đề cập".
- Trích nguồn (tên file) sau mỗi ý.

=== Tài liệu ===
{context_text}

=== Câu hỏi ===
{question}

=== Trả lời ==="""

    # temperature thấp (0.2) cho câu trả lời nhất quán, ít sáng tạo.
    # Với RAG luôn nên dùng temperature thấp vì ta muốn LLM bám sát tài liệu.
    # think=False: tắt thinking mode của Qwen3 (cho ra `<think>...</think>` block dài,
    # không cần cho RAG. Nếu model không hỗ trợ tham số này, Ollama bỏ qua.
    try:
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2},
            think=False,
        )
    except TypeError:
        # Phiên bản ollama-python cũ chưa hỗ trợ tham số think
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2},
        )
    return response.message.content


# ============================================================
# Hàm tiện ích: chạy đầy đủ pipeline 1 lần
# ============================================================
def ask(question: str, show_context: bool = True) -> None:
    """Pipeline đầy đủ: retrieve + generate, in ra terminal có cấu trúc."""
    print(f"\n[Câu hỏi] {question}")
    print(f"[Retrieve] Đang tìm top-{TOP_K} đoạn liên quan...")
    hits = retrieve(question)

    # In tóm tắt các chunk retrieve được — giúp học viên nhìn thấy
    # "LLM đang dựa vào gì" để trả lời (debug, audit)
    if show_context:
        print("\n[Đoạn tìm được]")
        for i, h in enumerate(hits, 1):
            preview = h["text"][:120].replace("\n", " ")
            print(f"  {i}. [{h['source']}] (distance={h['distance']:.3f}) {preview}...")

    print("\n[Sinh câu trả lời]")
    answer = generate_answer(question, hits)
    print(f"\n{answer}\n")


def interactive() -> None:
    """Chế độ chat liên tục — gõ câu hỏi, nhận trả lời, lặp lại.

    GHI CHÚ: chưa giữ lịch sử hội thoại (mỗi câu hỏi là một query độc lập).
    Mở rộng: lưu messages vào list, gửi cả list cho generate_answer.
    """
    print(f"=== RAG interactive (model={LLM_MODEL}, embed={EMBED_MODEL}) ===")
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
        ask(q, show_context=False)


# ============================================================
# CLI entry point
# ============================================================
def main() -> None:
    parser = argparse.ArgumentParser(description="RAG minimal cho workshop")
    parser.add_argument("--build", action="store_true", help="Build lại index từ data/")
    parser.add_argument("--ask", type=str, help="Hỏi 1 câu rồi thoát")
    parser.add_argument("--interactive", action="store_true", help="Chế độ chat liên tục")
    args = parser.parse_args()

    if args.build:
        build_index()
        return

    # Nếu chưa build index, không thể query → báo lỗi rõ ràng
    if not DB_DIR.exists():
        print(f"Chưa có index. Chạy trước: python {Path(__file__).name} --build")
        return

    if args.ask:
        ask(args.ask)
    elif args.interactive:
        interactive()
    else:
        # Không có flag → chạy demo mặc định cho học viên có cái nhìn nhanh
        ask("Quy định mật khẩu của đơn vị như thế nào?")


if __name__ == "__main__":
    main()
