from langchain_core.language_models import BaseChatModel

from .single_agent import SingleAgent


class ResearchAgent(SingleAgent):

    def __init__(self, llm: BaseChatModel):
        super().__init__(
            llm=llm,
            tools=[],
            system_prompt="""
You are a research specialist.

Your job is to:
- Analyze the user's research question.
- Identify important facts.
- Separate facts from assumptions.
- Provide concise findings to the orchestrator.

You are not responsible for writing the final answer.
Return useful research findings that another agent can consume.
""",
            max_iterations=3,
        )
