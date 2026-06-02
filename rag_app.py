# -*- coding: utf-8 -*-
"""
rag_app.py — Ứng dụng RAG tối giản, 100% local (Ollama + ChromaDB), KHÔNG dùng LangChain.

Pipeline 6 bước:
    Load → Chunk → Embed → Store   (offline, chạy 1 lần: --build)
    Retrieve → Generate            (online, mỗi câu hỏi: --ask "...")

Yêu cầu: Ollama đang chạy + đã pull `qwen3:1.7b` và `nomic-embed-text`;
         pip install ollama chromadb

Cách dùng:
    python rag_app.py --build
    python rag_app.py --ask "Quy trình xử lý sự cố ATTT gồm những bước nào?"
"""
import argparse
import glob
import os
import sys

import chromadb
import ollama

# In tiếng Việt không vỡ trên console Windows (mặc định cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ===== Cấu hình =====
DATA_DIR = "2_rag/data"          # thư mục tài liệu nguồn (.md / .txt)
DB_DIR = "chroma_db"             # nơi ChromaDB lưu vector (tự tạo)
COLLECTION = "rag_docs"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "qwen3:1.7b"
CHUNK_SIZE = 500                 # số ký tự mỗi đoạn
CHUNK_OVERLAP = 50               # số ký tự gối nhau giữa 2 đoạn
TOP_K = 3                        # số đoạn lấy ra cho mỗi câu hỏi


# ===== Bước 1 — LOAD: đọc tài liệu =====
def load_documents(data_dir=DATA_DIR):
    docs = []
    paths = sorted(glob.glob(os.path.join(data_dir, "*.md")) +
                   glob.glob(os.path.join(data_dir, "*.txt")))
    for path in paths:
        with open(path, encoding="utf-8") as f:
            docs.append({"source": os.path.basename(path), "text": f.read()})
    return docs


# ===== Bước 2 — CHUNK: cắt thành đoạn nhỏ có gối nhau =====
def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks, start = [], 0
    while start < len(text):
        chunk = text[start:start + size].strip()
        if chunk:
            chunks.append(chunk)
        start += size - overlap
    return chunks


# ===== Bước 3 — EMBED: chữ → vector (chạy local qua Ollama) =====
def embed(texts):
    """texts: list[str] → list[list[float]] (mỗi text 1 vector)."""
    resp = ollama.embed(model=EMBED_MODEL, input=texts)
    return resp["embeddings"]


# ===== Bước 4 — STORE: lưu vector vào ChromaDB (build index) =====
def build_index():
    client = chromadb.PersistentClient(path=DB_DIR)
    try:                                    # build lại từ đầu cho sạch
        client.delete_collection(COLLECTION)
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

    embeddings = embed(documents)           # embed cả lô 1 lần
    col.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    print(f"[Build] {len(docs)} tài liệu → {len(documents)} đoạn đã lưu vào '{COLLECTION}'.")


# ===== Bước 5 — RETRIEVE: tìm top-k đoạn gần nghĩa nhất =====
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


# ===== Bước 6 — GENERATE: LLM trả lời dựa trên ngữ cảnh + trích nguồn =====
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
        think=False,                        # qwen3: tắt 'suy nghĩ' cho output sạch
    )
    print(resp["message"]["content"].strip())
    nguon = ", ".join(sorted({h["source"] for h in hits}))
    print(f"\n--- Trích nguồn: {nguon}")


def main():
    ap = argparse.ArgumentParser(description="Ứng dụng RAG local (Ollama + ChromaDB)")
    ap.add_argument("--build", action="store_true", help="Build index từ tài liệu trong data/")
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
