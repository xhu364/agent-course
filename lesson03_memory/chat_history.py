class ChatHistory:
    def __init__(self):
        self.messages = []

    def add_user(self, text):
        self.messages.append({
            "role": "user",
            "parts": [
                {
                    "text": text
                }
            ],
        })

    def add_assistant(self, text):
        self.messages.append({
            "role": "model",
            "parts": [
                {
                    "text": text
                }
            ],
        })

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages.clear()