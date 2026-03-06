from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from core.chat_engine import ChatEngine

router = APIRouter()

engine = ChatEngine("models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")


class ChatRequest(BaseModel):
    user_id: int
    message: str


@router.post("/chat/stream")
def chat_stream(req: ChatRequest):

    def generator():
        for token in engine.chat_stream(req.user_id, req.message):
            yield token

    return StreamingResponse(generator(), media_type="text/plain")
