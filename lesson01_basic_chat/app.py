from google import genai
from config import GEMINI_API_KEY
import time

client = genai.Client(api_key=GEMINI_API_KEY)

start_time = time.time()
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Explain what Kubernetes is in one paragraph."
)
end_time = time.time()

print(end_time - start_time, response.text)