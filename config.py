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
    LLM_MODEL = "llama3.2:1b"
    OLLAMA_KEEP_ALIVE = -1  # Keep model resident in RAM to avoid reload delays
    OLLAMA_NUM_THREADS = 8  # Optimal multi-threading for this 12-core CPU
    OLLAMA_NUM_CTX = 1024   # Low context window for minimum KV cache overhead

    # Vector database
    PERSIST_DIR = Path("./wiki_vector_db")
    COLLECTION_NAME = "wiki_collection"

    # Chunking settings (smaller chunks = faster embedding and leaner context)
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

    # Retrieval settings (top 2 chunks is optimal for speed and precision)
    TOP_K_RESULTS = 2
    MAX_CONTEXT_CHARS = 1000

    # LLM settings
    LLM_TEMPERATURE = 0.1
    LLM_TOP_P = 0.9
    LLM_REPEAT_PENALTY = 1.1
    LLM_NUM_PREDICT = 90  # Cap output tokens for fast, concise 1-3 sentence answers

    # Comprehensive Offline RAG Topics
    DEFAULT_TOPICS = [
        # Original 8 Core Topics
        "Python (programming language)",
        "Machine learning",
        "Deep learning",
        "Natural language processing",
        "Artificial intelligence",
        "Neural network",
        "Large language model",
        "Data science",
        # DSA
        "Data structure",
        "Algorithm",
        "Tree (data structure)",
        "Graph (abstract data type)",
        # Databases & Cloud
        "Database",
        "Relational database",
        "NoSQL",
        "Cloud computing",
        # Advanced AI, RAG & Agents
        "Retrieval-augmented generation",
        "Intelligent agent",
        "Multi-agent system",
        "Prompt engineering",
        # Security & Ethical Hacking
        "Computer security",
        "White hat (computer security)",
        # Frontend, Web & Modern Stacks
        "HTML",
        "CSS",
        "JavaScript",
        "React (software)",
        "Node.js",
        "Bootstrap (front-end framework)",
        "Three.js",
        "User interface design",
        "User experience",
        # 3D Software
        "Blender (software)",
    ]

config = Config()
