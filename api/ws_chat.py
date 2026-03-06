import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from core.chat_engine import ChatEngine

router = APIRouter()

# ✅ SINGLE shared engine instance
engine = ChatEngine("models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket connected")

    try:
        while True:
            data = await websocket.receive_json()
            user_id = data["user_id"]
            message = data["message"]

            # 🔥 STREAM TOKENS LIVE
            async for chunk in stream_llm_live(user_id, message):
                await websocket.send_text(chunk)

            await websocket.send_text("__END__")

    except WebSocketDisconnect:
        print("❌ Client disconnected")
    except Exception as e:
        print("⚠️ WebSocket error:", e)


# =========================
# 🔑 TRUE LIVE STREAM (WORD BY WORD)
# =========================
async def stream_llm_live(user_id: int, message: str):
    """
    Runs llama.cpp generator in a background thread
    and streams output word-by-word.
    """

    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    def run_llm():
        buffer = ""
        for token in engine.chat_stream(user_id, message):
            buffer += token

            # Emit word-by-word
            while " " in buffer:
                word, buffer = buffer.split(" ", 1)
                loop.call_soon_threadsafe(queue.put_nowait, word + " ")

        if buffer:
            loop.call_soon_threadsafe(queue.put_nowait, buffer)

        loop.call_soon_threadsafe(queue.put_nowait, None)  # END

    # Run blocking LLM in background thread
    asyncio.create_task(asyncio.to_thread(run_llm))

    while True:
        item = await queue.get()
        if item is None:
            break
        yield item
        await asyncio.sleep(0)  # 🔥 flush to websocket
