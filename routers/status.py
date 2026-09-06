from fastapi import APIRouter
from models.schemas import StatusResponse, HealthCheck
from services.embedder import embedder
from config import config
from datetime import datetime
import httpx

router = APIRouter(prefix="/status", tags=["Status"])

@router.get("/", response_model=StatusResponse)
async def get_status():
    """Get the current status of all services."""
    # Check Ollama connection
    ollama_connected = False
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{config.OLLAMA_BASE_URL}/api/tags",
                timeout=5.0
            )
            ollama_connected = response.status_code == 200
    except Exception:
        ollama_connected = False

    # Get vector store stats
    stats = embedder.get_stats()

    return StatusResponse(
        status="ready" if stats["total_chunks"] > 0 else "needs_build",
        vector_db_ready=stats["total_chunks"] > 0,
        ollama_connected=ollama_connected,
        model_loaded=config.LLM_MODEL,
        embed_model_loaded=config.EMBED_MODEL,
        total_chunks=stats["total_chunks"],
        topics_count=stats["topics_count"]
    )


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Simple health check endpoint."""
    return HealthCheck(status="healthy", timestamp=datetime.now())
