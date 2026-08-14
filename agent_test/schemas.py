from pydantic import BaseModel


class ChatRequest(BaseModel):
    role: str
    message: str


class ChatResponse(BaseModel):
    reply: str


class ThreadCreateResponse(BaseModel):
    thread_id: str
