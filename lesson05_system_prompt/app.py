from chat_engine import ChatEngine
from chat_history import ChatHistory
from config import GEMINI_API_KEY

model="gemini-2.5-flash-lite"

def main():
    history = ChatHistory()
    engine = ChatEngine(api_key=GEMINI_API_KEY, model=model, history=history)

    while True:
        msg = input("User: ").strip().lower()
        if msg == "exit":
            print("Chat finished")
            break
        if msg:
            print(f"Model: {engine.chat(msg)}")

if __name__ == "__main__":
    main()