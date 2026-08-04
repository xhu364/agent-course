from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.

Rule: only output json string without any additional string.

Question:
{question}
""")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.0,
)

parser = StrOutputParser()


chain = RunnablePassthrough.assign(answer=prompt | llm | parser).assign(
    word_count=lambda x: len(x["answer"].split())
)
response = chain.invoke({"question": "Explain decorators"})
print(response)
