from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, topics, status
from config import config
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Wikipedia Chatbot API",
    description="""
## Local Wikipedia Chatbot API

Retrieval-Augmented Generation (RAG) service powered by Wikipedia articles, ChromaDB, and local Ollama models.

### Features:
* **Chat**: Query the indexed knowledge base using an Ollama LLM (`/chat`, `/chat/stream`)
* **Topics**: Fetch, chunk, embed, and manage indexed Wikipedia topics (`/topics/build`, `/topics/add`, `/topics/list`, `/topics/refresh`, `/topics/search`)
* **Status**: Service diagnostic and connectivity check (`/status`, `/status/health`)
""",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(topics.router)
app.include_router(status.router)

@app.get("/", tags=["General"])
async def root():
    """Root endpoint with documentation links and API info."""
    return {
        "message": "Wikipedia Chatbot API is online",
        "docs_url": "/docs",
        "status_url": "/status",
        "health_url": "/status/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
