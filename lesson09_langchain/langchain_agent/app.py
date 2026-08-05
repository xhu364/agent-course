from langchain_core.messages import HumanMessage
from llm import create_llm
from tools import calculator, get_weather

llm = create_llm()

tools = [
    calculator,
    get_weather,
]

llm_with_tools = llm.bind_tools(tools)


question1 = "What is 123 * 456?"
question2 = "What is temperature in Boston today"

response = llm_with_tools.invoke(
    [HumanMessage(content=question1), HumanMessage(content=question2)]
)

print(response)
