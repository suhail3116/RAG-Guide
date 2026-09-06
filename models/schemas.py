from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ---- Request Models ----

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="User query")
    top_k: Optional[int] = Field(3, ge=1, le=10, description="Number of context chunks to retrieve")


class AddTopicsRequest(BaseModel):
    topics: List[str] = Field(..., min_items=1, description="List of Wikipedia topics to add")


class RemoveTopicRequest(BaseModel):
    topic: str = Field(..., description="Topic name to remove")


class RefreshRequest(BaseModel):
    topics: Optional[List[str]] = Field(None, description="Optional: specific topics to refresh")

# ---- Response Models ----

class SourceDocument(BaseModel):
    source: str
    chunk_preview: str
    url: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    query: str
    model: str
    timestamp: datetime = Field(default_factory=datetime.now)


class TopicInfo(BaseModel):
    name: str
    chunks: int
    last_updated: Optional[str] = None


class TopicsResponse(BaseModel):
    topics: List[TopicInfo]
    total_chunks: int


class StatusResponse(BaseModel):
    status: str
    vector_db_ready: bool
    ollama_connected: bool
    model_loaded: str
    embed_model_loaded: str
    total_chunks: int
    topics_count: int


class MessageResponse(BaseModel):
    message: str
    success: bool


class HealthCheck(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
