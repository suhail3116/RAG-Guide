import os
import sys
import json
import shutil
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from langchain_community.vectorstores import Chroma
from services.embedder import FastOllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import config

def build_incremental():
    print("[BUILD] Starting batch-by-batch vector database build...")
    
    # 1. Clean old vector DB directory if locked or reset
    persist_dir = str(config.PERSIST_DIR)
    
    # 2. Load articles cache & curated docs
    with open("data/articles_cache.json", "r", encoding="utf-8") as f:
        cache_data = json.load(f)

    from services.curated_docs import get_curated_documents
    curated = get_curated_documents()

    all_docs = list(cache_data.values())
    for c in curated:
        all_docs.append({
            "title": c["title"],
            "full_text": c["full_text"],
            "url": c["url"],
            "image_url": c.get("image_url", ""),
            "categories": c.get("categories", [])
        })

    print(f"[BUILD] Loaded {len(all_docs)} total documents.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    embeddings = FastOllamaEmbeddings(model=config.EMBED_MODEL, base_url=config.OLLAMA_BASE_URL)

    # Delete existing vector DB directory if starting a fresh build
    if os.path.exists(persist_dir):
        try:
            shutil.rmtree(persist_dir)
            print(f"[BUILD] Cleaned existing persist directory: {persist_dir}", flush=True)
        except Exception as e:
            print(f"[BUILD] Warning cleaning directory: {e}", flush=True)

    # Initialize empty Chroma DB
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name=config.COLLECTION_NAME
    )

    # Process document by document, and embed in sub-batches of 30 chunks for fast commits
    total_chunks_added = 0
    doc_count = len(all_docs)
    for idx, d in enumerate(all_docs, 1):
        title = d.get("title", "Unknown")
        text_content = d.get("full_text") or d.get("page_content") or ""
        if not text_content:
            continue
        c_list = splitter.create_documents(
            texts=[text_content],
            metadatas=[{
                "title": title,
                "url": d.get("url", ""),
                "image_url": d.get("image_url", ""),
                "categories": ",".join(d.get("categories", []))
            }]
        )
        if not c_list:
            continue
        
        print(f"[{idx}/{doc_count}] Embedding '{title}' ({len(c_list)} chunks)...", flush=True)
        # Sub-batch in chunks of 30
        sub_size = 30
        for s in range(0, len(c_list), sub_size):
            sub_chunks = c_list[s:s+sub_size]
            vectorstore.add_documents(sub_chunks)
            print(f"   Indexed {s + len(sub_chunks)}/{len(c_list)} chunks...", flush=True)
        
        total_chunks_added += len(c_list)
        print(f"   [OK] '{title}' complete! (Total indexed so far: {total_chunks_added})\n", flush=True)

    total_count = vectorstore._collection.count()
    print(f"\n✅ Build complete! Total vector chunks indexed: {total_count}", flush=True)

if __name__ == "__main__":
    build_incremental()
