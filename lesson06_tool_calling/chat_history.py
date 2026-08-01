from google.genai.types import Content, Part, FunctionResponse


class ChatHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, text):
        self.messages.append(
            Content(
                role=role,
                parts=[Part(text=text)],
            )
        )

    def add_content(self, content):
        """
        Store Gemini generated Content directly.
        Used for function_call responses.
        """
        self.messages.append(content)

    def add_function_response(self, name, result):
        """
        Store tool execution result as function_response.
        """
        self.messages.append(
            Content(
                role="user",
                parts=[
                    Part(
                        function_response=FunctionResponse(
                            name=name,
                            response={"result": str(result)},
                        )
                    )
                ],
            )
        )

    def get_messages(self):
        return self.messages
