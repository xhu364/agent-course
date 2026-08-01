from google import genai

from config import GEMINI_API_KEY
from prompt import create_prompt


client = genai.Client(
    api_key=GEMINI_API_KEY
)


code = """
def divide(a,b):
    return a/b
"""


prompt = create_prompt(code)

print(prompt)

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt
)


print(response.text)