from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
)


class CustomAgent:

    def __init__(self, llm, tools):
        self.llm = llm.bind_tools(tools)
        self.tools = {tool.name: tool for tool in tools}
        self.sessions = {}

    def invoke(self, session_id, question):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        messages = self.sessions[session_id]

        messages.append(HumanMessage(content=question))

        while True:
            response = self.llm.invoke(messages)
            if not response.tool_calls:
                messages.append(response)
                return response.content
            messages.append(response)
            for tool_call in response.tool_calls:
                name = tool_call["name"]
                args = tool_call["args"]
                id = tool_call["id"]
                tool = self.tools[name]
                tool_result = tool.invoke(args)
                messages.append(ToolMessage(content=str(tool_result), tool_call_id=id))
