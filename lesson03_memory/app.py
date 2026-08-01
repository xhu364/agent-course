from google import genai

from config import GEMINI_API_KEY
from chat_history import ChatHistory

MODEL_NAME = "gemini-2.5-flash-lite"


def main():
    client = genai.Client(api_key=GEMINI_API_KEY)

    history = ChatHistory()

    while True:
        user_input = input("You: ").strip()
        if user_input == "exit":
            print("exit chat")
            break

        history.add_user(user_input)

        response = client.models.generate_content(
            model=MODEL_NAME, contents=history.get_messages()
        )

        print(f"Assistant: {response.text}")

        history.add_assistant(response.text)

    print(history.get_messages())


if __name__ == "__main__":
    main()
