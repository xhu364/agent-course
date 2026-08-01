from google import genai

from chat_history import ChatHistory
from prompts import DEFAULT_SYSTEM_PROMPT


class ChatEngine:

    def __init__(self, api_key, model, history, system_prompt=DEFAULT_SYSTEM_PROMPT):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.history = history
        self.system_prompt = system_prompt

    def chat(self, user_message):

        self.history.add_message("user", user_message)

        response = self.client.models.generate_content(
            model=self.model,
            contents=self.history.get_messages(),
            config={
                "system_instruction": self.system_prompt
            }
        )

        answer = response.text

        self.history.add_message("model", answer)

        return answer