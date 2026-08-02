from google import genai

from chat_history import ChatHistory
from tools import get_weather, calculator, get_time


def get_tools():
    return [
        {
            "function_declarations": [
                {
                    "name": "get_weather",
                    "description": "Get weather information for a city",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "city": {"type": "STRING", "description": "City name"}
                        },
                        "required": ["city"],
                    },
                },
                {
                    "name": "calculator",
                    "description": "Evaluate a mathematical expression and return the calculated result. "
                    "Use this tool when the user asks to perform arithmetic calculations "
                    "or solve a numeric expression.",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {"expression": {"type": "STRING"}},
                        "required": ["expression"],
                    },
                },
                {
                    "name": "get_time",
                    "description": "Get the current local time for a city. ",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {"city": {"type": "STRING"}},
                        "required": ["city"],
                    },
                },
            ]
        }
    ]


class ChatEngine:
    def __init__(
        self, api_key, model, system_prompt=None, tool_registry=None, history=None
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt
        self.tool_registry = tool_registry
        self.history = history if history is not None else ChatHistory()

    def execute_tool(self, name, args):
        return self.tool_registry.execute(name, args)

    def chat(self, message):
        self.history.add_message("user", message)

        response = self.client.models.generate_content(
            model=self.model,
            contents=self.history.get_messages(),
            config={"tools": self.tool_registry, "system_instruction": self.system_prompt},
        )

        candidate = response.candidates[0]

        # Check if Gemini wants a tool call
        content = candidate.content
        self.history.add_content(content)

        for part in content.parts:
            if part.function_call:
                tool_call = part.function_call
                result = self.execute_tool(tool_call.name, tool_call.args)
                self.history.add_function_response(name=tool_call.name, result=result)

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=self.history.get_messages(),
                    config={
                        "tools": get_tools(),
                        "system_instruction": self.system_prompt,
                    },
                )

                # Normal response
                answer = response.text

                self.history.add_message("model", answer)

            return answer

        answer = response.text

        self.history.add_message("model", answer)

        return answer
