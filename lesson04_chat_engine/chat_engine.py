from google import genai

from chat_history import ChatHistory


class ChatEngine:

    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.history = ChatHistory()

    def chat(self, user_message):

        self.history.add_user(user_message)

        response = self.client.models.generate_content(
            model=self.model,
            contents=self.history.get_messages()
        )

        answer = response.text

        self.history.add_assistant(answer)

        return answer