from chat_engine import ChatEngine
from config import GEMINI_API_KEY

engine = ChatEngine(
    api_key=GEMINI_API_KEY,
    model="gemini-2.5-flash-lite",
)


print(
    engine.chat(
        # "What is the weather in Boston now?"
        #"What is value for (2*3*4*5.2)"
        "what is the local time in Boston"
    )
)
