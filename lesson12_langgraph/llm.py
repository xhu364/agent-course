from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


def create_llm(llm_type="llama"):
    if llm_type == "llama":
        return ChatOllama(
            model="llama3.2:3b",
            temperature=0.0,
        )
    elif llm_type == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.0,
        )
