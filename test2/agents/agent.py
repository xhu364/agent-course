from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Union

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage


@dataclass
class ToolSpec:
    name: str
    func: Callable[..., Any]
    description: str = ""
    args_schema: Optional[Any] = None


class SingleAgent:
    """Minimal single-agent loop with explicit tool execution and chat history."""

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Optional[Sequence[Union[Callable[..., Any], ToolSpec]]] = None,
        system_prompt: str = "You are a helpful assistant.",
        max_iterations: int = 5,
    ) -> None:
        self.llm = llm
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.chat_history: List[BaseMessage] = [SystemMessage(content=system_prompt)]
        self.tool_map: Dict[str, Callable[..., Any]] = {}
        self.tool_specs: List[ToolSpec] = []

        for tool_obj in tools or []:
            self.add_tool(tool_obj)

        self.llm_with_tools = self.llm.bind_tools(
            [
                {
                    "name": spec.name,
                    "description": spec.description,
                    "parameters": spec.args_schema.model_json_schema() if spec.args_schema else {"type": "object", "properties": {}},
                }
                for spec in self.tool_specs
            ]
        ) if self.tool_specs else self.llm

    def add_tool(self, tool_obj: Union[Callable[..., Any], ToolSpec]) -> None:
        if isinstance(tool_obj, ToolSpec):
            spec = tool_obj
        else:
            name = getattr(tool_obj, "__name__", tool_obj.__class__.__name__)
            description = getattr(tool_obj, "__doc__", "") or ""
            spec = ToolSpec(name=name, func=tool_obj, description=description)

        self.tool_map[spec.name] = spec.func
        self.tool_specs.append(spec)

        if self.tool_specs:
            self.llm_with_tools = self.llm.bind_tools(
                [
                    {
                        "name": s.name,
                        "description": s.description,
                        "parameters": s.args_schema.model_json_schema() if s.args_schema else {"type": "object", "properties": {}},
                    }
                    for s in self.tool_specs
                ]
            )

    def run(self, user_input: str) -> str:
        self.chat_history.append(HumanMessage(content=user_input))

        for _ in range(self.max_iterations):
            response = self.llm_with_tools.invoke(self.chat_history)
            self.chat_history.append(response)

            tool_calls = getattr(response, "tool_calls", None) or []
            if not tool_calls:
                return self._extract_text(response)

            for tool_call in tool_calls:
                name = tool_call.get("name")
                arguments = tool_call.get("args", {}) or {}
                tool_id = tool_call.get("id")

                if name is None or name not in self.tool_map:
                    raise ValueError(f"Unsupported tool call: {tool_call}")

                result = self.tool_map[name](**arguments)
                self.chat_history.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_id or f"call_{name}",
                        name=name,
                    )
                )

        raise RuntimeError("Exceeded maximum tool-call iterations without final answer.")

    @staticmethod
    def _extract_text(message: BaseMessage) -> str:
        if isinstance(message, AIMessage):
            return message.content if isinstance(message.content, str) else str(message.content)
        return str(message.content)


if __name__ == "__main__":
    # Example usage:
    # pip install langchain-google-genai langchain-ollama
    # from langchain_google_genai import ChatGoogleGenerativeAI
    # from langchain_ollama import ChatOllama
    # llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    # llm = ChatOllama(model="llama3.1")

    def get_weather(city: str) -> str:
        """Return a simple mock weather result for a city."""
        return f"The weather in {city} is sunny and 23C."

    # Replace this with your actual provider-specific model adapter.
    # Example: llm = ChatOllama(model="llama3.1")
    # agent = SingleAgent(llm=llm, tools=[get_weather], system_prompt="You are a helpful weather assistant.")
    # print(agent.run("What's the weather in Paris?"))

    print("SingleAgent is ready. Configure llm = ChatGoogleGenerativeAI(...) or ChatOllama(...).")
