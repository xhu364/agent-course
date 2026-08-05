from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from prompt import initial_prompt, example_prompt, quiz_prompt, keyword_prompt
from llm import create_llm
from add_metadata import add_metadata

prompt = initial_prompt
llm = create_llm()
parser = StrOutputParser()

initial_chain = RunnablePassthrough.assign(explanation=prompt | llm | parser).assign(
    summary=lambda x: x["explanation"]
) | RunnableLambda(add_metadata)

example_chain = (
    RunnableLambda(lambda x: {"explanation": x["explanation"]})
    | example_prompt
    | llm
    | parser
)

quiz_chain = (
    RunnableLambda(lambda x: {"explanation": x["explanation"]})
    | quiz_prompt
    | llm
    | parser
)

keyword_chain = (
    RunnableLambda(lambda x: {"explanation": x["explanation"]})
    | keyword_prompt
    | llm
    | parser
)

chain = initial_chain | RunnablePassthrough.assign(
    example=example_chain,
    quiz=quiz_chain,
    keywords=keyword_chain,
)

response = chain.invoke({"topic": "Python decorators"})
print(response)
# {
#    "question": "...",
#    "summary": "...",
#    "metadata": {
#        "words": ...,
#        "reading_time": ...
#    },
#    "quiz": "...",
#    "keywords": [...],
#    "examples": "..."
# }
