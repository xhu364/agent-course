from langchain_core.language_models import BaseChatModel

from .single_agent import SingleAgent


class WriterAgent(SingleAgent):

    def __init__(self, llm: BaseChatModel):
        super().__init__(
            llm=llm,
            tools=[],
            system_prompt="""
You are a communication specialist.

Your job is to:
- Turn provided findings into a clear response.
- Organize information logically.
- Avoid inventing facts.
- Make the answer easy for the user to understand.

You are responsible for producing the final response.
""",
            max_iterations=3,
        )
