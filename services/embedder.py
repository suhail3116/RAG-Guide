try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except (ImportError, ModuleNotFoundError):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from langchain_core.documents import Document
except (ImportError, ModuleNotFoundError):
    from langchain.schema import Document

import requests
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma
from typing import List, Dict, Optional
from config import config
import shutil
import os

class FastOllamaEmbeddings(Embeddings):
    def __init__(self, model: str = config.EMBED_MODEL, base_url: str = config.OLLAMA_BASE_URL):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        batch_size = 50
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            resp = requests.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model, "input": batch},
                timeout=120
            )
            if resp.status_code == 200:
                embeddings.extend(resp.json()["embeddings"])
            else:
                raise RuntimeError(f"Ollama embed error {resp.status_code}: {resp.text}")
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        resp = requests.post(
            f"{self.base_url}/api/embed",
            json={"model": self.model, "input": [text]},
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()["embeddings"][0]
        else:
            raise RuntimeError(f"Ollama embed error {resp.status_code}: {resp.text}")

class Embedder:
    def __init__(self):
        self.embeddings = FastOllamaEmbeddings()
        self.vectorstore: Optional[Chroma] = None
        self._init_vectorstore()

    def _init_vectorstore(self):
        """Initialize or load existing vector store."""
        if config.PERSIST_DIR.exists():
            try:
                self.vectorstore = Chroma(
                    persist_directory=str(config.PERSIST_DIR),
                    embedding_function=self.embeddings,
                    collection_name=config.COLLECTION_NAME
                )
                count = self.vectorstore._collection.count() if self.vectorstore._collection else 0
            except Exception as e:
                self.vectorstore = None

    def chunk_documents(self, documents: List[Dict]) -> List[Document]:
        """Split documents into chunks."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len
        )

        docs = []
        for doc in documents:
            chunks = splitter.create_documents(
                texts=[doc["full_text"]],
                metadatas=[{
                    "title": doc["title"],
                    "url": doc.get("url", ""),
                    "image_url": doc.get("image_url", ""),
                    "categories": ",".join(doc.get("categories", [])),
                }]
            )
            docs.extend(chunks)

        print(f"[OK] Created {len(docs)} chunks from {len(documents)} documents")
        return docs

    def build_index(self, documents: List[Dict]):
        """Build vector index from documents."""
        # Clear existing collection safely without locking file conflicts on Windows
        if self.vectorstore:
            try:
                self.vectorstore.delete_collection()
            except Exception:
                pass
            self.vectorstore = None
        elif config.PERSIST_DIR.exists():
            try:
                shutil.rmtree(config.PERSIST_DIR)
            except Exception:
                pass

        # Chunk documents
        chunks = self.chunk_documents(documents)

        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=str(config.PERSIST_DIR),
            collection_name=config.COLLECTION_NAME
        )

        print(f"[OK] Vector store built and persisted with {len(chunks)} chunks")

    def add_documents(self, documents: List[Dict]):
        """Add more documents to existing index."""
        if not self.vectorstore:
            self.build_index(documents)
            return

        chunks = self.chunk_documents(documents)
        self.vectorstore.add_documents(chunks)
        print(f"[OK] Added {len(chunks)} new chunks")

    def get_retriever(self, top_k: int = 3):
        """Get a retriever for the vector store."""
        if not self.vectorstore or not config.PERSIST_DIR.exists():
            self._init_vectorstore()

        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Build index first.")

        try:
            _ = self.vectorstore._collection.count()
        except Exception:
            self._init_vectorstore()

        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Build index first.")

        return self.vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )

    def get_stats(self) -> Dict:
        """Get statistics about the vector store."""
        if not self.vectorstore:
            self._init_vectorstore()

        if not self.vectorstore:
            return {"total_chunks": 0, "topics_count": 0, "topics": []}

        try:
            chunks = self.vectorstore._collection.count()
            data = self.vectorstore.get()
            topics = set(m.get("title", "unknown") for m in data.get("metadatas", []))
        except Exception:
            try:
                self._init_vectorstore()
                chunks = self.vectorstore._collection.count() if self.vectorstore else 0
                data = self.vectorstore.get() if self.vectorstore else {}
                topics = set(m.get("title", "unknown") for m in data.get("metadatas", []))
            except Exception:
                chunks = 0
                topics = set()

        return {
            "total_chunks": chunks,
            "topics_count": len(topics),
            "topics": list(topics)
        }

# Singleton
embedder = Embedder()
