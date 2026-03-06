from fastapi import FastAPI

from core.chat_engine import ChatEngine
from api.chat import router as chat_router
from api.ws_chat import router as ws_router

# --------------------------------------------------
# Create LLM engine ONCE (global, shared)
# --------------------------------------------------
engine = ChatEngine(
    model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
)

# --------------------------------------------------
# FastAPI app
# --------------------------------------------------
app = FastAPI(
    title="Open-Source Streaming Chatbot",
    description="LLM streaming API using open-source models",
    version="1.0"
)

app.include_router(chat_router)
app.include_router(ws_router)


@app.get("/")
def health():
    return {"status": "running"}


# --------------------------------------------------
# 🔥 LLM Warm-up (CRITICAL)
# --------------------------------------------------
@app.on_event("startup")
def warmup_model():
    print("\n🔥 Warming up LLM (GPU / CUDA kernels)...")

    # tiny dummy prompt (NOT stored in memory)
    for _ in engine.chat_stream(
        user_id=0,          # reserved warm-up user
        user_input="hello"
    ):
        pass

    print("✅ LLM warm-up complete\n")
