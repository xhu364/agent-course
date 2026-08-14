from langchain_core.language_models import BaseChatModel

from .single_agent import SingleAgent


class DataAgent(SingleAgent):

    def __init__(self, llm: BaseChatModel):
        super().__init__(
            llm=llm,
            tools=[],
            system_prompt="""
You are a data analysis specialist.

Your job is to:
- Analyze numerical or structured information.
- Identify trends and anomalies.
- Perform calculations when needed.
- Explain the analytical reasoning clearly.

Return your findings to the orchestrator.
Do not write the final user-facing answer.
""",
            max_iterations=3,
        )
