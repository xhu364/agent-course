from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful teacher."),
        ("human", "Explain: {question}"),
    ]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
)

parser = StrOutputParser()

pipeline = prompt | llm | parser

response = pipeline.invoke({"question": "Write a hello world in Python."})

print(response)
