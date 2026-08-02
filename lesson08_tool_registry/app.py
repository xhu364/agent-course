from chat_engine import ChatEngine
from config import GEMINI_API_KEY
from tool_registry import ToolRegistry
from tools import get_time, get_weather, calculator

tool_registry = ToolRegistry()
tool_registry.register("get_time", get_time)
tool_registry.register("get_weather", get_weather)
tool_registry.register("calculator", calculator)

engine = ChatEngine(
    api_key=GEMINI_API_KEY, model="gemini-2.5-flash-lite", tool_registry=tool_registry
)


print(
    engine.chat(
        # "What is the weather in Boston now?"
        # "What is value for (2*3*4*5.2)"
        "what is the local time in Boston"
    )
)
