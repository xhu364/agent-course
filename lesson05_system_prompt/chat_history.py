class ChatHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, text):
        self.messages.append({
            "role": role,
            "parts": [
                {
                    "text": text
                }
            ],
        })

    def add_model(self, text):
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