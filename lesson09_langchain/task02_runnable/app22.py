from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.

Question:
{question}
""")


def summary(message: str):
    return {
        "answer": message,
        "words": len(message.split()),
        "characters": len(message),
        "reading_time": "1 minute",
    }


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.0,
)

parser = StrOutputParser()

pipeline = prompt | llm | parser | RunnableLambda(summary)

response = pipeline.invoke({"question": "Explain code war in less than 50 words."})

print(response)
