from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from dotenv import load_dotenv

load_dotenv()


def create_llm(llm_type="ollama"):
    if llm_type == "ollama":
        return ChatOllama(
            model="llama3.2:3b",
            temperature=0.0,
        )

    if llm_type == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.0,
        )

    raise ValueError(f"Unsupported LLM type: {llm_type}")
