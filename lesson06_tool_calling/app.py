from chat_engine import ChatEngine
from chat_history import ChatHistory
from tools import get_tools
from agent import Agent
from config import GEMINI_API_KEY

engine = ChatEngine(
    api_key=GEMINI_API_KEY, model="gemini-2.5-flash-lite", tool_registry=get_tools()
)

agent = Agent(engine)

history = ChatHistory()

answer = agent.run("What is the weather and time in Boston?", history)

print(answer)
