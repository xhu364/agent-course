from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import os

llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
)

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are an experienced Python mentor."), ("human", "{question}")]
)

chain = prompt | llm

response = chain.invoke({"question": "Explain decorators with example."})

print(response.content)
