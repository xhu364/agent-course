from chat_engine import ChatEngine
from config import GEMINI_API_KEY

model = "gemini-2.5-flash-lite"

engine = ChatEngine(api_key=GEMINI_API_KEY, model=model)

messages = ["how are you", "My name is Mike H. Who are you?", "What is my name?"]

for msg in messages:
    print(f"User: {msg}")
    print(f"Model: {engine.chat(msg)}")
