"""Simple LLMAgent wrapper for LangChain chat models.

Provides a synchronous `invoke` method which accepts a list of
`langchain.schema.BaseMessage` objects and returns the assistant reply
as a string. Also includes `invoke_from_tuples` convenience method that
accepts a list of `(role, message)` tuples.

This keeps the interface small for interview/demo use; for production you
may want async support, retries, streaming, and stronger type handling.
"""
from typing import List, Tuple, Optional
from cache import ChatCache

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage


class LLMAgent:
    """Light-weight LangChain-based LLM agent.

    Args:
        llm: Optional LangChain chat model instance. If omitted the class
            will attempt to construct `ChatOpenAI(temperature=0)`.
    """

    def __init__(self, llm, cache: Optional[ChatCache] = None):
        self._llm = llm

        self.cache = cache

    def chat(self, thread_id: str, role: str, message: str) -> str:
        """Add a message to the `thread_id`, call the LLM with full history, store assistant reply, and return it.

        Requires `self.cache` to be set (inject a `ChatCache` instance via `with_cache`).
        """
        if self.cache is None:
            raise RuntimeError("ChatCache not attached to LLMAgent")

        if not self.cache.exists(thread_id):
            raise KeyError("thread not found")

        self.cache.add_message(thread_id, role, message)
        msgs = self.cache.get_messages_as_base(thread_id)
        reply = self.invoke(msgs)
        self.cache.add_message(thread_id, "assistant", reply)
        return reply

    def invoke(self, messages: List[BaseMessage]) -> str:
        """Invoke the LLM with a list of `BaseMessage` and return text reply.

        This method tolerates a few common return shapes from LangChain
        chat models and falls back to a simple echo if no model is available.
        """
        if not messages:
            return ""

        result = self._llm.invoke(messages)
        return result.content if hasattr(result, "content") else str(result)

    def invoke_from_tuples(self, history: List[Tuple[str, str]]) -> str:
        """Convert (role, message) tuples to `BaseMessage` then invoke.

        Roles: `user` -> `HumanMessage`, `assistant` -> `AIMessage`, `system` -> `SystemMessage`.
        """
        mapping = {}
        if HumanMessage is not None:
            mapping = {"user": HumanMessage, "assistant": AIMessage, "system": SystemMessage}

        msgs: List[BaseMessage] = []
        for role, text in history:
            cls = mapping.get(role) if mapping else None
            if cls:
                msgs.append(cls(content=text))  # type: ignore[arg-type]
            else:
                # fallback to a simple object with `content` attribute
                class _M:
                    def __init__(self, content):
                        self.content = content

                msgs.append(_M(text))  # type: ignore[arg-type]

        return self.invoke(msgs)
