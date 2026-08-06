from llm import create_llm
from prompts import get_prompt
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from tools import *

tool_used = ToolRegister()

tool_used.register(get_wikipedia_tool())
tool_used.register(get_time)
tool_used.register(get_weather)
tool_used.register(calculator)


tools = tool_used.get_tools()


agent = create_tool_calling_agent(
    llm=create_llm(),
    tools=tools,
    prompt=get_prompt(),
)


agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = agent_executor.invoke({"input": user_input})

    print("Assistant:", result["output"])
