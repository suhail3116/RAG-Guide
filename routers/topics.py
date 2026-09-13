from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import (
    AddTopicsRequest, RefreshRequest, TopicsResponse,
    TopicInfo, MessageResponse
)
from services.fetcher import fetcher
from services.embedder import embedder
from services.qa_engine import qa_engine
from config import config

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.post("/build", response_model=MessageResponse)
async def build_index(background_tasks: BackgroundTasks):
    """
    Build the vector index from default Wikipedia topics.

    Runs in background to avoid timeout.
    """
    def _build():
        print("Fetching Wikipedia articles...")
        documents = fetcher.fetch_multiple(config.DEFAULT_TOPICS)
        from services.curated_docs import get_curated_documents
        for c in get_curated_documents():
            documents.append({
                "title": c["title"],
                "page_content": c["full_text"],
                "summary": c["full_text"][:400],
                "full_text": c["full_text"],
                "url": c["url"],
                "categories": c.get("categories", []),
                "length": len(c["full_text"])
            })
        print(f"Building index from {len(documents)} documents...")
        embedder.build_index(documents)
        qa_engine._build_chain()
        print("Index build complete!")

    background_tasks.add_task(_build)

    return MessageResponse(
        message="Index building started in background...",
        success=True
    )


@router.post("/add", response_model=MessageResponse)
async def add_topics(request: AddTopicsRequest, background_tasks: BackgroundTasks):
    """
    Add new Wikipedia topics to the existing index.

    Topics are fetched and embedded in the background.
    """
    def _add():
        print(f"Adding topics: {request.topics}")
        documents = fetcher.fetch_multiple(request.topics)
        if documents:
            embedder.add_documents(documents)
            qa_engine._build_chain()
        print("Topics added successfully!")

    background_tasks.add_task(_add)

    return MessageResponse(
        message=f"Adding {len(request.topics)} topics in background...",
        success=True
    )


@router.get("/list", response_model=TopicsResponse)
async def list_topics():
    """List all indexed topics and their chunk counts."""
    stats = embedder.get_stats()
    topics = [
        TopicInfo(name=t, chunks=0)
        for t in stats.get("topics", [])
    ]

    return TopicsResponse(
        topics=topics,
        total_chunks=stats.get("total_chunks", 0)
    )


@router.post("/refresh", response_model=MessageResponse)
async def refresh_index(request: RefreshRequest, background_tasks: BackgroundTasks):
    """
    Refresh the entire index with optional specific topics.

    If topics are provided, only those are refreshed.
    """
    topics = request.topics or config.DEFAULT_TOPICS

    def _refresh():
        print(f"Refreshing index with topics: {topics}")
        documents = fetcher.fetch_multiple(topics)
        embedder.build_index(documents)
        qa_engine._build_chain()
        print("Refresh complete!")

    background_tasks.add_task(_refresh)

    return MessageResponse(
        message=f"Refreshing {len(topics)} topics in background...",
        success=True
    )


@router.post("/search")
async def search_wikipedia(query: str, limit: int = 5):
    """
    Search Wikipedia for topics matching a query.

    Returns potential topic names that can be added.
    """
    results = fetcher.search(query, limit=limit)
    return {"query": query, "results": results}
