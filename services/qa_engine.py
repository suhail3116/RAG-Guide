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
from langchain_core.prompts import PromptTemplate
from typing import Optional, Dict, List, Generator, Tuple
import json
import httpx
from config import config
from services.embedder import embedder

# Ultra-fast, concise prompt template for both questions and topic summaries
QA_PROMPT = PromptTemplate(
    template="""You are a helpful assistant. Use the provided Wikipedia context to answer the question or summarize the topic in 1-3 direct, concise sentences. Do not add conversational filler. If the context does not contain relevant information, say you do not have enough information.

Context:
{context}

Query: {question}
Answer:""",
    input_variables=["context", "question"]
)

class QAEngine:
    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Auto-detect available fast model with fallback
            model_to_use = getattr(config, "LLM_MODEL", "llama3.2:1b")
            try:
                import httpx
                resp = httpx.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=1.5)
                if resp.status_code == 200:
                    available = [m.get("name") for m in resp.json().get("models", [])]
                    # If preferred model is not yet available, fallback gracefully
                    if not any(model_to_use in m for m in available):
                        for fallback in ["llama3.2:1b", "llama3.2", "llama3:latest", "llama3"]:
                            if any(fallback in m for m in available):
                                model_to_use = fallback
                                break
            except Exception:
                pass

            self.active_model = model_to_use
            self.llm = Ollama(
                model=model_to_use,
                base_url=config.OLLAMA_BASE_URL,
                temperature=config.LLM_TEMPERATURE,
                top_p=config.LLM_TOP_P,
                repeat_penalty=config.LLM_REPEAT_PENALTY,
                keep_alive=getattr(config, "OLLAMA_KEEP_ALIVE", -1)
            )
        self.chain: Optional[RetrievalQA] = None
        self._current_top_k: int = getattr(config, "TOP_K_RESULTS", 2)
        self._build_chain(top_k=self._current_top_k)

    def _build_chain(self, top_k: int = 2):
        """Build the QA retrieval chain with speed optimizations."""
        try:
            retriever = embedder.get_retriever(top_k=top_k)
            self.chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": QA_PROMPT},
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
                "url": doc.metadata.get("url", ""),
                "image_url": doc.metadata.get("image_url", "")
            })

        return {
            "answer": result.get("result", ""),
            "sources": sources
        }

    def stream_query(self, question: str, top_k: int = 2) -> Generator[Tuple[str, Optional[List[Dict]]], None, None]:
        """
        Stream answer tokens one-by-one in real time directly from Ollama.
        Yields (token, None) for each generated token, and finally yields ("", sources).
        Provides sub-second perceived response latency.
        """
        if not embedder.vectorstore:
            embedder._init_vectorstore()

        if not embedder.vectorstore:
            raise ValueError("Vector store not ready. Please build the index first via /build or POST /topics/build")

        # 1. Retrieve top relevant documents
        try:
            docs = embedder.vectorstore.similarity_search(question, k=top_k)
        except Exception as e:
            embedder._init_vectorstore()
            if not embedder.vectorstore:
                raise ValueError("Vector store not ready. Please build the index first via /build")
            docs = embedder.vectorstore.similarity_search(question, k=top_k)

        # 2. Context preparation & bounded size to prevent prompt processing lag
        context_snippets = []
        sources = []
        total_chars = 0
        max_chars = getattr(config, "MAX_CONTEXT_CHARS", 1200)

        for doc in docs:
            snippet = doc.page_content.strip()
            if total_chars + len(snippet) > max_chars:
                remaining = max(0, max_chars - total_chars)
                if remaining > 80:
                    context_snippets.append(snippet[:remaining] + "...")
                break
            context_snippets.append(snippet)
            total_chars += len(snippet)
            sources.append({
                "source": doc.metadata.get("title", "Wikipedia"),
                "chunk_preview": doc.page_content[:200] + "...",
                "url": doc.metadata.get("url", ""),
                "image_url": doc.metadata.get("image_url", "")
            })

        if not sources and docs:
            sources.append({
                "source": docs[0].metadata.get("title", "Wikipedia"),
                "chunk_preview": docs[0].page_content[:200] + "...",
                "url": docs[0].metadata.get("url", ""),
                "image_url": docs[0].metadata.get("image_url", "")
            })

        combined_context = "\n\n".join(context_snippets)
        prompt_text = QA_PROMPT.format(context=combined_context, question=question)

        # Check fast model availability
        model_to_use = getattr(config, "LLM_MODEL", "llama3.2:1b")
        try:
            tag_resp = httpx.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=1.5)
            if tag_resp.status_code == 200:
                available = [m.get("name", "") for m in tag_resp.json().get("models", [])]
                if not any(model_to_use in m for m in available):
                    for fallback in ["llama3.2:1b", "llama3.2", "llama3:latest", "llama3"]:
                        if any(fallback in m for m in available):
                            model_to_use = fallback
                            break
        except Exception:
            pass

        self.active_model = model_to_use

        payload = {
            "model": model_to_use,
            "prompt": prompt_text,
            "stream": True,
            "keep_alive": getattr(config, "OLLAMA_KEEP_ALIVE", -1),
            "options": {
                "temperature": config.LLM_TEMPERATURE,
                "top_p": config.LLM_TOP_P,
                "repeat_penalty": config.LLM_REPEAT_PENALTY,
                "num_predict": getattr(config, "LLM_NUM_PREDICT", 90),
                "num_thread": getattr(config, "OLLAMA_NUM_THREADS", 8),
                "num_ctx": getattr(config, "OLLAMA_NUM_CTX", 1024)
            }
        }

        try:
            with httpx.stream(
                "POST",
                f"{config.OLLAMA_BASE_URL}/api/generate",
                json=payload,
                timeout=60.0
            ) as response:
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                        token = chunk.get("response", "")
                        if token:
                            yield (token, None)
                        if chunk.get("done", False):
                            break
                    except Exception:
                        continue

            # Final yield containing the sources
            yield ("", sources)

        except Exception as e:
            # Fallback to standard chain if streaming connection fails
            res = self.query(question, top_k=top_k)
            yield (res["answer"], res.get("sources", []))

# Singleton
qa_engine = QAEngine()
