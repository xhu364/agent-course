from google import genai

from chat_history import ChatHistory
from chat_engine import ChatEngine
from tools import get_weather, calculator, get_time


class Agent:
    def __init__(self, engine: ChatEngine):
        self.engine = engine

    def execute_tool(self, name, args):

        if name == "get_weather":
            return get_weather(args["city"])

        if name == "calculator":
            return calculator(args["expression"])

        if name == "get_time":
            return get_time(args["city"])

        raise ValueError(f"Unknown tool {name}")

    def run(self, message, history):
        history.add_message("user", message)

        content = self.engine.generate(history)

        history.add_content(content)

        print(f"xxx {content}")

        for part in content.parts:
            if part.function_call:
                tool_call = part.function_call
                result = self.execute_tool(tool_call.name, tool_call.args)
                history.add_function_response(name=tool_call.name, result=result)

                response = self.engine.generate(history)
                print(f"yyy {response}")
                answer = response.text

                history.add_message("model", answer)

            return answer

        answer = response.text

        history.add_message("model", answer)

        return answer
