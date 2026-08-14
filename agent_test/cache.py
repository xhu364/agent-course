import uuid
from typing import Dict, List, Tuple
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage


class ChatCache:
    def __init__(self):
        # thread_id -> list of (role, message)
        self._threads: Dict[str, List[Tuple[str, str]]] = {}

    def create_thread(self) -> str:
        thread_id = uuid.uuid4().hex
        self._threads[thread_id] = []
        return thread_id

    def exists(self, thread_id: str) -> bool:
        return thread_id in self._threads

    def add_message(self, thread_id: str, role: str, message: str) -> None:
        if thread_id not in self._threads:
            raise KeyError("thread not found")
        self._threads[thread_id].append((role, message))

    def get_messages(self, thread_id: str):
        return list(self._threads.get(thread_id, []))

    def tuples_to_messages(self, history: List[Tuple[str, str]]) -> List[BaseMessage]:
        """Convert a list of (role, message) tuples to LangChain `BaseMessage` objects.

        Roles map to message classes as follows: `user` -> `HumanMessage`,
        `assistant` -> `AIMessage`, `system` -> `SystemMessage`.
        """
        mapping = {"user": HumanMessage, "assistant": AIMessage, "system": SystemMessage}
        msgs: List[BaseMessage] = []
        for role, text in history:
            cls = mapping.get(role, HumanMessage)
            msgs.append(cls(content=text))
        return msgs

    def get_messages_as_base(self, thread_id: str) -> List[BaseMessage]:
        """Get the stored messages for `thread_id` as a list of `BaseMessage`.

        Raises `KeyError` if the thread does not exist.
        """
        if not self.exists(thread_id):
            raise KeyError("thread not found")
        history = self.get_messages(thread_id)
        return self.tuples_to_messages(history)
