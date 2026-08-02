from google import genai
from google.genai.types import Content

from chat_history import ChatHistory
from tools import get_tools
from tools import get_weather, calculator, get_time


class ChatEngine:
    def __init__(self, api_key, model, system_prompt=None, tool_registry=None):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt
        self.tool_registry = tool_registry or get_tools()

    def generate(self, history):
        response = self.client.models.generate_content(
            model=self.model,
            contents=history.get_messages(),
            config={
                "tools": self.tool_registry,
                "system_instruction": self.system_prompt,
            },
        )
        return response.candidates[0].content

    @staticmethod
    def extract(content: Content):
        text = []
        for part in content.parts:
            if part.text:
                text.append(part.text)
        return "".join(text)
