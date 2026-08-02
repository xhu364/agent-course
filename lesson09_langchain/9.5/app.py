from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from company import Company

from config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY, temperature=0
)


parser = PydanticOutputParser(pydantic_object=Company)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an information extraction assistant.

Extract company information.

Return ONLY the JSON format.

{format_instructions}
""",
        ),
        ("human", "{text}"),
    ]
)

chain = prompt | llm | parser

result = chain.invoke(
    {
        "text": """
    Apple was founded by Steve Jobs in 1976.
    It creates consumer electronics such as iPhones and Macs.
    """,
        "format_instructions": parser.get_format_instructions(),
    }
)

print(type(result))
print(result)
