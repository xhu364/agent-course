from llm import create_llm
from graph import Conversation

conversation = Conversation(create_llm())

result = conversation.app.invoke(
    {
        "question": "What is weather in Boston today?",
        "attempts": 0,
        "score": 0,
        "feedback": "",
    }
)
print(result)
