from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from llm import create_llm
from tools import calculator, get_weather
from prompt import SYSTEM_PROMPT

llm = create_llm("gemini")

tools = [
    calculator,
    get_weather,
]

llm_with_tools = llm.bind_tools(tools)


question = "What is 123 * 456? and What is temperature in Boston today"

messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=question),
]

while True:
    ai = llm_with_tools.invoke(messages)
    messages.append(ai)
    if not ai.tool_calls:
        break
    for tool_call in ai.tool_calls:
        name = tool_call["name"]
        args = tool_call["args"]
        tool = next(t for t in tools if t.name == name)
        tool_result = tool.invoke(args)
        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"],
            )
        )
        messages.append(tool_result)

answer = messages[-1].content
print(answer)
