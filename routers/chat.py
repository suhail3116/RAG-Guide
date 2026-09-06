from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import ChatRequest, ChatResponse, SourceDocument
from services.qa_engine import qa_engine
from config import config
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Ask a question to the Wikipedia chatbot.

    The bot will search the indexed Wikipedia articles and
    generate an answer based on the retrieved context.
    """
    try:
        result = qa_engine.query(
            question=request.query,
            top_k=request.top_k
        )

        return ChatResponse(
            answer=result["answer"],
            sources=[
                SourceDocument(
                    source=s["source"],
                    chunk_preview=s["chunk_preview"],
                    url=s.get("url")
                )
                for s in result["sources"]
            ],
            query=request.query,
            model=config.LLM_MODEL,
            timestamp=datetime.now()
        )

    except ValueError as e:
        raise HTTPException(
            status_code=503,
            detail="Vector store not ready. Please build the index first via POST /topics/build"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream the chatbot response (returns Server-Sent Events).

    Use this endpoint for real-time streaming responses.
    """
    from fastapi.responses import StreamingResponse

    async def event_generator():
        try:
            result = qa_engine.query(request.query, top_k=request.top_k)
            yield f"data: {result['answer']}\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
