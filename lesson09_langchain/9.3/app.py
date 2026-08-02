from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant."), ("human", "{question}")]
)

llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
)

pipeline = prompt | llm

response = pipeline.invoke({"question": "What is the capital of China?"})

# output
# <class 'langchain_core.runnables.base.RunnableSequence'>
# <class 'str'>
# The capital of China is Beijing.
print(type(pipeline))
print(type(response.content))
print(response.content)
