from config import GEMINI_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GEMINI_API_KEY,
)
#llm = ChatOllama(
#    model="llama3.2",
#    temperature=0.7,
#)

response = llm.invoke("Hello")

#print(response.content)
print(type(response))
print()

print(response)
print()

print(response.content)
print()

print(response.response_metadata)
print()

print(response.usage_metadata)
