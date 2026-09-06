try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except (ImportError, ModuleNotFoundError):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from langchain_core.documents import Document
except (ImportError, ModuleNotFoundError):
    from langchain.schema import Document

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List, Dict, Optional
from config import config
import shutil
import os

class Embedder:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=config.EMBED_MODEL,
            base_url=config.OLLAMA_BASE_URL
        )
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
