from google import genai

from config import GEMINI_API_KEY
from prompt import prompt_text

client = genai.Client(api_key=GEMINI_API_KEY)


code = """
def divide(a,b):
    return a/b
"""


prompt = prompt_text.format(topic="Kafka")

print(prompt)

response = client.models.generate_content(
    model="gemini-2.5-flash-lite", contents=prompt
)


print(response.text)
