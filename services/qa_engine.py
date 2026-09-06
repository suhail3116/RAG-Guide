import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

try:
    from langchain.chains import RetrievalQA
except (ImportError, ModuleNotFoundError):
    from langchain_classic.chains import RetrievalQA

from langchain_community.llms import Ollama
try:
    from langchain_core.callbacks import StreamingStdOutCallbackHandler
except ImportError:
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from typing import Optional, Dict, List
from config import config
from services.embedder import embedder

class QAEngine:
    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.llm = Ollama(
                model=config.LLM_MODEL,
                base_url=config.OLLAMA_BASE_URL,
                temperature=config.LLM_TEMPERATURE,
                top_p=config.LLM_TOP_P,
                repeat_penalty=config.LLM_REPEAT_PENALTY
            )
        self.chain: Optional[RetrievalQA] = None
        self._current_top_k: int = config.TOP_K_RESULTS
        self._build_chain(top_k=self._current_top_k)

    def _build_chain(self, top_k: int = 3):
        """Build the QA retrieval chain."""
        try:
            retriever = embedder.get_retriever(top_k=top_k)
            self.chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                verbose=False
            )
            self._current_top_k = top_k
        except Exception as e:
            self.chain = None

    def query(self, question: str, top_k: int = 3) -> Dict:
        """Query the chatbot and return answer with sources."""
        if not self.chain or top_k != self._current_top_k:
            self._build_chain(top_k)

        if not self.chain:
            raise ValueError("Vector store not ready. Please build the index first via POST /topics/build")

        # Invoke chain with auto-recovery if vectorstore collection was out of sync
        try:
            if hasattr(self.chain, "invoke"):
                result = self.chain.invoke({"query": question})
            else:
                result = self.chain({"query": question})
        except Exception as e:
            err_msg = str(e).lower()
            if "collection" in err_msg or "does not exist" in err_msg:
                print(f"[RECOVER] Rebuilding QA chain due to collection sync: {e}")
                self._build_chain(top_k)
                if not self.chain:
                    raise e
                if hasattr(self.chain, "invoke"):
                    result = self.chain.invoke({"query": question})
                else:
                    result = self.chain({"query": question})
            else:
                raise e

        # Parse source documents
        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "source": doc.metadata.get("title", "Unknown"),
                "chunk_preview": doc.page_content[:200] + "...",
                "url": doc.metadata.get("url", "")
            })

        return {
            "answer": result.get("result", ""),
            "sources": sources
        }

# Singleton
qa_engine = QAEngine()
