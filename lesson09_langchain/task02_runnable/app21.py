from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

{"question": "Explain Python decorators in 50 words."}
prompt = ChatPromptTemplate.from_template("question: {question}")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
)

parser = StrOutputParser()

pipeline = prompt | llm | parser

response = pipeline.invoke({"question": "Explain Python decorators."})

print(response)
