import os
import warnings
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore")
try:
    from langchain_core._api.deprecation import LangChainDeprecationWarning
    warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
except Exception:
    pass

from pathlib import Path

class Config:
    # Ollama settings
    OLLAMA_BASE_URL = "http://localhost:11434"
    EMBED_MODEL = "nomic-embed-text"
    LLM_MODEL = "llama3"

    # Vector database
    PERSIST_DIR = Path("./wiki_vector_db")
    COLLECTION_NAME = "wiki_collection"

    # Chunking settings
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 100

    # Retrieval settings
    TOP_K_RESULTS = 3

    # LLM settings
    LLM_TEMPERATURE = 0.3
    LLM_TOP_P = 0.9
    LLM_REPEAT_PENALTY = 1.1

    # Default Wikipedia topics
    DEFAULT_TOPICS = [
        "Python (programming language)",
        "Machine learning",
        "Deep learning",
        "Natural language processing",
        "Artificial intelligence",
        "Neural network",
        "Large language model",
        "Data science",
    ]

config = Config()
