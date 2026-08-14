from fastapi import FastAPI, HTTPException
import uvicorn

from cache import ChatCache
from schemas import ChatRequest, ChatResponse, ThreadCreateResponse
from llm_agent import LLMAgent
from llm import create_llm

app = FastAPI()
cache = ChatCache()
llm_agent = LLMAgent(llm=create_llm(), cache=cache)


@app.post("/chat/{thread_id}/message", response_model=ChatResponse)
def post_message(thread_id: str, req: ChatRequest):
    """Post a message to an existing thread and return assistant reply."""
    try:
        reply = llm_agent.chat(thread_id, req.role, req.message)
    except KeyError:
        raise HTTPException(status_code=404, detail="thread not found")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"reply": reply}


@app.post("/chat/threads", response_model=ThreadCreateResponse)
def post_messages():
    """Create a new thread, post the provided message, and return thread id."""
    thread_id = cache.create_thread()
    return {"thread_id": thread_id}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")
