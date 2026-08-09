from llm import create_llm
from graph import Conversation

conversation = Conversation(create_llm())

result = conversation.app.invoke({"question": "What is Python?", "attempts": 0})
print(result)
