from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

summary_prompt = ChatPromptTemplate.from_template("""
    Explain the following programming topic.

    Topic:
    {topic}

    Provide a concise summary.
    """)


# Prompt 2: Interview questions
quiz_prompt = ChatPromptTemplate.from_template("""
    Create three interview questions about:

    {topic}

    Include answers.
    """)


# Prompt 3: Keywords
keyword_prompt = ChatPromptTemplate.from_template("""
    Extract five important keywords about:

    {topic}

    Return only a comma-separated list.
    """)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.0,
)

parser = StrOutputParser()

summary_chain = summary_prompt | llm | parser
quiz_chain = quiz_prompt | llm | parser
keyword_chain = keyword_prompt | llm | parser

parallel_chain = RunnableParallel(
    summary_chain=summary_chain,
    quiz_chain=quiz_chain,
    keyword_chain=keyword_chain,
)

response = parallel_chain.invoke({"topic": "Python decorators"})
print(response)
