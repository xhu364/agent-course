from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)


class SingleAgent:
    """
    Minimal agent implementation.

    Responsibilities:
    - Maintain conversation history
    - Call the LLM
    - Execute requested tools
    - Feed tool results back to the LLM
    - Stop after a maximum number of iterations
    """

    def __init__(
        self,
        llm: BaseChatModel,
        tools: list[Any] | None = None,
        system_prompt: str = "You are a helpful assistant.",
        max_iterations: int = 5,
    ):
        self.llm = llm
        self.tools = tools or []
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations

        self.tool_map = {
            tool.name: tool
            for tool in self.tools
        }

        self.history: list[BaseMessage] = []

        if self.tools:
            self.llm_with_tools = self.llm.bind_tools(self.tools)
        else:
            self.llm_with_tools = self.llm

    def run(self, user_message: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            *self.history,
            HumanMessage(content=user_message),
        ]

        for _ in range(self.max_iterations):
            response: AIMessage = self.llm_with_tools.invoke(messages)

            messages.append(response)

            # No tool call = final answer.
            if not response.tool_calls:
                self.history.extend(
                    [
                        HumanMessage(content=user_message),
                        response,
                    ]
                )

                return self._extract_text(response.content)

            # Execute all requested tools.
            for tool_call in response.tool_calls:
                result = self._execute_tool(tool_call)
                messages.append(result)

        raise RuntimeError(
            f"Agent exceeded maximum iterations: "
            f"{self.max_iterations}"
        )

    def _execute_tool(self, tool_call: dict[str, Any]) -> ToolMessage:
        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})

        tool = self.tool_map.get(tool_name)

        if tool is None:
            return ToolMessage(
                content=f"Unknown tool: {tool_name}",
                tool_call_id=tool_call["id"],
            )

        try:
            result = tool.invoke(tool_args)

            return ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )

        except Exception as exc:
            return ToolMessage(
                content=f"Tool failed: {exc}",
                tool_call_id=tool_call["id"],
            )

    @staticmethod
    def _extract_text(content: Any) -> str:
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []

            for item in content:
                if isinstance(item, str):
                    parts.append(item)

                elif isinstance(item, dict):
                    if "text" in item:
                        parts.append(item["text"])

            return "".join(parts)

        return str(content)

    def clear_history(self):
        self.history.clear()
