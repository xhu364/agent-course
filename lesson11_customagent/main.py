from llm import create_llm
from prompts import get_prompt
from langchain_classic.agents import AgentExecutor
from custom_agent import CustomAgent
from tools import calculator, get_weather, get_time, get_wikipedia_tool

tools = [calculator, get_weather, get_time, get_wikipedia_tool()]

llm = create_llm("gemini")

agent = CustomAgent(
    llm=llm,
    tools=tools,
)

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    response = agent.invoke("123", user_input)
    print("Assistant:", response)
print("finished")
